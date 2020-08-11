import cv2
import time
from ONVIFCameraControl import ONVIFCameraControl  # import ONVIFCameraControlError to catch errors
#stream_link = 'rtsp://admin:admin@192.168.1.23:554/cam/realmonitor?channel=1&subtype=0'
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
######################################################################################################################
class VideoStreamWidget(object):
    def __init__(self, CamIP='0',timeout = 40, VidAnal = 'Normal',preset = 'home'):
        # Create a VideoCapture object
        if (CamIP == '0'):
            self.CameraTitle = 'USB Camera'
            stream_link = 0
        else :
            mycam = ONVIFCameraControl((CamIP, 80), "admin", "admin")
            mycam.goto_preset(preset_token=preset)

            self.CameraTitle = 'IP Camera :' + CamIP
            stream_link = f'rtsp://admin:admin@{CamIP}:554/cam/realmonitor?channel=1&subtype=0'
        capture = cv2.VideoCapture(stream_link)
       # print('Bhaskar')
        #print(capture.isOpened())
        self.timeout = timeout
        self.stopFlag = False
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        print('Camera Streaming Widget')
        key = '1'
        WIDTH = 400
        HEIGHT= 300
        window_z = 'Normal'
        #if(capture.isOpened()):
        if(True):
            i = 0
            ret, face_frame = capture.read()
            while (t2 - t1) < self.timeout :
          #  while (True):
                # Capture frame-by-frame
                t2 = time.perf_counter()
                ret, frame = capture.read()
               # cv2.imshow(self.CameraTitle, frame)
                # Our operations on the frame come here
               # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               # if(VidAnal == 'Normal'):
                    # Display the resulting frame
               #     cv2.imshow(self.CameraTitle, frame)
                if(VidAnal == 'FaceDetect'):
                   # frame = cv2.resize(frame, (, 640))
                    # convert to gray scale of each frames
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # Detects faces of different sizes in the input image
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        # To draw a rectangle in a face
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (20,20)
                # fontScale
                fontScale = 0.4
                # Blue color in BGR
                color = (240, 0, 0)
                # Line thickness of 2 px
                thickness = 1
                # Using cv2.putText() method
                #text = 'Press q to quit, c to continue' + '(Timeout: {:.2f})'.format(40-(t2-t1)), org, font, fontScale, color, thickness, cv2.LINE_AA
                frame = cv2.putText(frame, 'Press q to quit, c to continue\n' + '(Timeout: {:.2f})'.format(40-(t2-t1)), org, font, fontScale, color, thickness, cv2.LINE_AA)
                #print(text)
                cv2.resizeWindow(self.CameraTitle, WIDTH, HEIGHT)
                cv2.namedWindow(self.CameraTitle, cv2.WINDOW_KEEPRATIO)

                cv2.imshow(self.CameraTitle, frame)
                key = cv2.waitKey(1) & 0xFF
               # if cv2.waitKey(1) & 0xFF == ord('q'):
                if(key == ord('q')) or (key == ord('Q')):
                    break
                elif(key == ord('c')) or (key == ord('C')):
                    t1 =  time.perf_counter()
                    t2 = t1
                    print('extended')
                elif(key == ord('f')) or (key == ord('F')):
                    VidAnal = 'FaceDetect'
                elif(key == ord('n')) or (key == ord('N')):
                    VidAnal = 'Normal'
                elif(key == ord('z')) or (key == ord('Z')):
                    WIDTH = 800
                    HEIGHT = 480
                elif (key == ord('u')) or (key == ord('U')):
                    WIDTH = 400
                    HEIGHT = 260
            # When everything done, release the capture
            capture.release()
            cv2.destroyAllWindows()
      #  else:
      #      print('Unable to open Camera Port')
######################################################################################################################
if __name__ == '__main__':
    timeout = 40
    VidAnal = 'Normal'
    VideoStreamWidget('192.168.1.23', timeout, VidAnal='Normal',preset='home')
   # print('Hello')
