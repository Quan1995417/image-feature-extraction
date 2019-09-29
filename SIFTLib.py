import cv2
import os
def sift(img, filename):
    sift = cv2.xfeatures2d.SIFT_create()

    kp, dest = sift.detectAndCompute(img, None)
    keypoints = []
    for point in kp:
        temp = (point.pt, point.size, point.angle, point.response, point.octave)
        keypoints.append(temp)

    img = cv2.drawKeypoints(img, kp, None)

    cv2.imwrite(feature_file(filename), img)
    return dest, kp

def feature_file(filename):
    if not os.path.exists('siftKeypoints'):
        os.mkdir('siftKeypoints')
    return os.path.join('siftKeypoints' , 'sift_keypoints_' + filename)

def formatted_keypoints(kp):
    keypoints = []
    for point in kp:
        temp = (point.pt, point.size, point.angle, point.response, point.octave)
        keypoints.append(temp)
    return keypoints