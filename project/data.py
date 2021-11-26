import numpy as np
import pandas as pd
import math
from settings import *


class Star:
    def __init__(self, phi, theta, brightness):
        self.phi = phi
        self.theta = theta
        self.brightness = brightness


def coord2angles(x, y, z):
    phi = np.arctan2(z, x)  # horizontal
    theta = np.arctan2(y, np.sqrt(x**2+z**2))  # vertical
    return phi, theta


def init():
    """инициализация модуля, загружает данные из файла с данными в глобальный массив stars"""

    global stars

    #data_frame = pd.read_csv(r"D:\ucheba\python\Sky_drip\project\hygdata_v3.csv")
    data_frame = pd.read_csv(__file__[:-7]+'hygdata_v3.csv')

    num_stars = len(data_frame)
    x = data_frame['x'].values
    y = data_frame['y'].values
    z = data_frame['z'].values
    phi, theta = coord2angles(x, y, z)
    mag = data_frame['mag'].values
    hundreds = np.array([100 for i in range(num_stars)])
    brightness = np.power(hundreds, mag / 5)

    #brightness = brightness * 255.0/(np.max(brightness) - np.min(brightness))
    scale = 255.0/np.mean(brightness)
    brightness = [min(255, i*scale) for i in brightness]

    stars = []

    for i in range(num_stars):
        stars.append(Star(phi[i], theta[i], brightness[i]))


def what_we_see(hor_angle, vert_angle, visual_field):
    global stars

    visible_stars = []

    for a_star in stars:
        if abs(a_star.phi - hor_angle) % np.pi <= visual_field / 2 and abs(a_star.theta - vert_angle) % np.pi   <= visual_field / 2:
            visible_star = Star((a_star.phi - hor_angle) % np.pi, (a_star.theta - vert_angle) % np.pi, a_star.brightness)

            visible_stars.append(visible_star)

    return visible_stars
