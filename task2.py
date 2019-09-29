import os
import sys
import numpy as np
import sqlite3
import cv2
import colorMomentsLib as cm
import SIFTLib
import json

folder = str(input("Enter folder name: "))

# connecting to the database
connection = sqlite3.connect("features.db")
# cursor
crsr = connection.cursor()

# create table to store color moments
sql_color = """CREATE TABLE IF NOT EXISTS colorMoments (image_id VARCHAR(100) PRIMARY KEY, moments BLOB);"""
# create table to store sift descriptors and keypoints
sql_sift = """CREATE TABLE IF NOT EXISTS sift (image_id VARCHAR(100) PRIMARY KEY, descriptor BLOB, keypoints BLOB);"""

# execute db query to create tables
crsr.execute(sql_color)
crsr.execute(sql_sift)

crsr.execute("""DELETE from colorMoments;""")
crsr.execute("""DELETE from sift;""")

# iterate over each image in the folder
for img_path in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, img_path), 1)
    #get color moments for the image
    colorMoments = cm.color_moments(img)

    #query to store color moment values
    sql_color = """INSERT INTO colorMoments VALUES (?, ?);"""

    #get sift descriptors and keypoints for the image
    dest, keypoints = SIFTLib.sift(img, img_path)
    kps = SIFTLib.formatted_keypoints(keypoints)

    #query to store sift descriptors and keypoints in the database
    sql_sift = """INSERT INTO sift VALUES (?,?,?);"""

    #execute queries to store values in the db
    crsr.execute(sql_color, [img_path, json.dumps(colorMoments.tolist())])
    crsr.execute(sql_sift, [img_path, json.dumps(dest.tolist()), json.dumps(kps)])
    connection.commit()
connection.close()