import zeep
import os
import logging

from os import path
from camera import CameraOnvifConnection, CameraRtspWindow
from workers import FaceDetectionWorker
from utils import Resources
from dotenv import load_dotenv

load_dotenv()

# Monkey patch for bug with GetProfiles method
def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue


def main():
    logging.info('Connecting to camera')

    camera = CameraOnvifConnection(
        os.getenv("CAMERA_HOST"),
        os.getenv("CAMERA_PORT"),
        os.getenv("CAMERA_USERNAME"),
        os.getenv("CAMERA_PASSWORD"),
        Resources.wsdl_dir()
    )

    logging.info('Connection established')

    rtsp_url = camera.get_rtsp_url(profile_number=1)

    logging.info('Connecting to rtsp by url {}'.format(rtsp_url))

    worker = FaceDetectionWorker(
        Resources.haarcascade('haarcascade_frontalface_default.xml')
    )

    window = CameraRtspWindow(rtsp_url)

    window.loop(worker)

    window.destroy()

    logging.info('Program closed correctly')


if __name__ == '__main__':
    main()
