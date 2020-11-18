"""
This is a proof of concept for the logic of the localization method.
"""

from scipy.linalg import solve # can prob use this from numpy
from scipy.spatial.distance import euclidean # can prob use this from numpy
import numpy as np
import matplotlib.pyplot as plt


class Location:
    """
    Class for different location related operations of the robot.
    The main functionality for now is localization.
    """

    def __init__(self, markers: list) -> None:
        """
        Markers is a list of coordinates for each perimeter marker
        """
        self.markers = markers
        # L_* are the lengths between markers
        self.L_ab = euclidean(markers[0], markers[1])
        self.L_bc = euclidean(markers[1], markers[2])
        self.L_ca = euclidean(markers[2], markers[0])
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
        b = np.array([self.A_a, self.A_b, self.A_c, 180-self.theta12, 180-self.theta23, 180-self.theta31])
        x = np.matmul(np.linalg.pinv(a), b)
        # hardcoded to use the AB line and marker A but any line/marker could be used
        # line/marker will have to be choosed dynamically if there are obstacles
        x = np.deg2rad(x)
        d = self.L_ab*((np.sin(x[2])*np.sin(x[1]))/np.sin(x[1]+x[2]))
        l = d/np.tan(x[1])
        rotation_matrix = np.array([[np.cos(np.deg2rad(self.A_a)), -1*np.sin(np.deg2rad(self.A_a))],
                                    [np.sin(np.deg2rad(self.A_a)), np.cos(np.deg2rad(self.A_a))]])
        coords = np.matmul([self.markers[0][0]-l, self.markers[0][1]+d], rotation_matrix)
        return coords

    def outside_localize(self) -> list:
        if self.theta12 > 180:
            pass
        elif self.theta23 > 180:
            pass
        elif self.theta31 > 180:
            pass
        else:
            print("error") # TODO: Make this a propper error being raised
        return


# MAIN PROGRAM
markers = np.array([[173, 109],
                    [97, 5],
                    [29, 109]])
localizer = Location(markers)
coords = localizer.localize(54, 153, -71)

x = [markers[0][0], markers[1][0], markers[2][0], coords[0]]
y = [markers[0][1], markers[1][1], markers[2][1], coords[1]]
plt.scatter(x, y)
plt.show()
