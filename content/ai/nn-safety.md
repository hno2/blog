---
title: Safety and Security for Neuronal Networks
Tags: machine learning, artificial intelligence, neuronal networks, robustness, safety, security, adverserial, attack, interpretability, explainability
date: 2020-07-21 8:11:00
slug: nn-safety
summary: How can we ensure that Neuronal Networks work the way we want them to work? An Overview of Attacks and their Countermeasures in the Domain of Neuronal Networks.
--- 
## Terminology 
* Robustness. Insensitivity to deviations from the underlying assumptions
* Saftey. Robustness to natural deviations (malfunctions)
* Security. Robustness to intended malicious artificially crafted input
* Verifiable AI - methods to ensure/prove the correctness of AI
* [Explainable AI](https://en.wikipedia.org/wiki/Explainable_artificial_intelligence) (XAI)- methods to make the results of AI understandable for humans

## Insufficiencies of Deep Neuronal Networks
Insufficiencies are systematic latent weaknesses

* Lack of Generalization. Input is different from training &rarr; Adversarial Attacks
* Lack of Explainability. Explain how what the AI learned and how it came to its decision
* Lack of Plausibility. 


## Interpretability
> Interpretability [is] the ability to explain or to present in understandable terms to a human.
<cite>[@@doshi2017towards]</cite>

Especially for critical systems (e.g. autonomous driving), we need to make sure that all edge cases are in the problem statement (Completeness).

* Transparent interpretability: *How does the model work?* This can be approached at different abstraction level model, components, or algorithmic level.
* Post-Training Interpretability: *What could the model tell me?* Based on explanations. 

&rarr; The Goal is to have an explanation that is human-understandable. [@@molnar2020interpretable]
From this goal we can derive properties that an explanation method should have:

* Expressive Power: Language and Structure are understandable.
* Translucency: The amount of (parameter) knowledge the method needs.
* Portability: Transfer of explanations is possible.
* Algorithmic Complexity: The computational effort needed to generate the explanation. [@@molnar2020interpretable]

And to make the method human-friendly, answers should answer the why-question. So good properties for explanations include

* Contrastive. Why this prediction and not another?
* Selective. Even if many reasons influence the prediction, only give back a couple.
* Social. Explanations are part of a communication
* Focus on the abnormal. Abnormal things should always be included
* Truthful. Machine Learning needs fidelity
* Consistent. Should conform to prior beliefs
* Probable and General. A generalized explanation is better than a rare cause. 

## Feature Visualization & Importance
The goal of Feature Visualization is to show the user what parts of the input image are most important for the classification. This can be seen as *"Where does the network look most?"*
### Activation Maps
Activation or Feature Maps visualize the filters of Convolutional Neuronal Networks. 
The idea is to create an image with random pixels and for each layer, you are interested in computing the gradients and update the pixel values to maximize the activation output.  

### Saliency Maps
Saliency maps help to understand the contribution of certain pixels in certain regions to the overall output.[@@simonyan2013deep]
### Class Activation Maps
> A class activation map for a particular category indicates the discriminative image regions used by the CNN to identify that category. <cite>[@@zhou2016learning]</cite>

The Activation map preceding the Global Average Pooling (GAP) Layer is a feature representation of the target but in space.

### Gradient Class Activation Maps
Gradient Class Activation Maps (Grad-CAM) uses additional Gradient in combination with GAP.

$$\alpha_{c}^{k}=\frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^{c}}{\partial A_{i, j}^{k}}$$

### Occlusion Sensitivity
By covering parts of the input image with grey patches (of increasing size) we can learn whether a feature map is sensitive to a specific part of the image. [@@zeiler2014visualizing] The common issue is that the background is learned instead of the object. 

### SHAPley Values
Idea from Game Theory to find out how much each feature contributed to the final output. 
The Shapley value is the average of all the marginal contributions to all possible coalitions.

&rarr; [Learn More](https://christophm.github.io/interpretable-ml-book/shapley.html) [@@molnar2020interpretable]

### Local interpretable model-agnostic explanations (LIME)
Local interpretable model-agnostic explanations (LIME) by [@ribeiro2016should] is a model agnostic way to explain a prediction. The instance requiring explanation is perturbed and get the predictions of our model. We then learn a second linear model with which we get the superpixel with the highest importance. 

&rarr; I like this [explanation](https://www.oreilly.com/content/introduction-to-local-interpretable-model-agnostic-explanations-lime/) or [this video](https://youtu.be/hUnRCxnydCc).

## Adversarial Attacks
### Taxonomy
based on the access level

* White Box - full knowledge of the model (parameters, structure...) &rarr; Gradient-based attacks
* Black Box - no knowledge of the model &rarr; Gradient-free attacks
* Grey Box - some knowledge (e.g. by transfer from another model)

based on goal

* Untargetet - output can be any class
* Targeted - output is of a specific class


* Adversarial example (AE) – input pattern that is generated to fool machine learning algorithm
* Perturbate ($\delta$ in an allowed/reasonable perturbation set $\Delta$) a given example $x$ in a way that maximizes the loss $\ell$
  
$$\operatorname{maximize}_{\delta \in \Delta} \ell\left(h_{\theta}(x+\delta), y\right)$$

### Methods

#### Fast Gradient Sign Method
The Fast Gradient Sign Method (FGSM) by [@goodfellow2014explaining] adds noise $\delta$ to move in the direction of the gradient $\Delta$ (untargeted attack) or opposite towards the target class $y'$ (targeted attack). The parameters $\theta$ control the size (visibility) of the perturbation.

$$\delta=\epsilon \cdot \operatorname{sign}\left(\nabla_{x} L(\theta, x+\delta, y)\right)$$

#### Projected Gradient Descent
Projected Gradient Descent iteratively takes gradient steps as described in FGSM

#### Carlini & Wagner Attack
The Carlini & Wagner Attack (C&W) starts with an adverserial loss $f(x+\delta)=\max \left(\max \left\{Z(x+\delta)_{i}: i \neq y^{\prime}\right\}-Z(x+\delta)_{y^{\prime}},-k\right)$ with $Z$ the logits returned and $k$ a confidence parameter.

The Optimization Problem is now $\underset{\delta \in \Delta}{\arg \min }\|\delta\|_{p}+c \cdot f(x+\delta)$ subject to $0 \leq x+\delta \leq 1$. The Optimization problem is to keep the change $\delta$ small and get a negative $f$, which happens when $(x+\delta)$ is missclassified. The constraint is for the pixel values of the image to be valid. [@@carlini2016towards]

#### Zeroth Order Optimization 
Zeroth Order Optimization (ZOO) is a gradient-free attack, meaning it works for black-box models, with access to just the scores. It has the same approach as the Carlini & Wagner Attack but infers the gradients form a large number of outputs. [@@chen2017zoo]

#### Boundary Attacks
Boundary Attacks by [@brendel2017decision]  (gradient-free black-box approach) search for the boundary between classes. The attacks start by choosing a point away from the clean image and then performing a binary search to find the boundary. Afterward, it follows the boundary to the closest point from the original image. [Check out the visualization](https://medium.com/bethgelab/accurate-reliable-and-fast-robustness-evaluation-4e2a5ab43521) by the author.

### Real World Attacks 
![Adverserial Patch](../images/ml2/adverserial-patch.jpg)
Real-World Attacks work by printing out a patch of perturbation [@@brown2017adversarial] [@@sharif2016accessorize].


### Defences
#### Increasing robustness
* Gradient Masking. Prevents a model from revealing meaningful gradients (e.g. Random Operations, shattered gradients)
* Adversarial Training. Add adversarial examples to the training. Model is vulnerable to unseen attacks
* Defense Distillation. [@@papernot2016distillation] Use two networks, one trained on data and one on the output probabilities of the first networks.
#### Detecting Adversarial Examples
* Naïve Approaches. Find differences between clean inputs and adversarial examples (e.g. PCA)
* Detector Networks. Add a subnetwork classifier
* Feature Squeezing. Compare predictions between squeezed (color reduction, spatial smoothing) and the unsqueezed image.
