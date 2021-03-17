import numpy as np
import imutils
import cv2


class Localizer():
    def __init__(self, markers: list, camera, servo_driver, arm_driver) -> None:
        """
        Markers is a list of coordinates for each perimeter marker
        """
        self.markers = markers
        self.camera = camera
        self.servo_driver = servo_driver
        self.arm_driver = arm_driver

        # L_* are the lengths between markers
        # constant for a given set of markers
        self.L_AB = np.linalg.norm(markers[0]-markers[1])
        self.L_BC = np.linalg.norm(markers[1]-markers[2])
        self.L_CD = np.linalg.norm(markers[2]-markers[3])
        self.L_DA = np.linalg.norm(markers[3]-markers[0])

        # set the colour ranges for the markers
        # OpenCV HSV colour range is H: 0-179, S: 0-255, V: 0-255
        self.colour_ranges = {'A': ((10, 100, 100), (25, 255, 255)),  # orange
                              'B': ((10, 100, 100), (25, 255, 255)),
                              'C': ((10, 100, 100), (25, 255, 255)),
                              'D': ((10, 100, 100), (25, 255, 255))}

        return

    def compute_thetas(self, phi_A, phi_B, phi_C, phi_D):
        # convert all angles to cw
        if phi_A < 0:
            phi_A = 360 + phi_A
        if phi_B < 0:
            phi_B = 360 + phi_B
        if phi_C < 0:
            phi_C = 360 + phi_C
        if phi_D < 0:
            phi_D = 360 + phi_D

        # get min to determine general orientation
        phi_min = np.amin(np.array([phi_A, phi_B, phi_C, phi_D]))

        # calculate generic case for all thetas
        theta_AB = phi_B - phi_A
        theta_BC = phi_C - phi_B
        theta_CD = phi_D - phi_C
        theta_DA = phi_A - phi_D

        # one theta does not fit generic case based on orientation
        if phi_min == phi_A:
            theta_DA = 360 - phi_D + phi_A
        elif phi_min == phi_B:
            theta_AB = 360 - phi_A + phi_B
        elif phi_min == phi_C:
            theta_BC = 360 - phi_B + phi_C
        elif phi_min == phi_D:
            theta_CD = 360 - phi_C + phi_D

        return np.array([theta_AB, theta_BC, theta_CD, theta_DA])

    def compute_location(self, phi_A, phi_B, phi_C, phi_D):
        (theta_AB, theta_BC, theta_CD, theta_DA) = self.compute_four_thetas(phi_A, phi_B, phi_C, phi_D)

        best_error = 360

        for i in range(round(self.L_BC)):
            for j in range(round(self.L_CD)):
                # calculate distance to each marker
                point = np.array([i, j])
                d_A = np.linalg.norm(point - self.markers[0])
                d_B = np.linalg.norm(point - self.markers[1])
                d_C = np.linalg.norm(point - self.markers[2])
                d_D = np.linalg.norm(point - self.markers[3])

                # calculate each theta
                ctheta_AB = np.rad2deg(np.arccos((self.L_AB**2 - d_A**2 - d_B**2)/(-2*d_A*d_B)))
                ctheta_BC = np.rad2deg(np.arccos((self.L_BC**2 - d_B**2 - d_C**2)/(-2*d_B*d_C)))
                ctheta_CD = np.rad2deg(np.arccos((self.L_CD**2 - d_C**2 - d_D**2)/(-2*d_C*d_D)))
                ctheta_DA = np.rad2deg(np.arccos((self.L_DA**2 - d_D**2 - d_A**2)/(-2*d_D*d_A)))

                # compute the error for this position
                error = np.sum(np.array([
                    np.abs(theta_AB - ctheta_AB),
                    np.abs(theta_BC - ctheta_BC),
                    np.abs(theta_CD - ctheta_CD),
                    np.abs(theta_DA - ctheta_DA)
                ]))

                # update location if error is smallest
                if error < best_error:
                    best_error = error
                    location = [i, j]

        return np.array(location)

    def localize(self):
        X_PIXELS = 320
        phi_angles = {'A': None, 'B': None, 'C': None, 'D': None}

        # tilt camera up
        self.servo_driver.tilt(0)

        # put collection arm down
        self.arm_driver.down()

        camera_angle = 180

        while camera_angle > -180:
            # update camera angle and move camera
            camera_angle -= 31.1
            self.servo_driver.pan(camera_angle)

            # take photo
            image = self.camera.read()

            # check photo for each marker
            centers = {'A': None, 'B': None, 'C': None, 'D': None}
            for marker in ('A', 'B', 'C', 'D'):
                centers[marker] = (X_PIXELS/2) - self.detect_marker(image, marker)

            if centers['A'] is None and centers['B'] is None and centers['C'] is None and centers['D'] is None:
                # no markers detected, continue searching
                continue
            else:
                # if multiple markers are seen, take the most clockwise one
                most_cw = max(centers.values())
                marker = [key for key in centers if centers[key] == most_cw]
                marker = marker[0]
                center = centers[marker]

                # fine tune the camera angle until the marker is directly inline,
                # this is the angle to the marker
                while np.abs(center) > 20:  # 20 pixels off centre could be reduced
                    camera_angle += (center/(X_PIXELS/2))*31.1
                    self.servo_driver.pan(camera_angle)

                    image = self.camera.read()

                    center = self.detect_marker(image, marker)

                # now camera_angle is angle to marker
                phi_angles[marker] = camera_angle

            # repeat until all markers are seen
            none_angles = [key for key in phi_angles if phi_angles[key] is None]
            if len(none_angles) == 0:
                break

        # call compute_location
        location = self.compute_location(phi_angles['A'], phi_angles['B'], phi_angles['C'], phi_angles['D'])

        # send the location back to main
        print(location)

        return

    def detect_marker(self, image, marker):
        # convert colour space to HSV becuase it is easier to segment colours
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # blur the image
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        # get the ranges for this marker colour
        low = self.colour_ranges[marker][0]
        high = self.colour_ranges[marker][1]

        # threshold the image to isolate orange
        mask = cv2.inRange(hsv, low, high)

        # erode and dilate to remove small false positives
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find the biggest contour in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # make sure the ares of the contour is above a minimum to count as
        # a marker detection
        area = cv2.contourArea(cnts)
        if area > 150:
            # compute the center of the contour
            M = cv2.moments(cnts)
            cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])  # don't need y axis center

            return cX
        else:
            return None