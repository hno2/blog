---
title: n-shot Learning for NLP
Tags: machine learning, artificial intelligence, neuronal networks, nlp
slug: n-shot
date: 2021-09-10 14:23
summary: Few-shot, one-shot and zero-shot learning allow us to train models with minimal data in a way even more similar to how we humans learn.
--- 

Developing algorithms capable of generalizing to new tasks with just a few samples is a major problem in narrowing the gap between performance at a machine and human level. Organized, reusable concepts are the essence of human cognition enabling us to quickly adjust to new tasks and make sense of our choices. In NLP models are limited by their requirements for large annotated datasets for each new task. As models nowadays develop broad skills with the ever-better capacity of transformer models, meta-learning can be used to utilize these skills even with zero or few samples. E.g. *"Few-shot classification  is a task in which a classifier must be adapted to accommodate new classes not seen in training, given only a few examples of each of these classes."* [@@snell2017prototypical]

For meta-learning three options are possible, each not updating model weights: [@@brown2020language]

## Few-short Learning
Few-short Learning or in-context learning, allowing as many demonstrations ( $N=[10..100]$ ) as the model’s context window allows
~~~{#lst:fewshot .py caption="Example for Few Short Learning Input with N=3"}
Translate German to English   # Directive
Lehrer => teacher             # Demonstration
Uhrzeiger => watch handle     # Demonstration
Schule => school              # Demonstration
Lernen =>                     # Query
~~~

## One-Shot Learning
One-Shot Learning allowing only one demonstration plus a directive
~~~{#lst:oneshot .py caption="Example for One-Short Learning Input with (N=1)"}
Translate German to English   # Directive
Lehrer => teacher             # Demonstration
Lernen =>                     # Query
~~~
## Zero-Shot Learning
Zero-Shot Learning allowing only a natural language directive and no examples
~~~{#lst:zeroshot .py caption="Example for One-Short Learning Input (N=0)"}
Translate German to English   # Directive
Lernen =>                     # Query
~~~

The data used for few/one/zero-shot learning is called support set $\mathcal{S}=\left\{\left(x_{1}, y_{1}\right),\left(x_{2}, y_{2}\right), \ldots,\left(x_{K \times N}, y_{K \times N}\right)\right\}$, $N$ denotes the number of samples (n-shot) and $K$ the number of classes in the support set (k-ways). For classification tasks each class must contained in the support set. The Query set $\mathcal{Q}=\left\{\left(x_{1}^{*}, y_{1}^{*}\right),\left(x_{2}^{*}, y_{2}^{*}\right), \ldots,\left(x_{Q \times N}^{*}, y_{Q \times N}^{*}\right)\right\}$ contains a number of requests to the network, nessesarily from the same classes of the support set.

GPT-3 is one example of a model that is usable in these type of setting:*"We presented a 175 billion parameter language model which shows strong performance on many NLP tasks and benchmarks in the zero-shot, one-shot, and few-shot settings, in some cases nearly matching the performance of 40 state-of-the-art fine-tuned systems, as well as generating high-quality samples and strong qualitative performance at tasks defined on-the-fly."* [@@brown2020language]

NLP is not the only use case for n-shot learning it is already popular in Computer Visions, Robotics and Audio Processing.