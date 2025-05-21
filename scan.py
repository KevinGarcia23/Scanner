from transform import four_point_transform #used to find the image we are scanning
#transform.py is a file by pyimagesearch 
from skimage.filters import threshold_local #helps obtain black and white images
import numpy as np #used for numerical processing
import argparse #used for parsing command line arguements
import cv2 #used for our OpenCV bindings
import imutils #used for resizing, rotating, and cropping images

#construct the argument parser and parse the arguements
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image to be scanned")
args = vars(ap.parse_args())

#Edge detection using openCV
#loads the image and computes the ratio of the old height, 
# to the new height, resizes and clones it
image = cv2.imread(args["image"])
ratio = image.shape[0]/500.0 
original = image.copy()
image = imutils.resize(image, height = 500)

#converting the image to grayscale and find edges within the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0) # removing high frequency noise
edged = cv2.Canny(gray, 75, 200) #canny edge detection 

#show the original image and the edges detected 
print("STEP 1: Edge Dectection")
cv2.imshow ("Image", image)
cv2.imshow ("edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

#finding the contours in the edged image, keeping only the largest ones
#and intializing the screen contour
contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5] 
#^sorting the contours by area and keeping the largest ones, and discarding the rest

#loops over contours
for c in contours:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    # if our contour has 4 points then we have found our screen
    if len(approx) ==4:
        screenContour = approx
        break
#show the outline of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenContour], -1, (0,225,0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#applying the four point transfrom to obtain a top-down view of the paper
warped = four_point_transform(original, screenContour.reshape(4,2)* ratio)

#convert warped into grayscale, and applying adaptive threshholding
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

#show the original and scanned
print("STEP 3: Apply persepective transform")
cv2.imshow("Original", imutils.resize(original, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey()