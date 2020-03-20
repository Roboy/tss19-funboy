# GPT-2 TLH Server

GPT-2 TLH (Transfer Learning for Humour) is a pre-trained GPT-2-L model finetuned on humour data

The server runs this model for inference over http. It requires Python 3.6 and Tensorflow-gpu 1.15.2.

### Installation
Install the necessary dependencies via pip:
 
```bash

pip install -r requirements.txt

```

### Running
 
To start the server for joke generation, execute:

```bash

python -c "import server; server.run()"

```
By default, the server uses port 5050 on localhost which may cause a port conflict with Yahoo Messenger.
