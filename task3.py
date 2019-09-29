import sys
import numpy as np
import cv2
import sqlite3
import json
import math
import os

# input input image filename
filename = str(input("Enter a image file name: "))
#input feature model
feature = int(input("Select a feature model number:\n 1 Color Moments\n 2 SIFT\n"))
# input k
k = int(input("Enter value of k: "))

#dictionary to maintin distance from input image
k_arr = {}
# connecting to the database
connection = sqlite3.connect("features.db")
# cursor
crsr = connection.cursor()

#save to folder
def save_output(foldername, k_arr):
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    for f in k_arr.keys():
        img = cv2.imread(os.path.join('rinku',f))
        cv2.imwrite(os.path.join(foldername , f), img)

# function to calculate eucliden distance between vectors of blocks
def euclidean(moment, moments):
    sum = 0
    for j in range (0,12):
        for k in range (0, 16):
            for i in range (0, 9):
                sum += ((moments[j][k][i] - moment[j][k][i]) ** 2)
    return (sum ** (0.5))

# function for insertion sort in dictionary
def insert_dist(dist, name):
    # insert ecuclidean distance and filename as key in the dictionary
    k_arr[name] = dist
    if (len(k_arr) > k):
        # find maximum distance from the dictionary
        maximum = max(k_arr.keys(), key=(lambda k: k_arr[k]))
        # remove the element which has maximum distance from input image so that the length is maintained to k
        del k_arr[maximum]

def colorMomets():
    # query to get feature descriptors for input image
    sql = """SELECT moments FROM colorMoments WHERE image_id = '""" + filename + """';"""
    crsr.execute(sql)
    first = crsr.fetchall()

    # parse the feature discriptors to get as numpy array
    for row in first:
        l = json.loads(row[0])
        moment = np.asarray(l).reshape(12, 16, 9)

    # query to get color moments for all images except input image
    sql_color = """SELECT * FROM colorMoments WHERE image_id != '""" + filename + """';"""
    crsr.execute(sql_color)
    rows = crsr.fetchall()

    # parse color moments to get numpy array
    for row in rows:
        l = json.loads(row[1])
        moments = np.asarray(l).reshape(12, 16, 9)
        dist = euclidean(moment, moments)
        insert_dist(dist, row[0])
    print(k, " similar images using color moments are: ", sorted(k_arr.items(), key=lambda z: z[1]))
    output_folder = 'color_moments_'+ filename[0:-4] + "_" + str(k)
    save_output(output_folder, k_arr)

# function to find top 2 best matches for each block using descriptors
def sift_match(dest_main, dest_l):
    matches = []
    # iterate over query image blocks to calculate sift
    for qv in dest_main:
        distances = []
        for cv in dest_l:
            dist = 0
            for i in range(0, 128):
                dist += ((cv[i] - qv[i]) ** 2)
            distances.append(math.sqrt(dist))
        distances.sort()
        matches.append((distances[0], distances[1]))
    return matches

def cal_sift():
    # query sift descriptors for input image
    sql = """SELECT descriptor, keypoints FROM sift WHERE image_id = '""" + filename + """';"""
    crsr.execute(sql)
    rows = crsr.fetchall()

    # parse values to get descriptors and keypoints
    for row in rows:
        dest = row[0]
        kp = row[1]
        dest_main = json.loads(dest)
        kp_main = json.loads(kp)

    # Calculate length of keypoints for input image
    len_kp_main = len(kp_main)

    # query descriptors, keypoints for all other images
    sql = """SELECT * FROM sift WHERE image_id != '""" + filename + """';"""
    crsr.execute(sql)
    rows = crsr.fetchall()

    # parse data to descriptors, keypoints along with image name
    for row in rows:
        dest = row[1]
        kp = row[2]
        dest_l = json.loads(dest)
        kp_l = json.loads(kp)
        matches = sift_match(dest_main, dest_l)

        # List of good matches which are decided using 0.65 as a factor
        good_matches = []
        for match in matches:
            if match[0] < (0.65 * match[1]):
                good_matches.append(match[0])

        # get maximum number of keypoints to calculate similarity percentage
        if len_kp_main > len(kp_l):
            n_kp = len_kp_main
        else:
            n_kp = len(kp_l)

        # calculate similaritry and updat the list for k similar images
        similarity = (len(good_matches) / n_kp)
        k_arr[row[0]] = similarity

        # Remove extra elements from list to maintain length k
        if (len(k_arr) > k):
            # find minimum distance from the dictionary
            minimum = min(k_arr.keys(), key=(lambda k: k_arr[k]))
            # remove the element which has minimum distance from input image so that the length is maintained to k
            del k_arr[minimum]
    print(k, " similar images using sift are : ", sorted(k_arr.items(), key=lambda z: z[1], reverse=True))
    output_folder = 'sift_' + filename[0:-4] + "_" + str(k)
    save_output(output_folder, k_arr)

if feature == 1:
    colorMomets()
elif feature == 2:
    cal_sift()

connection.close()
