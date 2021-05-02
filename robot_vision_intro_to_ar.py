import cv2

# Read an image as BGR

apriltag_img = cv2.imread('/content/drive/My Drive/Robot/man3.jpg') # use your own path in google drive

""">> 2. Detect the corners of the apriltag. It requires step #2, #3, and #4. """

# load Tag36h11 in aruco dictionary
ARUCO_DICT = {"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11}
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_APRILTAG_36h11"])

import numpy as np
arucoParams = cv2.aruco.DetectorParameters_create()
(image_points, ids, rejected) = cv2.aruco.detectMarkers(apriltag_img, arucoDict,
	parameters=arucoParams)
print("image_points:", image_points)
print("id:", ids)

# by default, the four corners are (x,y) coordinates in the image, with pixel as unit. 
# The order of the four corners are top-left, top-right, bottom-right, and bottom-left

# Ensure that at least one tag is detected, then prepare the corners for drawing:
if len(image_points) > 0:
	# flatten the ArUco IDs list
	x=0
	topRight1 = []
	topLeft1 = []
	bottomRight1 = []
	bottomLeft1 = []
	image_points1 = []
	ids = ids.flatten()

# draw the ArUco marker ID on the image

print("[INFO] ArUco marker ID: {}".format(ids[1]))


