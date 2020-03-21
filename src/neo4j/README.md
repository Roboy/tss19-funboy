# Neo4j Docker Instance

Contains a supplementary script to deploy a Neo4j Docker instance.

## Installation 

Install Docker >= 19.03.

In the install.sh edit the locations for volume links where to store data and log files:
* /your_location:/data
* /your_location:/logs

Then, run the install.sh script:
```bash

./install.sh

```

The script will automatically build a Docker instance containing Neo4j 3.5 graph database.

It will expose ports:
* 7474
* 7687
for web-interface and the Bolt protocol.

## Running

The installation script will automatically run the instance when it is built.

To stop the instance, run:
```bash
docker stop funboyn4j

```

To start the instance again, execute:
```bash
docker start funboyn4j

```
