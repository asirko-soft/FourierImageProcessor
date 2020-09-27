import os
import cv2
import imutils
import re
from imutils import perspective
from imutils import contours
import numpy as np
import pytesseract
directory = r'C:\Users\ufo\Downloads\Cu_SEM_photos for Fourier'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
size=''
def append_suffix(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{suffix}{ext}".format(name=name, suffix='_legend', ext=ext)

def extract_size(text):
	global size
	if ('um') in text :
		size = re.search('\d+um', text).group(0)
	elif ('nm') in text :
		size = re.search('\d+nm', text).group(0)
	else:
		print('Shitty image detected')
	return size

def findSizetoRatio(path) :
	print('----------------START PROCESS NEW IMAGE----------------')
	print(path)
	img = cv2.imread(path)

	# crop the image legend, part with line and size in pixels
	img_legend = img[1440:1536, 1600:1920]
	# cv2.imshow("cropped", img_legend)
	scale_gray = cv2.cvtColor(img_legend, cv2.COLOR_BGR2GRAY)
	edged = cv2.Canny(scale_gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)
	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# sort the contours from left-to-right

	(cnts, _) = contours.sort_contours(cnts)

	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.arcLength(c, True) < 250:
			continue
		# compute the rotated bounding box of the contour
		box = cv2.minAreaRect(c)
		(x, y), (width, height), angle = box
		print('width is ', width, ' height is ', height)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")
		box = perspective.order_points(box)
		# draw the contours on the image
		orig = img_legend.copy()
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
	# detect text on original image
	text = pytesseract.image_to_string(img)
	print (text)

	print(extract_size(text), ' are ', round(max(height, width)), ' pixels on image ')
	# write image_legend to validate results
	cv2.imwrite(append_suffix(path), img_legend)


for entry in os.scandir(directory):
	if (entry.path.endswith(".jpg")) and entry.is_file():
		print(entry.path)
		findSizetoRatio(entry.path)