FROM ubuntu:18.04

LABEL vendor="Roboy" \
      maintainer="Vagram Airiian <vagram.airiian@tum.de>" \
      name="Rosemo" \
      version="0.5" \
      description="Funboy HRI ROS Emotion analyser"

RUN apt-get update && apt-get install -y python3.6 python3.6-dev python3-pip python3-virtualenv

## ROS
RUN echo "Installing ROS" && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic main restricted' >> /etc/apt/sources.list && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted' >> /etc/apt/sources.list && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic universe' >> /etc/apt/sources.list && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic-updates universe' >> /etc/apt/sources.list && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic multiverse' >> /etc/apt/sources.list && \
   echo 'deb-src http://archive.ubuntu.com/ubuntu/ bionic-updates multiverse' >> /etc/apt/sources.list && \
   apt-get update && apt-get install -y --no-install-recommends lsb-core -y && \
   sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
   apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
   apt update && \
   DEBIAN_FRONTEND=noninteractive apt install ros-melodic-desktop-full -y --no-install-recommends && \
   rosdep init && \
   rosdep update && \
   echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc && \
   echo "export ROS_MASTER_URI="http://127.0.0.1:11311/"" >> ~/.bashrc && \
   apt install python-rosinstall python-rosinstall-generator python-wstool build-essential -y --no-install-recommends

WORKDIR /

RUN mkdir -p catkin_ws/src && cd catkin_ws && \
  /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_make" && cd src && \
  git clone https://github.com/Roboy/roboy_communication.git && \
  git clone https://github.com/Roboy/pyroboy.git && \
  cd .. && \
  /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_make" && \
  echo "source /catkin_ws/devel/setup.bash" >> ~/.bashrc

## Dependencies
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
RUN apt install git-lfs
RUN git lfs install
RUN apt install -y alsa-base alsa-utils
RUN apt install -y portaudio19-dev python-pyaudio python3-pyaudio

RUN mkdir /rosemo
RUN mkdir /rosemo/data
RUN mkdir /rosemo/sdata
COPY ./ros /catkin_ws/src/rosemo

RUN cd /rosemo && git clone https://github.com/thoughtworksarts/EmoPy.git
COPY ./extras/setup.py /rosemo/EmoPy/setup.py
COPY ./extras/fermodel.py /rosemo/EmoPy/EmoPy/src/fermodel.py

ENV VIRTUAL_ENV=/rosemo/venv
RUN python3 -m virtualenv -p python3.6 /rosemo/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.txt /rosemo
RUN pip install -r /rosemo/requirements.txt
RUN pip install -e /rosemo/EmoPy

# Rebuild catkin
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd catkin_ws; catkin_make'

# CMD /bin/bash -i -c 'roslaunch rosemo rosemo.launch'
CMD tail -f /dev/null
