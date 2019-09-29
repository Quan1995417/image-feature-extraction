import sys
import cv2
import numpy as np
import colorMomentsLib as cm
import SIFTLib

filename = str(input("Enter image file name: "))
feature = int(input("Select a feature model:\n 1. color momemts \n 2. SIFT  \n"))

#read image
img = cv2.imread(filename) #('Hand_0000002.jpg')

if feature == 1:
    colorMoments = cm.color_moments(img)
    np.set_printoptions(suppress=True, threshold=sys.maxsize, linewidth=1000)
    print(colorMoments)

elif feature == 2:
    dest, keypoints = SIFTLib.sift(img, filename)
    np.set_printoptions(threshold=sys.maxsize, linewidth=500)
    print("Feature Descriptors:\n", dest)
    cv2.imshow('SIFT', cv2.imread(SIFTLib.feature_file(filename), 1))
    cv2.waitKey()
    cv2.destroyAllWindows()