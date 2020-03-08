import re
import random
import logging
import os
from typing import List

from .comedian import Comedian

logger = logging.getLogger(__name__)

import numpy as np
import tensorflow as tf

from .sample import *
from .encoder import *

MODEL='774A'
SEED=None
NSAMPLES=1
BATCH=1
LENGTH=35
TEMPERATURE=0.9
TOP_K=40
TOP_P=0.9
PATH=f'{os.path.dirname(__file__)}/models'


class DeepComedian(Comedian):

    def __init__(self, model_name=MODEL, path=PATH):
        self.types = {
            "chicken":"<|chicken|>",
            "momma": "<|momma|>",
            "jew":f"<|jew|>",
            "trump": f"<|trump|>",
            "nazi": f"<|nazi|>",
            "pet": f"<|pet|>",
            "army": f"<|army|>",
            "police": f"<|police|>",
            "religion": f"<|religion|>",
            "bar": f"<|bar|>",
            "clown": f"<|clown|>",
            "german": f"<|german|>",
            "queer": f"<|queer|>",
            "boss": f"<|boss|>",
            "doctor": f"<|doctor|>",
            "british": f"<|british|>",
            "cookie": f"<|cookie|>",
            "family": f"<|family|>",
            "friend": f"<|friend|>",
            "dadjokes": f"<|dadjokes|>",
            "other": f"<|other|>"
        }
        self.nsamples = 35
        self.batch_size = 1
        self.path = path
        self.model_name = model_name
        self.encoder = get_encoder(model_name)
        self.session, self.output, self.context = self.interactive_model()

    def interactive_model(self, seed=None, nsamples=35, length=1, temperature=1, top_k=40, top_p=0.9):
        """
        Interactively run the model
        :seed=None : Integer seed for random number generators, fix seed to reproduce
         results
        :nsamples=1 : Number of samples to return total
        :length=None : Number of tokens in generated text, if None (default), is
         determined by model hyperparameters
        :temperature=1 : Float value controlling randomness in boltzmann
         distribution. Lower temperature results in less random completions. As the
         temperature approaches zero, the model will become deterministic and
         repetitive. Higher temperature results in more random completions.
        :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
         considered for each step (token), resulting in deterministic completions,
         while 40 means 40 words are considered at each step. 0 (default) is a
         special setting meaning no restrictions. 40 generally is a good value.
        :top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
         overriding top_k if set to a value > 0. A good setting is 0.9.
        """
        batch_size = 1
        assert nsamples % batch_size == 0

        hparams = default_hparams()
        with open(os.path.join(self.path, self.model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if length is None:
            length = hparams.n_ctx // 2
        elif length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

        sess = tf.InteractiveSession()
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(self.path, self.model_name))
        saver.restore(sess, ckpt)

        return sess, output, context

    def render(self, type: str, utterance: str = None) -> str:
        logger.info(f"{self.__class__.__name__} | Input: {utterance} | Type: {type}")

        line = self._get_tokens(type, utterance)

        result = ""
        context_tokens = self.encoder.encode(line)
        l = len(context_tokens)
        for _ in range(self.nsamples // self.batch_size):
            out = self.session.run(self.output,
                                   feed_dict={
                                       self.context: [context_tokens for _ in range(self.batch_size)]
                                   })
            context_tokens = out[0]
        for token in out[:, l:]:
            result += self.encoder.decode(token)
        result = self._clean_result(result)

        logger.info(f"{self.__class__.__name__} | Result: {result} | Type: {type}")
        return result

    def _get_tokens(self, type: str, utterance: str = None) -> str:
        type = f"{self.types.get(type, '<|other|>')}"
        #s = f"<|short|> <|nazi|>"
        if utterance is None:
            s = f"<|short|> {type}"
        else:
            s = f"<|medium|> {type}" if random.random() < 0.4 else f"<|short|> {type}"
            s = f"{s}{utterance}"
        logger.info(f"Tokens: {s}")
        return s

    def _clean_result(self, result: str) -> str:
        result = f"{result}<|"
        pattern = "(.*?)<\|"
        return re.search(pattern, result).group(1)
