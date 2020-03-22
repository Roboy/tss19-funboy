import wave

from ros.scripts.SpeechEmotionRecognition import SpeechEmotionRecognition

rec = f'voice_recording.wav'
new_rec = f'voice_recording_temp.wav'
sample_size, frames = SpeechEmotionRecognition.voice_recording(new_rec, duration=1)

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
