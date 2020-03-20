## Command Line Interface to access GPT-2 TLH Server

This command line 

### Installation
Install the necessary dependencies via pip:
 
```bash

pip install -r requirements.txt

```

### Running
First, you need to start GPT-2 TLH Server, then run:

```bash

python cmd_joke_interface.py

```

You should see this line in terminal:
```bash

Model prompt >>>

```
You can start typing.

### Trying
Try:

```bash

Model prompt >>> <|short|> <|chicken|>

```
If everything worked correctly, you will receive a similar result:
```bash

CLASS TOKENS: short, chicken | UTTERANCE:  |
RESPONSE: Why did the chicken cross the road? It was too chicken.

```