import zeep
import cv2
import os
import logging

from os import path
from dotenv import load_dotenv
from onvif import ONVIFCamera, ONVIFService, ONVIFError

load_dotenv()

# Monkey patch for bug with GetProfiles method
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

# Getting path to rtsp stream
logging.info(u'Connecting to the camera')

mycam = ONVIFCamera(
    host = os.getenv("CAMERA_HOST"), 
    port = os.getenv("CAMERA_PORT"), 
    user = os.getenv("CAMERA_USERNAME"), 
    passwd = os.getenv("CAMERA_PASSWORD")
)

logging.info(u'Connecting established successfully')

logging.info(u'Finding the rtsp stream url')

media_service = mycam.create_media_service()

profiles = media_service.GetProfiles()

token = profiles[1].token

url_info = media_service.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'UDP'},'ProfileToken':token})

url = url_info.Uri

logging.info('Connecting to rtsp by url {}'.format(url))

# Initializing OpenCV and drawing a rectangle at face
cap = cv2.VideoCapture(url)

faceCascade = cv2.CascadeClassifier(path.join(path.dirname(path.realpath(__file__)), 'haarcascade_frontalface_default.xml'))

dirname = path.join(path.dirname(path.realpath(__file__)), 'frames')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

logging.info('Program closed correctly')

cap.release()
cv2.destroyAllWindows()