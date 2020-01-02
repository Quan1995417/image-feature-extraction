#Feature Descriptors for Images
The intent of this project is to find the following feature descriptors of images - first 3 color moments - Mean (first), Variance (Second), Skewness (Third) and SIFT (Scale Invariant feature Transform). The feature descriptors are then stored in SQLite database. Using these feature descriptors k similar images are found.

### Prerequisites

Following packages need to be installed:

•	Python3

•	cv2

•	scipy
### Author
Rinku Nemade

### How to Use
All the image inputs are of resolution 1200 x 1600. The feature descriptors are calculated after splitting image in 100 x 100 blocks.
There are 3 utilities in this project:
#### task1:
##### Input:
•	Filename: Image file name along with extension (eg. Hand00002.jpg).

•	Feature: Color moments and SIFT are two features available. Select appropriate feature number (1 for color moments and 2 for SIFT)

##### Output:
1.	Color Moments: Before calculating color moments image is converted to YUV representation. Prints array of vectors of size 12 x 16; each vector consists of 9 elements – [mean of Y, mean of U, mean of V, variance of Y, variance of U, variance of V, skewness of Y, skewness of U, skewness of V]
2.	SIFT: Calculates feature descriptors and keypoints for the image. Feature descriptors are displayed in form of array of vectors of size 12 x 16.  Keypoints are drawn on the image and stored as mentioned in SIFTLib.
#### task2:
##### Input:

•	Name of a folder which contains multiple images.

##### Output:
1.	For each image in the folder first 3 color moments values and SIFT descriptors are calculated. Color moments are stored in table named colorMoments with image name as primary key. SIFT descriptors and keypoints are stored in table named sift. Also, for each image keypoints are drawn on a image and saved as mentioned in SIFTLib.

#### task3:
##### Input:
•	Filename: Image file name (referred as query image) along with extension (eg. Hand00002.jpg).

•	Feature: Color moments and SIFT are two features available. Select appropriate feature number (1 for color moments and 2 for SIFT)

•	k: Number of similar images to be found.
##### Output:
1.	k similar images to query image. Following are the two options:

* Color moments: The distance of query image is calculated with every other image and then top k values of minimum distance are displayed in form {image name: distance, ….}

* SIFT: The vectors in query image are compared with each of the vectors in target image (all images other than query images) to find best match and second best match for the vector in query image. Euclidian distance is used to calculate distance between two feature vectors. After calculating best and second best match, a ratio of 0.65 is used as a measure to find good matches. Then similarity is calculated as ratio of good matches to number of keypoint (maximum of number of keypoints in query image and target image). Top k similarities values (maximum values) are displayed in form {image name: similarity, …..}.
#### colorMomentsLib:
•	This provides color_moments utility to calculate color moments given an image.
#### SIFTLib:
This provides following functions:

•	sift: Calculation of feature descriptors and keypoints given image and filename. Also the keypoints are drawn and saved with same file name (filename) prefixed with ’ sift_keypoints_’.

•	feature_file: Returns the name of file with keypoints drawn on it given a filename as input.

•	Formatted_keypoints: Displays x,y co-ordinates, size, angle, response and octave values of a SIFT keypoints array.

