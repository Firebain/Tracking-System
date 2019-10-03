import zeep
import cv2
import os

from os import path
from dotenv import load_dotenv
from onvif import ONVIFCamera, ONVIFService

load_dotenv()

# Monkey patch for bug with GetProfiles method
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

# Getting path to rtsp stream 
mycam = ONVIFCamera(
    host = os.getenv("CAMERA_HOST"), 
    port = os.getenv("CAMERA_PORT"), 
    user = os.getenv("CAMERA_USERNAME"), 
    passwd = os.getenv("CAMERA_PASSWORD")
)

media_service = mycam.create_media_service()

profiles = media_service.GetProfiles()

token = profiles[1].token

url_info = media_service.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'UDP'},'ProfileToken':token})

url = url_info.Uri

# Initializing OpenCV and saving frames to directory
cap = cv2.VideoCapture(url)

dirname = path.join(path.dirname(path.realpath(__file__)), 'frames')

count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    else:
        cv2.imshow('frame', frame)
        name = "rec_frame"+str(count)+".jpg"

        cv2.imwrite(path.join(dirname, name), frame)

        count += 1
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()