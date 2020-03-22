#!/bin/bash

mkdir /home/roboy/data
mkdir /home/roboy/sdata
docker build -t rosemo .
docker run --name rosemo -p "11311:11311" -p "33690:33690" -v /home/roboy/data:/rosemo/data -v /home/roboy/sdata:/rosemo/sdata -v /home/roboy/tss19-funboy/src/rosemo/ros:/catkin_ws/src/rosemo --device /dev/video0:/dev/video0 --device /dev/snd:/dev/snd -d rosemo

