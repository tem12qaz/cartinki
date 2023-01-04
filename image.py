import numpy as np
import cv2

colors_hex = ('#000000', '#18212A', '#262D33', '#767F84', '#FFFFFF')
colors_10_ = (
    (0, 0, 0), (15, 15, 15), (30, 30, 30), (45, 45, 45), (60, 60, 60),
    (75, 75, 75), (90, 90, 90), (105, 105, 105), (120, 120, 120), (135, 135, 135),
    (150, 150, 150), (165, 165, 165), (180, 180, 180), (195, 195, 195), (210, 210, 210),
    (225, 225, 225), (240, 240, 240), (255, 255, 255)
)
colors_10 = [np.array(color) for color in colors_10_]

gradient = ' .:!/r(l1Z4H9W8$@'
NEWLINE = '''
'''


class Image:
    def __init__(self, path: str, contrast: int = 1, brightness: int = 1, gamma: float = 1.0):
        self.original = cv2.imread(path, 1)
        self.adjust_gamma(gamma)
        # kernel = np.array([[-1, -1, -1], [-1, 8.9, -1], [-1, -1, -1]])
        # self.original = cv2.filter2D(self.original, -1, kernel)
        self.original = self.original * (contrast / 127 + 1)+ brightness - contrast
        # self.original = self.original * (contrast / 127 + 1) - contrast + brightness
        self.bw_scaled = None
        self.width = None
        self.height = None
        self.output = ''

    def adjust_gamma(self, gamma=1.0):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        self.original = cv2.LUT(self.original, table)

    def scale_and_bw(self, height: int = 72,  width: int = 72):
        # cv2.imshow('Original', self.img)
        img_stretch = cv2.resize(self.original, (height, width))
        cv2.imwrite('2.jpg', img_stretch)
        self.bw_scaled = img_stretch
        self.width = width
        self.height = height

    def apply_colors(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.color_distance(self.bw_scaled[x, y])
                print(color)
                # self.bw_scaled[x,y] = color
                print(x)
                self.output += color

            self.output += NEWLINE

        # cv2.imwrite('3.jpg', self.bw_scaled)
        return self.output

    def color_distance(self, pixel):
        pixel = np.array((pixel, pixel, pixel))
        distances = []
        for color in colors_10:
            square = np.square(pixel - color)
            sum_square = np.sum(square)
            distances.append(np.sqrt(sum_square))

        return gradient[distances.index(min(distances))]

