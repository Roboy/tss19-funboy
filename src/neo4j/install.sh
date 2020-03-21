#!/bin/bash

mkdir /home/roboy/tss19-funboy/db
mkdir /home/roboy/tss19-funboy/db/data
mkdir /home/roboy/tss19-funboy/db/logs
docker pull neo4j:3.5
docker build -t funboyn4j .
docker run --name funboyn4j -p "7474:7474" -p "7687:7687" -v /home/roboy/tss19-funboy/db/data:/data -v /home/roboy/tss19-funboy/db/logs:/logs -d funboyn4j

