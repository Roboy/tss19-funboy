## GPT-2 TLH Server

GPT-2 TLH (Transfer Learning for Humour) is a pre-trained GPT-2-L model finetuned on humour data

The server runs this model for inference over http. It requires Python 3.6 and Tensorflow-gpu 1.15.2.


### Running
 
To start the server for joke generation, execute:

```bash

python -c "import server; server.run()"

```
