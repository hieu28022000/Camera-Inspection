import cv2
from Detector.yolo_detect import *
from Process.color_check import *
from datetime import date, datetime
import time
import argparse
from tkinter import *
import PIL.Image, PIL.ImageTk
import tkinter
import time
from threading import Thread


def get_day_time():
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return today, current_time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--video", type=bool, default=False)
    parser.add_argument("--video_path", type=str, default=None)
    parser.add_argument("--model_weigths", type=str, default="./Detector/model_weigths/yolov3_Box_last.weights")
    parser.add_argument("--config_model", type=str, default="./Detector/cfg/yolov3_Box.cfg")
    parser.add_argument("--output_path", type=str, default="./predict/")
    parser.add_argument("--yolo_config_classes", type=str, default="./Detector/cfg/obj.names")
    parser.add_argument("--img_path", type=str, default=None)
    parser.add_argument("--visualize", type=bool, default=False)
    return parser.parse_args()


class bottle_cap_check: 
    def __init__(self, parser): 
        self.parser = parser
        self.Yolo = Yolo_detector(self.parser.yolo_config_classes, self.parser.config_model, self.parser.model_weigths)
        print (self.parser)
    
    def process_image(self, ori_img = None):
        # if (self.parser.video == False):
        #     ori_img = cv2.imread(self.parser.img_path)
        img = cv2.resize(ori_img, (ori_img.shape[1]//3, ori_img.shape[0]//3))
        boxes, class_ids = self.Yolo.predict_image(img)
        Not_good = 0
        Blank = np.ones((img.shape[0],400,3), np.uint8)*255
        Blank_to_save = Blank.copy()
        img_to_save = img.copy()
        print (boxes)
        print (class_ids)
        if (6 in class_ids):
            Not_good = 1
            cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
            day, time = get_day_time()
        else:
            for i in range (len(boxes)):
                if (2 in class_ids and 3 in class_ids):
                    if (class_ids[i] == 3):
                        process_img = img[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0]: boxes[i][0] + boxes[i][2]]
                        color_check = Color_check(process_img)
                        check = color_check.Process()
                        if (check == 0):
                            Not_good = 1
                            cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                            day, time = get_day_time()
                        else:
                            cv2.putText(Blank, 'Status: OK', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                else:
                    Not_good = 1
                    cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                    day, time = get_day_time()
        result = np.concatenate((img,Blank),axis=1)
        return result
  
    def process_video (self):
        cap = cv2.VideoCapture(self.parser.video_path)
        codec = cv2.VideoWriter_fourcc(*'XVID')
        ret, frame = cap.read()
        WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if (self.parser.output_path != None):
            writer = cv2.VideoWriter(self.parser.output_path + "output.avi",codec,15,(WIDTH,HEIGHT))
        cap.release()
        cap = cv2.VideoCapture(self.parser.video_path)
        while True: 
            if frame is None:
                break
            _, frame = cap.read()
            result_frame = self.process_image(frame)
            if self.parser.visualize == True: 
                cv2.imshow('video', result_frame)
            if self.parser.output_path != None: 
                writer.write(result_frame)
        cv2.waitKey(0)    
        cap.release()
        cv2.destroyAllWindows()


def return_img(frame): 
    frame = frame
    thread = Thread(target = solve.process_image)
    thread.start()
    image = solve.process_image(frame)
    image = cv2.resize(image, (1000,500))
    return image

def process():
    global parser, solve, btnprocess, photo, T_F
    print (btnprocess)
    btnprocess = 1 - btnprocess
    # thuwr nghiem
    img1 = cv2.imread('data/data_0.jpeg')
    img2 = cv2.imread('data/data_22.jpeg')
    img = []
    img.append (img1)
    img.append(img2)
    i = 0
    j = -1
    # -------- 
    if (btnprocess == 1):
        prev_sensor = - 1
        cur_sensor = - 1
        # video = cv2.VideoCapture(0)
        cap = cv2.VideoCapture('data\\Wisenet WEBVIEWER - Internet Explorer 2020-10-27 14-40-48.mp4')
        while i < len(T_F):
            ret, frame = cap.read()
            # hàm tins hiệu trả về
            cur_sensor = T_F[i]
            print ("cur", cur_sensor)
            print ("prev",prev_sensor)
            if (prev_sensor == 0 and cur_sensor == 1):
                # ret, frame = cap.read()
                # frame = frame
                # thread = Thread(target = solve.process_image)
                # thread.start()
                # image = solve.process_image(frame)
                # image = cv2.resize(image, (1000,500))
                image = return_img(frame)
                # photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
                # canvas.create_image (0, 0, image = photo, anchor = tkinter.NW)
                # cap.release()
                # cv2.destroyAllWindows()
                photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
                canvas.create_image (0, 0, image = photo, anchor = tkinter.NW)
                canvas.update()
                # cv2.destroyAllWindows()
          
            prev_sensor = cur_sensor
            i += 1

 
if __name__ == "__main__":
    
    parser = parse_args()
    solve = bottle_cap_check(parser)
    T_F = [False,False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
    
    #draw UI
    window = Tk()
    window.title ("Bottle Cap Inspection")
    btnprocess = 0
    btn = Button (window, text = "Process", command = process)
    btn.pack()
    photo = None
    canvas = Canvas(window, height = 500, width = 1000)
    canvas.pack()  
    window.mainloop() 
    # ----------------------------------- #

            





    # # write log
    # if not os.path.exists ("logs"):
    #     os.makedirs('logs')
    # # write 
    # # write time not good
    # h = open('logs/NG_times.txt', 'r+', encoding = 'utf-8')
    # a = h.read()
    # a = a.split('\n')
    # try:
    #     a.remove('')
    # except:
    #     pass
    # NG_times = int (a[len(a) - 1])
    # if (Not_good == 1):
    #     NG_times += 1
    #     h.write('{} {}'.format(str(NG_times), '\n'))
    #     h.close()
    # cv2.putText(Blank, 'Not good times: ' + str(NG_times), (Blank.shape[0]//8, Blank.shape[1]//2), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)


    # # write time OK
    # g = open('logs/Ok_times.txt', 'r+', encoding = 'utf-8')
    # a = g.read()
    # a = a.split('\n')
    # try:
    #     a.remove('')
    # except:
    #     pass
    # Ok_times = int (a[len(a) - 1])
    # if (Not_good == 0):
    #     Ok_times += 1
    #     g.write('{} {}'.format(str(Ok_times), '\n'))
    #     g.close()
    # cv2.putText(Blank, 'Good times: ' + str(Ok_times), (Blank.shape[0]//8, Blank.shape[1]//3), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)

    # # write time iterations
    # f = open('logs/test_times.txt', 'r+', encoding = 'utf-8')
    # a = f.read()
    # a = a.split('\n')
    # try:
    #     a.remove('')
    # except:
    #     pass
    # times = int (a[len(a) - 1])
    # times += 1
    # cv2.putText(Blank, 'Times: ' + str(times), (Blank.shape[0]//8, Blank.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
    # f.write('{} {}'.format(str(times), '\n'))
    # f.close()

    # # write image if they art Not good image
    # if not os.path.exists ("Notgood_information"):
    #     os.makedirs('Notgood_information')
    # if (Not_good == 1):
    #     cv2.putText(Blank_to_save, 'Date: ' + str(day), (Blank.shape[0]//8, Blank.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
    #     cv2.putText(Blank_to_save, 'Time: ' + str(time), (Blank.shape[0]//8, Blank.shape[1]//3), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
    #     cv2.putText(Blank_to_save, 'Times: ' + str(times), (Blank.shape[0]//8, Blank.shape[1]//2), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
    #     img_to_save = cv2.hconcat([img, Blank_to_save])
    #     cv2.imwrite('Notgood_information/Notgood' + str(times) + '.png', img_to_save)
    # img = cv2.hconcat([img, Blank])
    # cv2.imshow('img', img)
    # cv2.waitKey()

