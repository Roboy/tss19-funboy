#!/usr/bin/env python3

import rospy
import cv2
import os

from time import time
from rosemo.msg import EmotionResult
from EmoPy.src.fermodel import FERModel

LABELS = ['calm', 'anger', 'happiness', 'surprise', 'disgust', 'fear', 'sadness']
PATH = '/catkin_ws/src/rosemo/ros_models/haarcascade_frontalface_default.xml'


class RosemoVideoServer:

    def __init__(self, labels, queue_size=10):
        self.labels = labels
        self.pub = rospy.Publisher('rosemo_pub/video', EmotionResult)
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.camera.set(cv2.CAP_PROP_FPS, 24)
        self.path = '/rosemo/data/' + str(int(time()))
        os.mkdir(self.path)
        self.model = FERModel(self.labels, verbose=True)
        self.face_detector = cv2.CascadeClassifier(PATH)

    def capture_image(self, camera, file, face_file):
        face = None
        if camera.isOpened():
            ret = False
            print("Capturing image ...")

            counter = 0
            max_tries = 100
            while not ret and camera.isOpened():
                counter += 1
                if counter >= max_tries:
                    return None
                # Capture frame-by-frame
                ret, frame = camera.read()
            # Save the captured frame on disk
            frame = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
            cv2.imwrite(file, frame)
            # Detect the face and crop it
            faces = self.face_detector.detectMultiScale(frame, 1.25, 6)
            for f in faces:
                # Define the region in the image
                x, y, w, h = [v for v in f]
                face = frame[y:y + h, x:x + w]
                cv2.imwrite(face_file, face)
            print("Face written to: ", face_file)
        else:
            print("Cannot access the webcam")

        return face

    def get_emotion_from_camera(self):
        file_name = str(time())
        file = f'{self.path}/{file_name}.jpg'
        face_file = f'{self.path}/{file_name}_face.jpg'
        face = self.capture_image(self.camera, file, face_file)

        if face is not None:
            # Can choose other target emotions from the emotion subset defined in
            # fermodel.py in src directory. The function
            # defined as `def _check_emotion_set_is_supported(self):`
            result = self.model.predict(face_file)
            with open(f'{self.path}/{file_name}.txt', 'w') as f:
                f.write(f"{str(self.labels)}\n{str(result)}")
            return result
        else:
            print("Face could not be detected")
            return None

    def run(self):
        rospy.init_node('rosemo_video')
        rate = rospy.Rate(2)  # 2hz
        print("Ready: Rosemo Video Server")
        while not rospy.is_shutdown():
            result = self.get_emotion_from_camera()
            if result is not None:
                rospy.loginfo(f'Result: {result}')
                self.pub.publish(EmotionResult(self.labels, result))
            rate.sleep()
        self.camera.release()


if __name__ == "__main__":
    server = RosemoVideoServer(labels=LABELS)
    server.run()
