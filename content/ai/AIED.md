---
title: Notes on the Artificial Intelligence in Education Conference 2021 
Tags: machine learning, artificial intelligence, conference, notes, education
--- 
Last week I participated in the AI in Education Conference (AIED) (virtually of course). Here are my semi-structured notes and comments.

## Keynote Dan Russel
Google's goal for education is assisting and inspiring Students.
Google is used extensively for learning - about 2% of all queries are about learning. Full homework questions make up about 0.9%, queries about concepts 1%, and queries about learning systems 0.1% 
The cognitive model of an AI system can matter more than its performance. If you do not have a good UX design it does not matter how good your AI is, so the user-centric design is key to successful implementation. We should think about the computer skill level of a population also which is often worse than thought. About 65% have a poor or lower level of computer skills, and only 10% are able to search a page via Ctr+F, mapping to a strong of computer skills. [@@OECD2016Skills]

Google helps students by presenting extra information boxes on the right-hand side. For many homework questions, Google goes even further and provides practice problems, the formula, and a calculator. (To test this, search for *newton's laws* or *covid*)

YouTube also plays a huge role in learning, as about 1/3 of the views are for learning (~1 billion/day) but not only for academic education but also for DIY problems. Google, therefore, offers you videos where they (based on the subtitles)highlight the parts that might answer your question. This way, you can skip everything else (introduction and more).

Considering mental models of AI systems is necessary, as it means that one can predict and understand what a system can do and not. We need to know that there are some questions Google can not answer. The big question is how to transfer learners from *"Answer my question now"* to *"Get started learning concepts"*. Today this means you cannot Google-proof your questions and students will go outside of classical resources. But this implies that learning how to ask questions and (critically evaluate) content is the essential learning skill of our century. Meta-learning (learning how to learn) is a must-have skill, and today learning how to search means learning how to learn.


## RepairNet
[@abhinav2021repairnet] train an encoder-decoder architecture based on LSTM (with attention for the encoder) on program exercises for C for 93 programming tasks (total of ~7k erroneous programs). They outperform the previous approach MACER, when using error messages as additional model input. The DeepDebug approach with a multi-language pretrained transformer networks (and additional synthetic bugs), seems like an even better approach to this problem. [@@drain2021deepdebug] Unfortunately there is currently no source code or pre-trained models available to test the performance. 
But both papers miss out on how to present this solution with bugs fixed to students and learners. Some ideas can be derived from the next paper.

## An Approach for Detecting Student Perceptions of the Programming Experience from Interaction Log Data
For many students spending time on fixing errors is seen as an indication of low ability as it is not anticipated in experts. This negative self-assessment often leads to lower self-efficacy, influencing persistence, and overall performance, looking like a self-fulfilling prophecy. [@gorson2021approach] level the field, by detecting these negative moments based on browser and IDE logs. This can help to analyze processes, performance or build automated interventions. 

Negative self-assessment moments were labeled in the log data from 42 students via retrospective interviews. The labels were  grouped into eight categories

* *Using resources to look up syntax* from the web or other sources
* *Using resources to research an approach* from the web or other sources
* *Changing approaches* to try a new approach for solving the programming problem
* *Writing a plan* in the comments or notes to outline future programming steps
* *Getting simple errors* are usually compiler errors due to oversights or typos
* *Getting Java errors* are usually runtime errors due to conceptual mistakes
* *Struggling with errors* while trying to fix or debug the errors
* *Stopping to think* while implementing a solution

## Interpretable Clustering of Students’ Solutions in Introductory Programming
[@effenberger2021interpretable] propose a four-stage process to cluster coding solutions:

1. Feature Selection. Features can be created via Abstract Syntax Trees or other statistical features (e.g. length) and are selected based on importance and interpretability. Features that are too similar (measured by the Jaccard Coefficient) are discarded
2. Pattern Mining. The interpretability is taken into account (by preferring fewer clauses) and an approach similar to the depth-first tree projection algorithm implemented
3. Pattern Selection uses a greedy approach called sequential covering, where patterns are scored both on Homogeneity, Interpretability (criteria: short, important, positive, precision), and Coverage.
4. Clustering Summarization. Providing a short description of each Cluster.

Using these clusters, learners can get strong feedback based on the cluster they fall in, e.g. when solving a problem that can be solved via indexing a `for` loop. 

## Extracting and Clustering Main Ideas from Student Feedback Using Language Models
[@masala2021extracting] use BERT to cluster main ideas from student feedback. After the keywords are extracted (via [KeyBert](https://maartengr.github.io/KeyBERT/)), context is added to be used for clustering by K-means. Based on these the Overall course rating is predicted for testing. Their approach can be easily adapted to other languages and contexts.



## “Can You Clarify What You Said?”: Studying the Impact of Tutee Agents’ Follow-Up Questions on Tutors’ Learning
[@shahriar2021can] develop a synthetic tutee for math that can ask deep questions. They call this Constructive Tutee Inquiry (CTI). Tutor learning happens when students learn by teaching others and get questions that promote knowledge-building responses (KBR). 
These questions can be grouped like so: 

| Category                         | Description                                                | Example                                                                             |
| -------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Explanation (Elaboration)        | Providing extended clarification for a concept of interest | *“Can you elaborate?”*                                                              |
| Example (Elaboration)            | Providing more examples for clarification                  | *“I know little about [x], tell me more?”*                                          |
| Error realization (Sense-Making) | Realizing own errors or misconceptions                     | *“I acted according to the rule I have learned from you. Why am I wrong?”*          |
| Inference   (Sense-Making)       | Realizing new inferences based on prior knowledge          | *“How to convert the unfamiliar form to the familiar one you’ve taught me before?”* |

Their user study with middle schoolers showed that CTI facilitated learning conceptual knowledge only for low prior tutors.

## “I didn’t copy his code”: Code Plagiarism Detection with Visual Proof
[@john2021didn] use a Random Forest (80% balanced accuracy) to detect Code Plagiarism and use [pydiff](https://github.com/yebrahim/pydiff) to provide a visual comparison.
## Assessment2Vec: Learning Distributed Representations of Assessments to Reduce Marking Workload
[@wang2021assessment2vec] use a pretrainedBERT transformer network combined with an LSTM to automatically assess free text answers of the automated student assessment prize (ASAP) dataset (available as a [Kaggle competition](https://www.kaggle.com/c/asap-aes))