#!/usr/bin/env python3
import random
import logging as logger
import re

import numpy as np
import tensorflow as tf
# tf.config.optimizer.set_jit(True)

from sample import *
from encoder import *

SEED = None
NSAMPLES = 1
BATCH = 1
LENGTH = 70
TEMPERATURE = 1.0
TOP_K = 40
TOP_P = 0.9


class GPTWrapper:

    def __init__(self, model_name, path, batch_size=BATCH, nsamples=NSAMPLES):

        self.batch_size = batch_size
        self.nsamples = nsamples
        self.path = path
        self.model_name = model_name
        self.encoder = get_encoder(model_name)
        self.session, self.output, self.context = self.interactive_model(SEED, LENGTH, TEMPERATURE, TOP_K, TOP_P)

    def interactive_model(
            self,
            seed,
            length,
            temperature,
            top_k,
            top_p
    ):
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
        assert self.nsamples % self.batch_size == 0

        hparams = default_hparams()
        with open(os.path.join(self.path, self.model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if length is None:
            length = hparams.n_ctx // 2
        elif length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

        sess = tf.InteractiveSession()
        context = tf.placeholder(tf.int32, [self.batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=self.batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(self.path, self.model_name))
        saver.restore(sess, ckpt)

        return sess, output, context

    def render(self, tokens):
        print(tokens)

        logger.info(f"{self.__class__.__name__} | Input: {tokens} ")

        context_tokens = self.encoder.encode(tokens)
        generated = 0
        for _ in range(self.nsamples // self.batch_size):
            out = self.session.run(self.output,
                                   feed_dict={
                                       self.context: [context_tokens for _ in range(self.batch_size)]
                                   })[:, len(context_tokens):]
            for i in range(self.batch_size):
                generated += 1
                text = self.encoder.decode(out[i])

        result = self._clean_result(text)

        logger.info(f"{self.__class__.__name__} | Result: {result} ")
        return result

    def _clean_result(self, result: str) -> str:
        result = f"{result}<|"
        pattern = "(.*?)<\|"
        return re.search(pattern, result).group(1)
