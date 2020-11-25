"""
This is a proof of concept for the logic of the localization method.
"""

import numpy as np
import matplotlib.pyplot as plt


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
        self.L_ab = np.linalg.norm(markers[0]-markers[1])
        self.L_bc = np.linalg.norm(markers[1]-markers[2])
        self.L_ca = np.linalg.norm(markers[2]-markers[0])
        # A_* are the angles of the triangle formed by markers
        self.A_a = np.rad2deg(np.arccos(np.dot(markers[1]-markers[0], markers[2]-markers[0])/(self.L_ab*self.L_ca)))
        self.A_b = np.rad2deg(np.arccos(np.dot(markers[0]-markers[1], markers[2]-markers[1])/(self.L_ab*self.L_bc)))
        self.A_c = np.rad2deg(np.arccos(np.dot(markers[0]-markers[2], markers[1]-markers[2])/(self.L_ca*self.L_bc)))
        return

    def compute_thetas(self, phi1, phi2, phi3) -> None:
        """
        phi1, phi2, phi3, are the angles to known markers 1, 2, and 3.
        The robot will start from straight ahead and look
        in a clockwise direction for 180 degrees. Then it will move
        counterclockwise to the front position and then look 180 degrees ccw
        from start. Cw anges will be positive and ccw angles will be negative.
        """

        # convert all angles to cw
        if phi1 < 0:
            phi1 = 360 + phi1
        if phi2 < 0:
            phi2 = 360 + phi2
        if phi3 < 0:
            phi3 = 360 + phi3

        # calculate the theta angles
        # split into cases base on robot orientation
        if phi1 < phi2 and phi2 < phi3:
            # pointing between 3 and 1
            self.theta12 = phi2 - phi1
            self.theta23 = phi3 - phi2
            self.theta31 = 360 - phi3 + phi1
        elif phi2 < phi3 and phi3 < phi1:
            # pointing betwwen 1 and 2
            self.theta12 = 360 - phi1 + phi2
            self.theta23 = phi3 - phi2
            self.theta31 = phi1 - phi3
        elif phi3 < phi1 and phi1 < phi2:
            # pointing between 2 and 3
            self.theta12 = phi2 - phi1
            self.theta23 = 360 - phi2 + phi3
            self.theta31 = phi1 - phi3
        else:
            print("You forgot a case")

        return

    def is_inside(self) -> bool:
        """
        Returns True if robot is inside triangle and False if robot is outside
        the triangle or markers
        """
        if self.theta12 > 180 or self.theta23 > 180 or self.theta31 > 180:
            return False
        else:
            return True

    def localize(self, phi1, phi2, phi3) -> list:
        """
        Wrapper to choose the correct localization function (inside or outside)
        """
        self.compute_thetas(phi1, phi2, phi3)
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
        a = np.array([[1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 1, 0, 0],
                      [0, 0, 0, 0, 1, 1],
                      [1, 0, 0, 0, 0, 1],
                      [0, 1, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0]])
        b = np.array([self.A_a, self.A_b, self.A_c, 180-self.theta31, 180-self.theta12, 180-self.theta23])
        x = np.matmul(np.linalg.pinv(a), b)
        # hardcoded to use the AB line and marker A but any line/marker could be used
        # line/marker will have to be choosed dynamically if there are obstacles
        x = np.deg2rad(x)
        d = self.L_ab*((np.sin(x[2])*np.sin(x[1]))/np.sin(x[1]+x[2]))
        l = d/np.tan(x[1])
        rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_a)), -1*np.sin(np.deg2rad(self.A_a))],
                                    [np.sin(np.deg2rad(self.A_a)), np.cos(np.deg2rad(self.A_a))]])
        coords_vec = np.matmul(rotation_matrix, [-l, d])
        coords = markers[0]+coords_vec
        return coords

    def outside_localize(self) -> list:
        if self.theta12 > 180:
            a = np.array([[0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 1, 1, 1],
                          [0, 0, 1, 1, 1, 0],
                          [1, 1, 0, 0, 0, 1],
                          [0, 1, 1, 0, 0, 0],
                          [1, 0, 0, 1, 1, 1]])
            b = np.array([self.A_c,
                          360-self.theta23-self.theta31,
                          180-self.theta23,
                          180-self.theta31,
                          180-self.theta23-self.theta31,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker A, non-trivial to use marker B
            d = self.L_ab*((np.sin(x[2])*np.sin(x[1]))/np.sin(x[1]+x[2]))
            l = d/np.tan(x[1])
            rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_a)), -1*np.sin(np.deg2rad(self.A_a))],
                                        [np.sin(np.deg2rad(self.A_a)), np.cos(np.deg2rad(self.A_a))]])
            coords_vec = np.matmul(rotation_matrix, [-l, -d])
            coords = markers[0]+coords_vec
            return coords
        elif self.theta23 > 180:
            a = np.array([[1, 1, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 1, 1],
                          [0, 1, 1, 1, 0, 0],
                          [0, 0, 0, 1, 1, 0],
                          [1, 1, 1, 0, 0, 1]])
            b = np.array([self.A_a,
                          360-self.theta12-self.theta31,
                          180-self.theta31,
                          180-self.theta12,
                          180-self.theta12-self.theta31,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker C, non-trivial to use marker B
            d = self.L_ab*((np.sin(x[3])*np.sin(x[4]))/np.sin(x[4]+x[3]))
            l = d/np.tan(x[4])
            rotation_matrix = np.array([[np.cos(np.deg2rad(-self.A_c)), -1*np.sin(np.deg2rad(-self.A_c))],
                                        [np.sin(np.deg2rad(-self.A_c)), np.cos(np.deg2rad(-self.A_c))]])
            coords_vec = np.matmul(rotation_matrix, [l, -d])
            coords = markers[2]+coords_vec
            return coords
        elif self.theta31 > 180:
            a = np.array([[0, 0, 1, 1, 0, 0],
                          [1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1],
                          [1, 0, 0, 0, 0, 1],
                          [0, 1, 1, 1, 1, 0]])
            b = np.array([self.A_b,
                          360-self.theta12-self.theta23,
                          180-self.theta12,
                          180-self.theta23,
                          180-self.theta12-self.theta23,
                          180])
            x = np.matmul(np.linalg.pinv(a), b)
            x = np.deg2rad(x)
            # hardcoded to use marker A, could also use marker C
            d = self.L_ab*((np.sin(x[5])*np.sin(x[0]))/np.sin(x[0]+x[5]))
            l = d/np.tan(x[0])
            # rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_a)), -1*np.sin(np.deg2rad(self.A_a))],
            #                             [np.sin(np.deg2rad(self.A_a)), np.cos(np.deg2rad(self.A_a))]])
            # coords_vec = np.matmul(rotation_matrix, [-l, d])
            coords_vec = [-l, d]
            coords = markers[0]+coords_vec
            return coords
        else:
            print("error")  # TODO: Make this a propper error being raised
        return


# MAIN PROGRAM
markers = np.array([[173, 109],
                    [97, 5],
                    [29, 109]])
localizer = Location(markers)

# case 1
phi1 = 54
phi2 = 153
phi3 = -71
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [83, 74] Found: '+str(coords))

# x = [markers[0][0], markers[1][0], markers[2][0], coords[0]]
# y = [markers[0][1], markers[1][1], markers[2][1], coords[1]]
# plt.scatter(x, y)
# plt.show()

# case 2
phi1 = -54
phi2 = -148
phi3 = 110
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [115, 44] Found: '+str(coords))

# case 3
phi1 = 155
phi2 = 13
phi3 = -70
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [126, 88] Found: '+str(coords))

# case 4
phi1 = -81
phi2 = -148
phi3 = 159
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [169, 42] Found: '+str(coords))

# case 5
phi1 = 15
phi2 = -15
phi3 = -63
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [192, 97] Found: '+str(coords))

# case 6
phi1 = 125
phi2 = 42
phi3 = -35
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [131, 35] Found: '+str(coords))

# case 7
phi1 = -30
phi2 = -100
phi3 = 29
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [54, 23] Found: '+str(coords))

# case 8
phi1 = 137
phi2 = 55
phi3 = -161
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [34, 71] Found: '+str(coords))

# case 9
phi1 = 52
phi2 = 102
phi3 = -11
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [38, 23] Found: '+str(coords))

# case 10
phi1 = -35
phi2 = 32
phi3 = 96
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [98, 142] Found: '+str(coords))

# case 11
phi1 = 128
phi2 = -79
phi3 = -164
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [63, 122] Found: '+str(coords))

# case 11
phi1 = -141
phi2 = -43
phi3 = 19
coords = localizer.localize(phi1, phi2, phi3)
print('Expected: [147, 117] Found: '+str(coords))
