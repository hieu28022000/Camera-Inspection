import cv2
import numpy as np

class Color_check:
    def __init__(self, img):
        # img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.img = img

    def Color_check(self):
        # define green threshold
        lower_green = (38, 90, 30)
        upper_green = (70, 255,255)
        # If pixel in range of green threshold then this pixel = 1 and if not this pixel = 0
        mask_img = cv2.inRange (self.img, lower_green, upper_green)
        # convert img from HSV back to RGB
        self.img = cv2.cvtColor (self.img, cv2.COLOR_HSV2RGB)
        # bitwise the grayscale img and origin img to get mask of img
        result = cv2.bitwise_and(self.img, self.img, mask=mask_img)
        #self.visualize(result)
        return result

    def visualize(self, mask_img):
        cv2.imshow('img', mask_img)
        cv2.waitKey(0)
    
    def Process(self):
        mask_img = self.Color_check()
    
        X = []
        Y = []
        x_min = mask_img.shape[1]
        y_min = mask_img.shape[0]
        x_max = 0
        y_max = 0
        for y in range (mask_img.shape[0]):
            for x in range (mask_img.shape[1]):
                if ((mask_img[y][x][0],mask_img[y][x][1],mask_img[y][x][2]) != (0,0,0)):
                    X.append (x)
                    Y.append (y)
        for x in X:
            x_max = max(x, x_max)
            x_min = min(x, x_min)
        for y in Y:
            y_max = max(y, y_max)
            y_min = min(y, y_min)
        cropped_img = mask_img[y_min:y_max, x_min:x_max]
        
        count_green_pixel = 0
        count_notgreen_pixel = 0
        for i in range (cropped_img.shape[0]):
            for j in range (cropped_img.shape[1]):
                if ((cropped_img[i,j,0], cropped_img[i,j,1], cropped_img[i,j,2]) != (0,0,0)):
                    count_green_pixel += 1
        count_notgreen_pixel = (cropped_img.shape[0]*cropped_img.shape[1]) - count_green_pixel
        ratio = count_notgreen_pixel / count_green_pixel
        if (ratio > 0.2):
            return 0
        else:
            return 1



        

