avi_tsuyang='.\\avi_tsuyang.mp4'
avi_trump='.\\trump.mp4'
avi_mine='.\\mine.mp4'
#/render_thread
import cv2
import sys
'''
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
'''
#from action_classifier import ActionClassifier
from action_classifier_mobile import ActionClassifier

import time

class RenderThread():
    status = None
    exitFlag = False
    #action_classifier = ActionClassifier(model_path='weights/i3d_rgb_multi_class_new.pth')
    #action_classifier = ActionClassifier(model_path='weights/i3d_rgb_multi_class.pth')
    action_classifier = ActionClassifier(model_path='weights\\mobilenet_v3-173-best.pth')

    #changePixmap = pyqtSignal(QImage)
    
    #action_result = pyqtSignal(str)
    #avi=avi_tsuyang#얼굴만지는게 없어
    
    def run(self):
        cap = cv2.VideoCapture(avi_tsuyang)########
        cnt=0
        while cap.isOpened():
            cnt+=1
            ret, frame = cap.read()
            print('프레임리턴',ret)
            self.status=False
            if ret:
                rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_img = cv2.resize(rgb_img, (480,320))
                h, w, ch = rgb_img.shape
                print('상태?',self.status)
                if self.status is False:
                    result,a = self.action_classifier.run(rgb_img)
                    print('결과',result)
                    #self.action_result.emit(result)

            bytesPerLine = ch * w
            #convertToQtFormat = QImage(rgb_img.data, w, h, bytesPerLine, QImage.Format_RGB888)
            #p = convertToQtFormat.scaled(480,320, Qt.KeepAspectRatio)
            #self.changePixmap.emit(p)
            if self.exitFlag is True:
                print('언제 엑싵이지')
                break
            #여기서 영상 저장하는거로 바꾸기..프레임에 표시해서 저장하는 것도 괜찮을 듯
            
            print('타입과 쉐입',type(frame),frame.shape)
            if result  == '얼굴을 만지지 마세요 !':
                cv2.putText(frame, a, (350,300), cv2.FONT_HERSHEY_COMPLEX, 4, (0,255,0),thickness=3)
            winname='test'
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 0, 0)
            cv2.imshow(winname,frame)
            cv2.waitKey(50)
            cv2.imwrite('.\\frames_tsuyang\\frame_tsuyang_%d.jpg' %cnt,frame)
            result=''

            
    
    def setStatus(self, status):
        self.status = status
        print('상태',self.status)
    def get_action_result(self):
        print('action_result',self.action_result)
        return self.action_result
    
    def exit(self, bool_flag):
        self.exitFlag = True