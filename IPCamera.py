import cv2
import time

#stream_link = 'rtsp://admin:admin@192.168.1.23:554/cam/realmonitor?channel=1&subtype=0'
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
######################################################################################################################
class VideoStreamWidget(object):
    def __init__(self, CamIP='0',timeout = 40, VidAnal = 'Normal'):
        # Create a VideoCapture object
        if (CamIP == '0'):
            self.CameraTitle = 'USB Camera'
            stream_link = 0
        else :
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
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                org = (50,20)
                # fontScale
                fontScale = 0.6
                # Blue color in BGR
                color = (0, 0, 250)
                # Line thickness of 2 px
                thickness = 2
                # Using cv2.putText() method
                frame = cv2.putText(frame, 'Press q to quit, c to continue ' + '(Timeout: {:.2f})'.format(40-(t2-t1)), org, font, fontScale, color, thickness, cv2.LINE_AA)
                cv2.imshow(self.CameraTitle, frame)

                key = cv2.waitKey(1) & 0xFF
               # if cv2.waitKey(1) & 0xFF == ord('q'):
                if(key == ord('q')):
                    break
                elif(key == ord('c')):
                    t1 =  time.perf_counter()
                    t2 = t1
                    print('extended')
            # When everything done, release the capture
            capture.release()
            cv2.destroyAllWindows()
      #  else:
      #      print('Unable to open Camera Port')
######################################################################################################################
if __name__ == '__main__':
    timeout = 40
    VidAnal = 'Normal'
    VideoStreamWidget('192.168.1.23', timeout, VidAnal)
   # print('Hello')