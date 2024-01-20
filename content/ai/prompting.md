---
title: Prompt Engineering 101 - Elevating Your Prompts to New Heights
slug: prompting
summary: Master ChatGPT prompt engineering with essential tips on crafting clear instructions, and exploring advanced techniques.
date: 2024-01-20 23:00
--- 
The art of prompting (also called prompt engineering) stands as a gateway to unlocking the true potential of text generation tools like ChatGPT. A well-crafted prompt with just the right instructions can unlock not only answers but also completely new use cases.

Let's establish a common ground: In the realm of textual data, a prompt is a user input, most often in natural language, functioning as the instruction that guides a large language model (LLM) to generate something or take a specific action. Here are four general tips to optimize the performance of these models for your needs:


1. **Understand Limitations:** Familiarize yourself with ChatGPT's operational constraints to tailor prompts for optimal performance.
      1.  Keep it Short: While the processing capabilities of ChatGPT and its counterparts have soared to new heights (with GPT-4 Turbo handling up to 128k tokens, equivalent to about 250 pages), it's essential to keep prompts concise. Very long texts, despite expanded capacities, may not yield optimal results.[@@2307.03172]
      2. Stay away from current: Note that ChatGPT is trained with a fixed cutoff date. While some adaptations can leverage additional tools or internet sources through Retrieval Augmented Generation (RAG, see [@2005.11401]),  up-to-date information is usually not reliable.
      3. Tasks like counting letters or words and some math problems will not work, either because tokenization or model restrictions.

2. **Instruct:** Craft your prompt as a clear instruction and split instructions from the information/example(s) with `###` or `"""` You can set the desired tone, specify the structure of the output – be it a table, bullet points or leave blanks for expansion. 

3. **Refine Iteratively:** You have two options to explore: a) refine the initial prompt based on model responses, or b) supplement instructions through additional chat prompts. As b) uses both the model's output and your inputs as memory/context, the results can be quite different.

4. **Check Results:** Before you delve deeper, always check the results. This step ensures that the generated output aligns with your expectations. Regularly assessing outcomes allows for quick adjustments and improvements. LLMs are prone to confabulations (also known as hallucinations), meaning they can come up with imaginary facts, Links, Papers etc. There are two simple prompt additions that can reduce the amount of these confabulations: 
      1. *"I don't know"*: Enhance output reliability by prompting ChatGPT to respond with "I don't know" when uncertain. Note that this approach isn't foolproof, as it doesn't eliminate all hallucinations. Additionally, future ChatGPT updates may impact results.
      2. *"What did I ask you to do"*: By asking ChatGPT to reproduce the original question, you can follow its Train of Thought and adapt if something was missed.



## For-Reasoning Prompts

This category encompasses prompting techniques designed to enhance ChatGPT's reasoning abilities. The primary strategies involve breaking down complex tasks into subtasks and offering reasoned instructions. These approaches provide ChatGPT with additional time and guidance, aiding it in deriving more accurate results.

### "Few-shot"
Few-shot learning [@@brown2020language] is a paradigm where a model can perform a task with minimal examples or shots of data. Unlike traditional approaches that require large datasets, few-shot learning enables a model to generalize and make accurate predictions based on a small set of examples, often just a handful.
Rather than stipulating the desired outcome, you provide explicit and representative examples that demonstrate the proper approach to solving the task.
See my [Blog Post](/n-shot) on example 

### "Chain-of-thought"

Chain of Thought (CoT) Prompting [@2201.11903], enhances few-shot learning by incorporating the reasoning process leading to the answers in the example. Unlike standard "Few-shot" prompting, it provides not just questions and answers but also the logical steps for arriving at solutions. However, it's important to note that chain-of-thought prompting may adversely impact performance compared to the traditional few-shot approach. In such cases, employing "Self-consistency" prompting may offer a remedy.


### "Think Step-by-Step"

[@2205.11916] describe using LLM as zero-shot learners, meaning that the systems need no example to solve complex problems. Their approach involves instructing ChatGPT to reason through a task sequentially (zero-shot Chain of Thought). Two steps are involved: By prompting ChatGPT to *"think step-by-step,"* a step-by-step description is generated, which is used as part of a second prompt to come to the final conclusion. The goal is to minimize the likelihood of missing crucial steps in the reasoning process.

### "Least-to-most"
Least-to-most prompting [@@2205.10625] involves breaking down complex tasks into smaller, more manageable subtasks. This strategy includes two stages:

1. Decomposition: The prompt initially provides examples demonstrating how to decompose complex problems, followed by the specific question to be decomposed.

2. Subproblem Solving: This stage's prompts are created based on three components:the initial problem description, a potentially empty list of previously answered subquestions and generated solutions, and the next question to be addressed (can be the initial question).


### "Selection-inference" and "Faithful reasoning"
[@2205.09712] introduced an extension to the chain-of-thought technique, which involves breaking down the generation of explanations and answers into smaller, modular parts. In this approach, the first prompt, known as the 'selection prompt', picks a relevant subset of facts from the text. Subsequently, a second prompt, the 'inference prompt', deduces a conclusion from the selected and limited facts. These prompts are iteratively alternated in a loop, creating multiple steps of reasoning that lead to a final answer, as illustrated in the accompanying figure.
This method was extended with Faithful Reasoning [@2208.14271], including ideas for when to halt the loop and further reduce hallucinations.
The application of both techniques is not straightforward, as it requires the fine-tuning of both selection and inference language models.


### "Maieutic"
[@2205.11822] introduced maieutic prompting, which generates a tree of potential explanations, both correct and incorrect, and analyzes their relationships to deduce the correct set. This complex but innovative technique explores the Socratic method of questioning to elicit ideas and determine logically integral explanations. For most of your use-cases this will be overkill and hard to apply. 

## Monte-Carlo Prompts
The techniques in this category improve the reliability by using repeated sampling, similar to a Monte Carlo simulation, to comprehend and predict outcomes based on their likelihood. Essentially, the model is called multiple times, and the collected answers are summarized to derive a result. If applicable, it is recommended to set a higher temperature parameter for the results to have a higher variance. However, it's crucial to be aware that these methods incur a higher cost, as the model is sampled repeatedly.



### "Self-consistency"
With Self-consistency [@@2203.11171] after generating multiple diverse results via Chain of Thought Prompting, the final result is determined by a majority vote or another metric. So you pick the answer that occurs most often.

### Tree/Graph of Thought
These methods extend Self-consistency by representing the reasoning steps ("thoughts") in a tree (Tree of Thought,[@2305.10601]) or Graph (Graph of Thought, [@2308.09687]), and having the model self-evaluate nodes for tree/graph search  algorithms. To use these advanced methods you will need to have some coding experience. (GitHub Repos [ToT](https://github.com/princeton-nlp/tree-of-thought-llm) and [GoT](https://github.com/spcl/graph-of-thoughts)).



# Outlook
Only a short while ago, we discussed the emerging role of a Prompt Engineer, responsible for crafting prompts for LLMs. However, recent advancements, such as Auto-CoT [@@2210.03493], Automatic Prompt Engineer (APE)[@@2211.01910], and Optimization by Prompting (OPRO)[@@2309.03409], reveal that LLMs themselves excel at prompt engineering. These techniques not only match but often surpass human-level performance, demonstrating the capacity to guide models toward truthfulness and informativeness. It suggests that in the future, the most effective prompts will be generated by LLMs.