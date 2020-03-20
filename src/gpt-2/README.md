
# GPT-2 Finetuning

This is a modified GPT-2 source based on:
* [original OpenAI's GPT-2 repository](https://github.com/openai/gpt-2)
* [nshepperd's fork](https://github.com/nshepperd/gpt-2)

## Usage
Install the necessary dependencies via pip:
```bash

pip install -r requirements.txt

```

Create a models directory:
```bash

mkdir models

```

Download models into the directory by running:
```bash

python download_model.py 774M

```
There are four currently available models:
* 124M
* 355M
* 774M
* 1558M

Or copy your own model there.

Then, you will need to pre-process your dataset:
```bash

PYTHONPATH=src ./encode.py --model 774M data.txt data.npz

```

After you have the model and the dataset, run:
```bash

PYTHONPATH=src ./finetune.py --model 774M --dataset data.npz

```

# gpt-2

Code and models from the paper ["Language Models are Unsupervised Multitask Learners"](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf).

You can read about GPT-2 and its staged release in our [original blog post](https://blog.openai.com/better-language-models/), [6 month follow-up post](https://openai.com/blog/gpt-2-6-month-follow-up/), and [final post](https://www.openai.com/blog/gpt-2-1-5b-release/).

We have also [released a dataset](https://github.com/openai/gpt-2-output-dataset) for researchers to study their behaviors.

<sup>*</sup> *Note that our original parameter counts were wrong due to an error (in our previous blog posts and paper).  Thus you may have seen small referred to as 117M and medium referred to as 345M.*

### Some caveats

- GPT-2 models' robustness and worst case behaviors are not well-understood.  As with any machine-learned model, carefully evaluate GPT-2 for your use case, especially if used without fine-tuning or in safety-critical applications where reliability is important.
- The dataset our GPT-2 models were trained on contains many texts with [biases](https://twitter.com/TomerUllman/status/1101485289720242177) and factual inaccuracies, and thus GPT-2 models are likely to be biased and inaccurate as well.
- To avoid having samples mistaken as human-written, we recommend clearly labeling samples as synthetic before wide dissemination.  Our models are often incoherent or inaccurate in subtle ways, which takes more than a quick read for a human to notice.

## Development

See [DEVELOPERS.md](./DEVELOPERS.md)

## Contributors

See [CONTRIBUTORS.md](./CONTRIBUTORS.md)

## Citation

Please use the following bibtex entry:
```
@article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019}
}
```

## License

[Modified MIT](./LICENSE)
