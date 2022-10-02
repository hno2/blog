---
title: NLP for Programming Code
Tags: machine learning, artificial intelligence, neuronal networks, nlp
slug: nlp4code
date: 2022-08-20 16:23
summary: TBD
---
Natural Language Processing is the current hot topic for many machine learning practitioners.
With [Hugging Face](https://huggingface.co/) democratizing the access to state-of-the-art pre-trained models and almost daily new advances, it seems like now is the perfect time to get started. The models can find & fix bugs, generate code based on natural language input or even translate between programming languages.
 
In this blog post, I will give you an overview of NLP Methods for programming code understanding, focused on models for Python.
 

## Code Understanding
### The Problem of Data
In 2019 GitHub published CodeSearchNet [@@hamel2019codeSearchNet], a challenge, benchmark, and dataset for six programming languages consisting of functions with documentation from open source projects on GitHub. The dataset and baseline models focus on Code Search. Self Attention encoding code and search query yielded the best overall result, measured by the Mean Reciprocal Rank between the correct code snippet and 999 distractors.
 
In March 2021, Microsoft published a benchmark dataset called [CodeXGLUE](https://github.com/microsoft/CodeXGLUE)[@@shuai2021codeXGLUE] that contains ten tasks across 14 different programming languages (including Python, Java, C++). CodeXGLUE is an adaption of the General Language Understanding Evaluation (GLUE) Benchmark to Programming Code.
The tasks are categorized into four distinct categories, shown in the table below:
<table>
<thead>
<tr>
<th>Category</th>
<th>Task</th>
<th>Description</th>
<th>Dataset for Python</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="6"><strong>Code-Code</strong></td>
<td>Clone Detection</td>
<td>Semantic Similarity</td>
<td>No</td>
</tr>
<tr>
 
<td>Defect Detection</td>
<td>Function Vulnerability</td>
<td>No</td>
</tr>
<tr>
<td>Cloze Test</td>
<td>Masked Token Prediction</td>
<td><em>Yes</em>    <a href=https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-all/data/cloze-all/python><span class="caps">CT</span>-all</a>/<a href=https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/ClozeTesting-maxmin/data/cloze-maxmin/python><span class="caps">CT</span>-min/max</a></td>
</tr>
<tr>
 
<td>Code Completion</td>
<td>Predict following Tokens</td>
<td><em>Yes</em>   <a href=https://www.sri.inf.ethz.ch/py150>Py150</a></td>
</tr>
<tr>
<td>Code Refinement</td>
<td>Bug Fixing</td>
<td>No</td>
</tr>
<tr>
<td>Code Translation</td>
<td>Translation between Programming Languages</td>
<td>No</td>
</tr>
<tr>
<td rowspan="2"><strong>Text-Code</strong></td>
<td>Code Search</td>
<td>Search code based on <span class="caps">NL</span>-Input</td>
<td><em>Yes</em> CodeSearchNet</td>
</tr>
<tr>
<td>Text-to-Code Generation</td>
<td>Generate Code based on <span class="caps">NL</span>-Input</td>
<td>No</td>
</tr>
<tr>
<td><strong>Code-Text</strong></td>
<td>Code Summarization</td>
<td>Generate Documentation based on code</td>
<td><em>Yes</em> CodeSearchNet</td>
</tr>
<tr>
<td><strong>Text-Text</strong></td>
<td>Documentation Translation</td>
<td>Translate documentation between NLs</td>
<td>-</td>
</tr>
</tbody>
</table>
 
Microsoft also published two strong baseline models, CodeBERT [@@zhangyin2020CodeBERT] and CodeGPT (GPT by [@brown2020language] trained on Programming Code). CodeBERT is used for all problems that require understanding and CodeGPT for completion and generation. The pre-trained models are available easily from [Hugging Face](https://huggingface.co/microsoft/codebert-base)
 
In May 2021, IBM published CodeNet [@@ruchir2021codenet] a novel and extensive dataset build on student submissions in 50 programming languages and including metadata on footprint and errors.
 

### Networks using AST
Abstract Syntax Trees represent program code an abstract tree. In Python, AST are just one standard [library](https://docs.python.org/3/library/ast.html) away. While it seems worthwhile to  I have not seen recent models utilizing this meta information.
### CodeBERT
Based on the BERT [@@devlin2018bert] transformers Microsoft trained a model on both bimodal and unimodal data of both programming code and natural language code documentation. Bimodal data refers to parallel data of natural language-code pairs, and unimodal data, where only one type (programming code or natural language) is used. Pretraining of CodeBERT is done via Masked Language Modelling (MLM - bimodal data) and  Replaced Token Detection (RTD - both unimodal and bimodal data). [@zhangyin2020CodeBERT] leave open the question of how to best integrate Abstract Syntax Trees (AST) and whether this might be able to improve performance.
 
### CodeTrans
CodeTrans by [@elnaggar2021codetrans] is one of the most recently published papers. The group from TU Munich, Google, and Nvidia trains T5 models on the same or similar datasets, described above, with a focus on Transfer and Multi-Task Learning. The T5 models were trained in three different sizes (small, base, large), with the training taking up to 87 days. CodeTrans with Transfer Learning or Multi-Task was able to outperform CodeBert in all Categories and languages, with the CodeTrans Multi-Task Base model performing best for Python. Again the pre-trained models are available on [Hugging Face](https://huggingface.co/SEBIS/code_trans_t5_base_code_documentation_generation_python_multitask_finetune).
## Debugging
### Deep Debug
[@drain2021deepdebug] from Microsoft build on their DeepDev PyTM5 transformers [@@clement2020pymt5], which seems like a successor of CodeGPT especially for Python) architecture. A dataset was generated by crawling GitHub (what a coincidence that GitHub was acquired by Microsoft in 2018) for commit messages with common Bug keywords (for example "Fix Bug"). The model was trained with bi-directional data, meaning both from buggy code to fixed code and from fixed to buggy. This idea - called back-translation - is already widely used in NLP.
Normalization for programming code can be difficult, and it has been shown that datasets with duplicate code can be problematic. [@@allamanis2018adverse]
To avoid these problems DeepDev tokenizers strips comments, standardize whitespace, and replaces
string and numeric literals with placeholders. A neural edit model to augment the data with synthetic bugs is also used for preprocessing.
Using this model backward DeepDebug can introduce synthetic (neural) bugs. Additionally, they employ a rule-based (heuristic) system.
DeepDebug increases performance (bugs found), while reducing False Positives significantly (compared to prior methods by [@lutellier2020coconut]). When Pytest stack traces are available the performance increases even further to 97% (Top-10 Success Rate). DeepDebug is said to be open-sourced, but currently, neither code nor dataset is available. (2021-06-11)
## Code Generation
Code Completion can be seen as a subtask of Code Generation, starting from your input. Since this blog post was first published in July 2021 a lot has happend. First of all GitHub CoPilot
 
### GitHub Copilot
[Github Copilot](https://github.com/features/copilot) is a tool that allows end-users without any machine learning skills to generate code in their favorite editor like Visual Studio Code.
GitHub CoPilot can be seen as an automatic Peer Reviewer and CoProgrammer that can generate code based on function names and documentation. It is powered by a novel neuronal network based on GPT-3 [@brown2020language] called Codex [@chen2021evaluating] build by OpenAI. As a propriatary model most of the details of the current version are unknown.
 
Copilot is available for free for OpenSources projects and students. Everyone else pays 10$/month.
#### Codex
Their overall goal was to translate docstrings of Python functions to functioning implementations and back, providing a solution that could function as a co-programmer. The training data contains 159 GB of Python programming code from openly available sources (e.g. GitHub Repositories) and natural language. Based on Codex, Codex-S was finetuned on only functions and docstrings, with the data collected from competitive programming websites and continuous integration. Codex-D was finetuned to generate docstring for existing programming code, in order to better understand models' intentions.
 
### Google
[Google](https://ai.googleblog.com/2022/07/ml-enhanced-code-completion-improves.html) created their own internal system for autocomplection with a similar approach. As with the Codex Model the base model is a Transformer network, here with "only" 0.5B parameters (due to latency considerations) and trained on internal code. While the training procedure is comparable (masking random code lines, leaving the rest as context),  the data is different. While the other models are trained with freely available code, this means that only curated quality code (tested, and peer-reviewed) is used for training. Following a data-driven Machine Learning life cycle this could increase the overall quality of the code generated. One has to consider the use case of the system. As it is used soley internally, this means Google can allow the model to be more specific and focused on their programming style and interfaces.
 
Additionally Google is combining of their semantic code-completion engine with the results of the Machine Learning model: Results that are both in the Semantic Engine as well as in the ML model predication are re-ranked by boosting their order. Additionally all suggestions are checked for semantic correctness using the same Semantic Engine and cached abstract syntax trees (AST). In a hands-on test, this hybrid approach reduced context switching by 7% and overall development iteration time by 6%.
 

### CodeGPT
CodeGPT has not officially been published, as it is basically a finetuned GPT-2. Some implementation and training details can be found [here](https://github.com/microsoft/CodeXGLUE/issues/36).
 
## Code Similarity
Code Similarity is important for Plagiarism Detection, but also for clustering code examples based on their implemented functionality.
The similarity of code can be measured by simple distance measures, like the Jaccard Distance, but this is unsatisfactory. Short Distance does not mean that programs have the same functionality or solve the same problem. [@ruchir2021codenet] propose using a Siamese network with token sequence to achieve similarity measured based on implemented functionality.
 
## Current Open Questions
* How can Abstract Syntax Trees help to improve accuracy?
* Why do CodeTrans not add extra whitespace tokens like the four spaces indent typical for Python? DeepDev is doing it and it increases throughput.
    * What Models employ this technique.
