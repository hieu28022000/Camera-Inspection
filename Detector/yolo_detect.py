import cv2
import numpy as np
import os
import random
import imutils
import time
import glob
import numba

from numba import jit, cuda 
from timeit import default_timer as timer  

class Yolo_detector:
    def __init__(self, class_name_path, cfg_path, model_path):
        # Class name
        classesFile = class_name_path
        self.classes = None
        with open(classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        # Load model
        self.net = cv2.dnn.readNet(model_path, cfg_path)
        # output_path = os.path.join("output", "data_33.jpg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        

    def predict_image(self, img):
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # font = cv2.FONT_HERSHEY_PLAIN
        # for i in range(len(boxes)):
        #     if i in indexes:
        #         x, y, w, h = boxes[i]
        #         label = str(self.classes[class_ids[i]])
        #         color = self.colors[class_ids[i]]
        #         cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        #         cv2.putText(img, label, (x, y-2), font, 1, color, 2)
        return boxes, class_ids

    def predict_videos(self, video_path):
        cap = cv2.VideoCapture(video_path)
        codec = cv2.VideoWriter_fourcc(*'XVID')
        ret, frame = cap.read()
        WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter("predict/demo.avi",codec,15,(WIDTH,HEIGHT))
        cap.release()
        cap = cv2.VideoCapture(video_path)
        while (True):
            ret, frame = cap.read() 
            height, width, channels = frame.shape
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            counts = 0
            outs = self.net.forward(self.output_layers)
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.8:
                        print(class_id)
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, label, (x, y-2), font, 1, color, 2)
            counts += 1
            # cv2.imshow('detection', frame)
            writer.write(frame)
        cap.release()
        out.release()
        cv2.destroyAllWindows()

