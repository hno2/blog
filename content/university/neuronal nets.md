---
title: [Lecture] Neuronal Networks
Tags: summary, lecture, ai, machine learning, artificial intelligence, exam, adaptive learning, neuronal network, lecture-notes, kit
slug: nn
layout: page
summary: a helpfull guides to the basics of NN
---

Question: How can we train Neuronal Networks faster and with better generalization?
Ideas: 

* Parallel Hardware (?)
* Efficient Implementation
* Faster Gradient Descent Search
* Selective Choice of Patterns
* Efficient Architectures


# Faster Gradient Descent
For visualizaton of Gradient Descent image a ball rolling down a hilly sloppy (this is our loss landscape) 
Initiation of our neuronal network means setting the ball at some random place in the landsape with no speed. Gradient Descent makes the ball roll towards the valley: For each weight update step it will go downhill but do not change its speed.

## Changing the Learning Rate
To get faster to our goal we could start with a high speed and decrease it the further we go. You might ask why not use the high speed all the time? Because than the ball might overshoot the global minimum and oscialte between the two hills left and right of the valley (We say the Neuronal Network does not converge).

## Momentum
Image half way to the bottom of the hill there is a sea, that is flat. The ball will not roll any further, we have reached a local minium - but not the global minimum. 


With Momentum we add a second term to our weight update, which looks at our previous gradient. If in this step we go in the same direction we accelarate, which leads to faster convergence, if it is different we reduce the update, which leads to less flucuations.
$\Delta \mathbf{w}_{\mathrm{ij}}(\mathrm{t})=\underbrace{-\varepsilon \partial \mathrm{E} / \partial \mathbf{w}_{\mathrm{ij}}(\mathrm{t})}_{\text{Learning Rate}}+\underbrace{\alpha \Delta \mathbf{w}_{\mathrm{ij}}(\mathrm{t}-1)}_{\text{Momentum}}$

## [Rprop](https://en.wikipedia.org/wiki/Rprop)
If the gradient (the direction where the ball should go) is switching for each update, it is likeley that we oscilating around a minimun. 
Therefore we ith Resilient backpropagation (Rprp) [@@riedmiller1994rprop] we use a a different learning rate for each weight. If we think in terms of our visualization this means, one weight (or distance) for left and right and one for up and down (or height).

So every time the direction/sign of the gradient for a weight changes, we will decrease the learning rate of it. If the direction is in the same direction we increase the learning rate.


## Training Samples
We might skip backward passes of samples if their output is under a threshold, meaning we have learned this pattern successfull. 
Or we update weights not after a whole batch but after subsets. Updating after every sample is fast but risky. *mini-batches*

## Acceleration of Learning Phase
By adding a constant to the output of each neuron, neurons are less likely to get stuck at turned off state. This is due the derivative of the sigmoid convering to zero for $+/-\infty$ [@@fahlman1988empirical]
## [Quickprop](https://en.wikipedia.org/wiki/Quickprop) 
Directy calculate the minimum. We assume that the error surface is a parabola and the parabolas for each weight are independent. Eventhough this is not true in reality this helps to quickly get near the actual minimum.
$\Delta \mathrm{w}(\mathrm{t})=\frac{\mathrm{s}(\mathrm{t})}{\mathrm{s}(\mathrm{t}-1)-\mathrm{s}(\mathrm{t})} \cdot \Delta \mathrm{w}(\mathrm{t}-1)$
with $\mathrm{s}(\mathrm{t})=\frac{\partial \mathrm{E}}{\partial \mathrm{w}_{\mathrm{ij}}}(\mathrm{t})$
## Performance Sheduling
Measure the error on the cross validation set and decrease the learning rate when the algorithm stops improving.

## Weights Initiation
Selecting the initial weights of a network can be an art. Rule of tumb would be $-0.3...+0.3$.

# Objective/Looss Function
## Mean Squared Error
$MSE=\sum_j(y_j-\text{target}_j)^2$ fails for if you have many outputs classes, since the influence of the one right class is minimal. Therefore it is likely that the network will set all outputs to zero.

To improve this use [softmax](https://en.wikipedia.org/wiki/Softmax_function).
$\sigma(\mathbf{z})_{j}=\frac{e^{z_{j}}}{\sum_{k=1}^{K} e^{z_{k}}} \quad$ for $j=1, \ldots, K$

## Classification Figure of Merit [@@hampshire1990novel]
$E_{CFM}(w) = \sum_k \frac{\alpha}{1 + e^{-\beta \Delta_k + \gamma}}$
Use the difference of the biggest wrong output and the true node $\Delta_k$

## Activation Functions
$\rightarrow$ Look at the [Wikipedia Article of most Activation Functions](https://en.wikipedia.org/wiki/Activation_function#Comparison_of_activation_functions)

## Batch Normalization


# Generalization
Collect more data
early stopping

architectual learning: just large enough occams razor
    * repated experiments
    * grow from small to big (constructive)
    * Reduce from big to small (desctructive)

# Unsupervised Learning


## Autoencoder
Give Input goal is to reconstruct the input at the networks outputs
Encoder and Decoder share 
## Variational Auto-Encoder

## Loss
How do we score the ouput of an unsupervised neuronal network

**Pixel-wise loss**: Use Mean-Squared Error
**Content Error**: Use Mean Squared Error on abstract Feature Vectors

### Gernerative Adversarial Network
Two nn compete against each other [@@makhzani2015adversarial]

## Structure Prediction
Given a part of an object/input reconstruct the rest of the object