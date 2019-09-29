# Module to calculate first 3 color moments
# input: RGB image
# output: First 3 color moments for YUV color model (100*100 window)

import cv2
from scipy import stats as stat
import numpy as np

def color_moments(img):
    # convert RGB image to YUV color represetation
    yuvImg = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)

    colorMoments = np.empty([12, 16, 9], dtype=float)

    # iterate over all the rows of the windows
    for i in range(12):
        # iterate over all the columns of the Windows
        for j in range(16):
            # initialize vectors for Y, U, V values
            y, u, v = [], [], []
            # Iterate over pixels in each window
            for p in range(100):
                for q in range(100):
                    # pixel value
                    pixel = yuvImg[i * 100 + p, j * 100 + q]
                    # Store Y, U, V channel values in respective vectors
                    y.append(pixel[0])
                    u.append(pixel[1])
                    v.append(pixel[2])
            # First color moment (mean of color channels)
            colorMoments[i][j] = [round(np.mean(y), 2), round(np.mean(u), 2), round(np.mean(v), 2),
            # Second color moment (std deviation of color channels)
                                    round(np.std(y), 2), round(np.std(u), 2), round(np.std(v), 2),
            # Third color moment (skewness of color channels)
                                    round(stat.skew(y), 2), round(stat.skew(u), 2), round(stat.skew(v), 2)]
    return colorMoments