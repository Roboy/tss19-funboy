#!/usr/bin/env python3

import wave
import rospy
import os

from time import time
from rosemo.msg import EmotionResult

from SpeechEmotionRecognition import SpeechEmotionRecognition

PATH = "/catkin_ws/src/rosemo/ros_models/audio.hdf5"


class RosemoAudioServer:

    def __init__(self, model_path, queue_size=10):
        self.pub = rospy.Publisher('rosemo_pub/speech', EmotionResult)
        self.path = '/rosemo/sdata/' + str(int(time()))
        os.mkdir(self.path)
        self.audio = []
        self.chunk_size = 2
        self.duration = 10
        self.offset = 0
        self.model = SpeechEmotionRecognition(model_path)
        self.labels = self.model._emotion.values()

    def get_emotion_from_speech(self):
        rec = f'{self.path}/voice_recording.wav'
        new_rec = f'{self.path}/voice_recording_temp.wav'
        sample_size, frames = SpeechEmotionRecognition.voice_recording(new_rec, duration=self.chunk_size)

        if self.offset > 0:
            # Export audio recording to wav format
            wf = wave.open(new_rec, 'w')
            wf.setnchannels(1)
            wf.setsampwidth(sample_size)
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()

            data = []
            for f in [rec, new_rec]:
                w = wave.open(f, 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()

            output = wave.open(rec, 'wb')
            output.setparams(data[0][0])
            output.writeframes(data[0][1])
            output.writeframes(data[1][1])
            output.close()
        else:
            # Export audio recording to wav format
            wf = wave.open(rec, 'w')
            wf.setnchannels(1)
            wf.setsampwidth(sample_size)
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()

        self.offset += 2

        if self.offset > self.duration + 5:
            emotions, timestamp = self.model.predict_emotion_from_file(rec, offset=self.offset, duration=self.duration)
            # Calculate emotion distribution
            emotion_dist = [int(100 * emotions.count(label) / len(emotions)) for label in self.labels]
            return emotion_dist
        else:
            print("Speech is not ready yet!")
            return None

    def run(self):
        rospy.init_node('rosemo_audio')
        rate = rospy.Rate(1)  # 1hz
        print("Ready: Rosemo Audio Server")
        while not rospy.is_shutdown():
            result = self.get_emotion_from_speech()
            if result is not None:
                rospy.loginfo(f'Result: {result}')
                self.pub.publish(EmotionResult(self.labels, result))
            rate.sleep()


if __name__ == "__main__":
    server = RosemoAudioServer(model_path=PATH)
    server.run()
