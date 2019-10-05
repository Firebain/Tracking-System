import cv2

from workers import Worker


class CameraRtspWindow(object):
    def __init__(self, url):
        self.destroyed = False
        self.__cap = cv2.VideoCapture(url)

    def loop(self, worker: Worker):
        while self.__cap.isOpened():
            ret, frame = self.__cap.read()

            if not ret:
                break
            else:
                frame = worker.process(frame)

                cv2.imshow('frame', frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    def destroy(self):
        self.__cap.release()
        cv2.destroyAllWindows()

        self.destroyed = True

    def __del__(self):
        if not self.destroyed:
            self.destroy()
