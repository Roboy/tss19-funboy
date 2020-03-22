# Rosemo: ROS Emotion Recognition

This module contains ROS topics for audio and video emotion recognition results.

## Installation

Install Docker >= 19.03.

In the install.sh edit the locations for volume links where to store data and log files:
* /your_location:/rosemo/data - for image data
* /your_location:/rosemo/sdata - for speech data

Then, run the install.sh script:
```bash

./install.sh

```

The script will automatically build a Docker instance containing ROS 1 Melodic and Ubuntu 18.04.

It will expose ports:
* 11311
* 33690
for ROS functionality.

The container needs access to video and audio recording devices:
* /dev/video0:/dev/video0 - for video
* /dev/snd:/dev/snd - for audio

## Running

The installation script will automatically run the container when it is built.

To stop the container, run:
```bash
docker stop rosemo

```

To start the container again, execute:
```bash
docker start rosemo

```

Enter a running container and start roscore:
```bash
roscore

```

Then, you can start video:
```bash
rosrun rosemo rosemo_video.py

```
and audio emotion recognition scripts:
```bash
rosrun rosemo rosemo_audio.py

```

They will publish to topics:
* rosemo/video
* rosemo/audio

respectively, using EmotionResult message:
* string[] labels
* float64[] scores


