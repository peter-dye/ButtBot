import cv2
import imutils
import numpy as np


# import the images
colour = 'from_bot'
images = []
for i in range(1, 5, 1):
    img = cv2.imread(colour+"/"+str(i)+".png")
    images.append(img)

for i in range(len(images)):
    # resize the image
    resized = imutils.resize(images[i], width=300)
    cv2.imshow("", resized)
    cv2.waitKey(0)

    # convert colour space to HSV becuase it is easier to segment colours
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # blur the image
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    # define bounds for the orange colour
    # opencv HSV colour range is H: 0-179, S: 0-255, V: 0-255
    low_orange = (10, 100, 100)
    high_orange = (25, 255, 255)

    colour = 'purple'
    colour_ranges = {'orange': ((11, 150, 100), (21, 255, 255)),
                     'green': ((42, 50, 100), (75, 255, 255)),
                     'yellow': ((24, 50, 100), (31, 255, 255)),
                     'purple': ((133, 50, 100), (150, 255, 255))}

    low = colour_ranges[colour][0]
    high = colour_ranges[colour][1]

    # threshold the image to isolate orange
    mask = cv2.inRange(hsv, low, high)

    # erode and dilate to remove small false positives
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find the biggest contour in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # print the area of the contour
        print(cv2.contourArea(cnts))

        # compute the center of the contour
        M = cv2.moments(cnts)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and its center on the image
        cv2.drawContours(resized, [cnts], -1, (0, 255, 0), 2)
        cv2.circle(resized, (cX, cY), 7, (0, 255, 0), -1)
        cv2.putText(resized, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow("", resized)
        cv2.waitKey(0)


# # convienience function to view and visually inspect all 5 images
# def show_images(images):
#     for img in images:
#         cv2.imshow("", img)
#         cv2.waitKey(0)
#
#
# # converts a 0 or 1 mask to RGB so it can be concatenated with normal images
# def mask_to_rgb(img):
#     new_img = np.empty((img.shape[0], img.shape[1], 3))
#
#     for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#             if img[i][j] == 0:
#                 # new_img[i][j] = [0, 0, 0]
#                 new_img[i][j][0] = 0
#                 new_img[i][j][1] = 0
#                 new_img[i][j][2] = 0
#             else:
#                 # new_img[i][j] = [255, 255, 255]
#                 new_img[i][j][0] = 255
#                 new_img[i][j][1] = 255
#                 new_img[i][j][2] = 255
#
#     return new_img
#
#
# # detects colours based on HSV range
# def detect_orange(img):
#     new_img = np.zeros((img.shape[0], img.shape[1]))
#
#     for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#
#             blue = float(img[i][j][0])
#             green = float(img[i][j][1])
#             red = float(img[i][j][2])
#
#             if blue < 40 and red/green > 1.5 and red/green < 3.0:
#                 new_img[i][j] = 1
#
#     return new_img
#
#
# # attempting inRange with RGB
# def detect_orange_range(img):
#     min = (0, 50, 100)
#     max = (50, 100, 220)
#     return cv2.inRange(img, min, max)
#
#
# def draw_contour_center(image, c, i):
#     # compute the center of the contour area and draw a circle
#     # representing the center
#     M = cv2.moments(c)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     # draw the countour number on the image
#     cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
#         1.0, (255, 255, 255), 2)
#     # return the image with the contour number drawn on it
#     return image
