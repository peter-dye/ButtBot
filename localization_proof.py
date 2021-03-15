"""
This is a proof of concept for the logic of the localization method.
"""

import numpy as np
# import matplotlib.pyplot as plt


class Location:
    """
    Class for different location related operations of the robot.
    The main functionality for now is localization.

    RESTRICTION: Markers can be in a trianlge at any locations, as long as the
    top two markers form a line parrallel to the x-axis of whatever coordinate
    system is defined.
    """

    def __init__(self, markers: list) -> None:
        """
        Markers is a list of coordinates for each perimeter marker
        """
        self.markers = markers

        # L_* are the lengths between markers
        # constant for a given set of markers
        self.L_AB = np.linalg.norm(markers[0]-markers[1])
        self.L_BC = np.linalg.norm(markers[1]-markers[2])

        # self.L_CA = np.linalg.norm(markers[2]-markers[0])

        self.L_CD = np.linalg.norm(markers[2]-markers[3])
        self.L_DA = np.linalg.norm(markers[3]-markers[0])


        # A_* are the angles of the triangle formed by markers
        # constant for a given set of markers
        # self.A_A = np.rad2deg(np.arccos(np.dot(markers[1]-markers[0], markers[2]-markers[0])/(self.L_AB*self.L_CA)))
        # self.A_B = np.rad2deg(np.arccos(np.dot(markers[0]-markers[1], markers[2]-markers[1])/(self.L_AB*self.L_BC)))
        # self.A_C = np.rad2deg(np.arccos(np.dot(markers[0]-markers[2], markers[1]-markers[2])/(self.L_CA*self.L_BC)))
        return

    def compute_thetas(self, phi_A, phi_B, phi_C) -> None:
        """
        phi_A, phi_B, phi_C, are the angles to known markers A, B, and C.
        The robot will start from straight ahead and look
        in a clockwise direction for 180 degrees. Then it will move
        counterclockwise to the front position and then look 180 degrees ccw
        from start. Cw anges will be positive and ccw angles will be negative.
        """

        # convert all angles to cw
        if phi_A < 0:
            phi_A = 360 + phi_A
        if phi_B < 0:
            phi_B = 360 + phi_B
        if phi_C < 0:
            phi_C = 360 + phi_C

        # calculate the theta angles
        # split into cases base on robot orientation
        if phi_A < phi_B and phi_B < phi_C:
            # pointing between A and C
            self.theta_AB = phi_B - phi_A
            self.theta_BC = phi_C - phi_B
            self.theta_CA = 360 - phi_C + phi_A
        elif phi_B < phi_C and phi_C < phi_A:
            # pointing betwwen A and B
            self.theta_AB = 360 - phi_A + phi_B
            self.theta_BC = phi_C - phi_B
            self.theta_CA = phi_A - phi_C
        elif phi_C < phi_A and phi_A < phi_B:
            # pointing between B and C
            self.theta_AB = phi_B - phi_A
            self.theta_BC = 360 - phi_B + phi_C
            self.theta_CA = phi_A - phi_C
        else:
            print("You forgot a case")

        return

    def compute_four_thetas(self, phi_A, phi_B, phi_C, phi_D):
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

    def is_inside(self) -> bool:
        """
        Returns True if robot is inside triangle and False if robot is outside
        the triangle or markers
        """
        if self.theta_AB > 180 or self.theta_BC > 180 or self.theta_CA > 180:
            return False
        else:
            return True

    def localize(self, phi_A, phi_B, phi_C) -> list:
        """
        Wrapper to choose the correct localization function (inside or outside)
        """
        self.compute_thetas(phi_A, phi_B, phi_C)
        if self.is_inside():
            coords = self.inside_localize()
        else:
            coords = self.outside_localize()
        return coords

    def inside_localize(self) -> list:
        """
        Calculate the position of the robot if it is inside the triangle
        of markers
        """
        # create and solve ax=b
        a = np.array([[1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 1, 0, 0],
                      [0, 0, 0, 0, 1, 1],
                      [1, 0, 0, 0, 0, 1],
                      [0, 1, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0]])
        b = np.array([self.A_A, self.A_B, self.A_C, 180-self.theta_CA, 180-self.theta_AB, 180-self.theta_BC])
        x = np.matmul(np.linalg.pinv(a), b)
        x = np.deg2rad(x)
        # hardcoded to use the AB line and marker A but any line/marker could be used
        # line/marker will have to be choosen dynamically if there are obstacles
        d = self.L_AB*((np.sin(x[2])*np.sin(x[1]))/np.sin(x[1]+x[2]))
        l = d/np.tan(x[1])
        rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_A)), -1*np.sin(np.deg2rad(self.A_A))],
                                    [np.sin(np.deg2rad(self.A_A)), np.cos(np.deg2rad(self.A_A))]])
        coords_vec = np.matmul(rotation_matrix, [-l, d])
        coords = markers[0]+coords_vec
        return coords

    def outside_localize(self) -> list:
        """
        Calculate the position of the robot if it is outside the triangle
        of markers. There are three distinct cases for being outside the
        trianlge: one for each side.
        """
        if self.theta_AB > 180:
            # outside of the triangle by the AB line

            # create and solve ax=b
            a = np.array([[0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 1, 1, 1],
                          [0, 0, 1, 1, 1, 0],
                          [1, 1, 0, 0, 0, 1],
                          [0, 1, 1, 0, 0, 0],
                          [1, 0, 0, 1, 1, 1]])
            b = np.array([self.A_C,
                          360-self.theta_BC-self.theta_CA,
                          180-self.theta_BC,
                          180-self.theta_CA,
                          180-self.theta_BC-self.theta_CA,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker A, non-trivial to use marker B
            d = self.L_AB*((np.sin(x[2])*np.sin(x[1]))/np.sin(x[1]+x[2]))
            l = d/np.tan(x[1])
            rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_A)), -1*np.sin(np.deg2rad(self.A_A))],
                                        [np.sin(np.deg2rad(self.A_A)), np.cos(np.deg2rad(self.A_A))]])
            coords_vec = np.matmul(rotation_matrix, [-l, -d])
            coords = markers[0]+coords_vec
            return coords

        elif self.theta_BC > 180:
            # outside of the triangle by the BC line

            # create and solve ax=b
            a = np.array([[1, 1, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 1, 1],
                          [0, 1, 1, 1, 0, 0],
                          [0, 0, 0, 1, 1, 0],
                          [1, 1, 1, 0, 0, 1]])
            b = np.array([self.A_A,
                          360-self.theta_AB-self.theta_CA,
                          180-self.theta_CA,
                          180-self.theta_AB,
                          180-self.theta_AB-self.theta_CA,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker C, non-trivial to use marker B
            d = self.L_AB*((np.sin(x[3])*np.sin(x[4]))/np.sin(x[4]+x[3]))
            l = d/np.tan(x[4])
            rotation_matrix = np.array([[np.cos(np.deg2rad(-self.A_C)), -1*np.sin(np.deg2rad(-self.A_C))],
                                        [np.sin(np.deg2rad(-self.A_C)), np.cos(np.deg2rad(-self.A_C))]])
            coords_vec = np.matmul(rotation_matrix, [l, -d])
            coords = markers[2]+coords_vec
            return coords

        elif self.theta_CA > 180:
            # outside of the triangle by the CA line

            # create and solve ax=b
            a = np.array([[0, 0, 1, 1, 0, 0],
                          [1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1],
                          [1, 0, 0, 0, 0, 1],
                          [0, 1, 1, 1, 1, 0]])
            b = np.array([self.A_B,
                          360-self.theta_AB-self.theta_BC,
                          180-self.theta_AB,
                          180-self.theta_BC,
                          180-self.theta_AB-self.theta_BC,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker A, could also use marker C
            d = self.L_AB*((np.sin(x[5])*np.sin(x[0]))/np.sin(x[0]+x[5]))
            l = d/np.tan(x[0])
            rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_A)), -1*np.sin(np.deg2rad(self.A_A))],
                                        [np.sin(np.deg2rad(self.A_A)), np.cos(np.deg2rad(self.A_A))]])
            coords_vec = np.matmul(rotation_matrix, [-l, d])
            coords_vec = [-l, d]
            coords = markers[0]+coords_vec
            return coords

        else:
            print("error")  # TODO: Make this a propper error being raised

        return

    def search_localize(self, phi_A, phi_B, phi_C):
        self.compute_thetas(phi_A, phi_B, phi_C)

        # change any thetas over 180 to be 360 - theta
        if self.theta_AB > 180:
            self.theta_AB = 360 - self.theta_AB
        elif self.theta_BC > 180:
            self.theta_BC = 360 - self.theta_BC
        elif self.theta_CA > 180:
            self.theta_CA = 360 - self.theta_CA

        # initialize error to be max
        best_error = 360

        # loop through all (x, y) coordinates in the space
        for i in range(200):
            for j in range(200):
                # calculate distance to each marker
                point = np.array([i, j])
                d_A = np.linalg.norm(point - self.markers[0])
                d_B = np.linalg.norm(point - self.markers[1])
                d_C = np.linalg.norm(point - self.markers[2])

                # calculate each theta
                ctheta_AB = np.rad2deg(np.arccos((self.L_AB**2 - d_A**2 - d_B**2)/(-2*d_A*d_B)))
                ctheta_BC = np.rad2deg(np.arccos((self.L_BC**2 - d_B**2 - d_C**2)/(-2*d_B*d_C)))
                ctheta_CA = np.rad2deg(np.arccos((self.L_CA**2 - d_C**2 - d_A**2)/(-2*d_C*d_A)))

                # compute the error for this position
                error = np.sum(np.array([
                    np.abs(self.theta_AB - ctheta_AB),
                    np.abs(self.theta_BC - ctheta_BC),
                    np.abs(self.theta_CA - ctheta_CA)
                ]))

                # update location if error is smallest
                if error < best_error:
                    best_error = error
                    location = [i, j]
                    # print(location)

                # if i == 169 and j == 42:
                #     print(ctheta_AB, ctheta_BC, ctheta_CA)
                # if i == 178 and j == 65:
                #     print(ctheta_AB, ctheta_BC, ctheta_CA)

        return np.array(location)

    def search_four_localize(self, phi_A, phi_B, phi_C, phi_D):
        (theta_AB, theta_BC, theta_CD, theta_DA) = self.compute_four_thetas(phi_A, phi_B, phi_C, phi_D)

        best_error = 360

        for i in range(200):
            for j in range(200):
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


# MAIN PROGRAM
# markers = np.array([[173, 109],
#                     [97, 5],
#                     [29, 109]])
# localizer = Location(markers)

# # case 1
# phi_A = 54
# phi_B = 153
# phi_C = -71
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('1. Expected: [83, 74] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([83, 74]-coords), 2)))
#
# # NOTE: Uncomment the matplotlib import at the top of the file to graph the markers and coordinates
# # x = [markers[0][0], markers[1][0], markers[2][0], coords[0]]
# # y = [markers[0][1], markers[1][1], markers[2][1], coords[1]]
# # plt.scatter(x, y)
# # plt.show()
#
# # case 2
# phi_A = -54
# phi_B = 110
# phi_C = -148
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('2. Expected: [115, 44] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([115, 44]-coords), 2)))
#
# # case 3
# phi_A = 155
# phi_B = -70
# phi_C = 13
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('3. Expected: [126, 88] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([126, 88]-coords), 2)))
#
# # case 4
# phi_A = -81
# phi_B = 159
# phi_C = -148
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('4. Expected: [169, 42] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([115, 44]-coords), 2)))
#
# # case 5
# phi_A = 15
# phi_B = -63
# phi_C = -15
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('5. Expected: [192, 97] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([192, 97]-coords), 2)))
#
# # case 6
# phi_A = 125
# phi_B = -35
# phi_C = 42
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('6. Expected: [131, 35] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([131, 35]-coords), 2)))
#
# # case 7
# phi_A = -30
# phi_B = 29
# phi_C = -100
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('7. Expected: [54, 23] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([54, 23]-coords), 2)))
#
# # case 8
# phi_A = 137
# phi_B = -161
# phi_C = 55
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('8. Expected: [34, 71] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([34, 71]-coords), 2)))
#
# # case 9
# phi_A = 52
# phi_B = 102
# phi_C = -11
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('9. Expected: [38, 23] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([38, 23]-coords), 2)))
#
# # case 10
# phi_A = -35
# phi_B = 32
# phi_C = 96
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('10. Expected: [98, 142] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([98, 142]-coords), 2)))
# print(localizer.theta_AB, localizer.theta_BC, localizer.theta_CA)
#
# # case 11
# phi_A = 128
# phi_B = -164
# phi_C = -79
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('11. Expected: [63, 122] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([63, 122]-coords), 2)))
#
# # case 12
# phi_A = -141
# phi_B = -43
# phi_C = 19
# coords = localizer.search_localize(phi_A, phi_B, phi_C)
# print('12. Expected: [147, 117] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
# print('Error: '+str(np.round(np.linalg.norm([147, 117]-coords), 2)))

# Cases for 4 markers
markers = np.array([[200, 200],
                    [200, 0],
                    [0, 0],
                    [0, 200]])
localizer = Location(markers)

# case 1
phi_A = 46
phi_B = 120
phi_C = -164
phi_D = -56
coords = localizer.search_four_localize(phi_A, phi_B, phi_C, phi_D)
print('1. Expected: [70, 123] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
print('Error: '+str(np.round(np.linalg.norm([70, 123]-coords), 2)))

# case 2
phi_A = -117
phi_B = 21
phi_C = 75
phi_D = 129
coords = localizer.search_four_localize(phi_A, phi_B, phi_C, phi_D)
print('2. Expected: [179, 168] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
print('Error: '+str(np.round(np.linalg.norm([179, 168]-coords), 2)))

# case 3
phi_A = -89
phi_B = -23
phi_C = 84
phi_D = -157
coords = localizer.search_four_localize(phi_A, phi_B, phi_C, phi_D)
print('3. Expected: [52, 61] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
print('Error: '+str(np.round(np.linalg.norm([52, 61]-coords), 2)))

# case 4
phi_A = 105
phi_B = -106
phi_C = -31
phi_D = 29
coords = localizer.search_four_localize(phi_A, phi_B, phi_C, phi_D)
print('4. Expected: [172, 100] Found: ['+str(round(coords[0], 2))+', '+str(round(coords[1], 2))+']')
print('Error: '+str(np.round(np.linalg.norm([172, 100]-coords), 2)))
