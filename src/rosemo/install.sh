#!/bin/bash

mkdir /home/wagram/data
mkdir /home/wagram/sdata
docker build -t rosemo .
docker run --name rosemo -p "11311:11311" -p "33690:33690" -v /home/wagram/data:/rosemo/data -v /home/wagram/sdata:/rosemo/sdata -v /home/wagram/tss19-funboy/src/rosemo/ros:/catkin_ws/src/rosemo --device /dev/video0:/dev/video0 --device /dev/snd:/dev/snd -d rosemo

