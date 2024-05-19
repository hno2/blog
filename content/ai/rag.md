---
title: Enhancing LLM Performance with Retrieval Augmented Generation (RAG)
Tags: machine learning, artificial Intelligence, ai, rag, agents, search, llm, Retrieval-Augmented-Generation
date: 2024-05-19 20:30:00
slug: rag
summary: Enhance the performance of large language models (LLMs) using Retrieval Augmented Generation (RAG) with our comprehensive guide. Learn how to effectively build a RAG system by mastering key steps: loading, indexing, storing, and querying.
---
Over the past six months, I've been working hard to improve the performance of large language models (LLMs) using corporate text data through a technique known as Retrieval Augmented Generation (RAG). RAG uses pre-trained models such as [GPT-3.5](https://openai.com/research/gpt-3), [LLaMA](https://ai.facebook.com/blog/large-language-models-are-having-their-stable-diffusion-moment/) or [Mistral](https://www.mistral.ai/) and dynamically incorporates relevant data into the query so that the model has the necessary context. It's important to remember that a prompt is essentially a long string; RAG systems append relevant information to this string. Importantly, this process does not change the training or hyperparameters of the model.

Here are the key lessons I've learned and a brief overview of what it takes to build an effective RAG system.

## Building a RAG system

There are six main steps to building a RAG system:
1. Loading
2. Indexing
3. Storing
4. Retrieval
5. Generate
6. Evaluate

In this article I will focus on the first four steps of creating a RAG system. The operational aspects and evaluation of such a system are complex and will be covered in a future article.

## 1. Loading

This step is essentially about data engineering and its complexity can vary considerably. It can range from reading CSV files with text to loading various types of files, including Office documents or even OCR processed images. There is a wide range of libraries available to help with these tasks. Some of the more notable ones are

- [LangChain](https://github.com/langchain-ai/langchain)
- [LLaMAIndex](https://github.com/jerryjliu/llama_index)
- [txtai](https://github.com/neuml/txtai)
* [haystack](https://github.com/deepset-ai/haystack)
These libraries provide robust tools for dealing with the various challenges associated with loading data into a RAG system. In my experience, Langchain has the most advanced RAG features available with a simple architecture. 
## 2. Indexing

Indexing involves first chunking—splitting—the documents and then embedding them. Depending on your data, it often makes sense to select and describe additional metadata.

### Chunking

Chunking, also known as text splitting, breaks up texts that are too long to embed into smaller, semantically similar pieces. There is a trade-off with chunk length: smaller chunks improve overall retrieval quality but may result in a loss of context and increase processing requirements for indexing and retrieval.

- **Fixed-length chunking**: Divides text into blocks of equal size, which is simple but often splits sentences or paragraphs unnaturally, sometimes even in the middle of words.
- **Sentence- or paragraph-based chunking**: Splits text at natural boundaries, preserving structure but potentially resulting in uneven chunk sizes.
- **Document-specific chunking**: For formatted text documents such as Markdown, HTML, or JSON, specific chunking strategies can be used to preserve structure and context of the document.
- **Semantic or agentic chunking**: Uses semantic similarity to break text into meaningful chunks based on content, ensuring that each chunk is contextually relevant.

### Embedding

Embedding is the process of converting chunks into numerical representations also known as  vectors or embeddings. 

- **Model Selection**: Choosing the right embedding model is critical. Factors to consider include the cost of the model, computational requirements (local vs. remote deployment), the maximum chunk size it can handle, performance, and the length of the output vectors. Resources such as the [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) can help you compare models based on these factors.
- **Dimensionality**: The dimensionality of the embedding vectors (e.g., 128, 256, 768 dimensions) affects both the performance and the computational load in the query step. Higher dimensions typically provide more nuanced representations but require more resources for storage and computation.
- **Training Data Similarity**: Ensure that the embedding model is trained on data similar to your use case to improve its relevance and accuracy. Pre-trained models can be fine-tuned on your specific dataset for better performance.
- **Multi-Embeddings**: In many cases it can be useful to index not only based on semantic similarity but also based on keywords or phrases that contain a specific string. The advantage is that abbreviations or domain-specific terms can be matched directly. While semantic similarity search usually uses dense vectors, keyword search uses sparse vectors - one dimension equals one token. These text search models must be applied to your corpus before they can be used.  You have the following options for keyword search
	* BM25 works on a normalised frequency analysis of words. 
	* [SPLADE](https://github.com/naver/splade?tab=readme-ov-file#playing-with-the-model) 

Note that you will need the same model(s) at runtime to create embeddings of the query. This can be either via the API or via a locally running model.

### Metadata

Including additional metadata can enhance the retrieval process:

- **Document Metadata**: Additional document metadata such as abstract, keywords, file names and titles may contain relevant additional information, need to be created and a decision made on how to include them. For example, titles can be added at the beginning of each chunk and embedded with the text, or they can be embedded separately their own index. If a LLM should select the right Metadata field clarify the range and describe each attribute (e.g. use Langchain [`AttributeInfo`](https://api.python.langchain.com/en/latest/chains/langchain.chains.query_constructor.schema.AttributeInfo.html))
- **Hypothetical Questions**: Generate questions for each chunk, perform queries against these questions, match them with the original chunks, and send the results to the LLM.
- **Hierarchical Indexing**:  If you have many long documents, organise them into several levels of granularity. A broad primary index for high-level categories or document summaries, combined with (multiple) indexes for fine-grained searches that contain document chunks at the lowest level.  
## 3. Storing
Efficient storage and retrieval of embeddings and documents are crucial for fast and accurate information access.
### Vector Database
In most cases you need a vector database to store your embeddings andand associated text. These are optimised for storing and retrieving high-dimensional vectors (embeddings) and allow fast similarity searches using metrics such as cosine similarity or Euclidean distance. A simple library for local storing is [Facebooks Faiss](https://github.com/facebookresearch/faiss), but in production you want to switch to a remote database like, [Milvus](https://milvus.io/) (open source) or [Weaviate](https://weaviate.io/)(open source), [Pinecone](https://www.pinecone.io/)(fully managed service) [qdrant](https://qdrant.tech/), [chromadb](https://www.trychroma.com/) or [pgvector](https://github.com/pgvector/pgvector) (vector-capable SQL database). The functionality and performance varies slightly between them,  so choose one that suits your needs and stick with it.
### Document Store
Unlike vector stores, document stores are optimised for storing and retrieving whole documents or textual data. They provide indexing and querying capabilities for text-based search and retrieval. Documents up to a scale can be stored locally or in memory as is. Databases of this type are also known as full-text search databases. Examples are [elasticsearch](https://www.elastic.co/de/elasticsearch) or [OpenSearch](https://opensearch.org/).
## 4. Querying

The idea of this step - also known as retrieval - is simple: acquire additional information to add relevant context to the user prompt. RAG is based on retrieval, which is another word for search. Retrieval is a very hard problem: the difficulty of searching, ranking and filtering to obtain a high quality collection of candidate documents for reasoning is often underestimated. This means that the balance between the amount of content to be retrieved and its relevance is crucial. Retrieving more or longer content may lead to higher costs or exceed the model's maximum input length, but it often leads to better results because the relevant information is likely to be contained somewhere.

A naive but effective initial approach is to perform a simple similarity search and return as many chunks as fit within your model's context window. However, several advanced methods can enhance this process.

### Query Transformation

If you aren't conducting a similarity search based on the entire user input, an LLM may already be transforming the user query to improve retrieval. Here are some additional techniques:

* **Decomposition**: Break down the query into multiple subtasks (e.g., at the agent level), retrieve for each subquery and build final answer from thebottom up.
* **Step-back Prompting**: Generate a more general high-level query and use both prompts to query the system.
* **Hypothetical Document Embeddings (HyDE)**: The LLM generates a hypothetical answer to the query, then queries for semantic similarity of this answer and using the retrieved chunks for generation. This method relies on answer-answer similarity rather than query-answer similarity. More details can be foud in the  [HyDE paper](http://boston.lti.cs.cmu.edu/luyug/HyDE/HyDE.pdf).

### Metadata Enhanced Search

* **User-defined Metadata Filters**: Allowing users to filter data via a front-end can significantly improve overall performance, e.g. by  filtering out old entries.
* **Self Query Retriever**: Use an LLM to reformat the query to extract semantic elements and apply metadata filters.

### Text Search

A basic approach is to check whether a word is occurs in a text and return only those instances, possibly ranked by frequency. This also depends on what approach you have taken to indexing.

* **Hybrid Search**: Combine keyword search with semantic or vector search. Use [Reciprocal Rank Fusion (RRF)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) to re-rank results that have different scores.

### Context Enrichment

Retrieve smaller chunks for better search results but add surrounding context:

* **Sentence Window**: Treat each sentence as a chunk and include a few sentences before and after.
* **Auto Merging Retriever (Parent Document Retriever)**: Search within child notes but provide the context of parent nodes. This approach retains the specificity of individual chunks for retrieval while providing broader context.

### Query Routing

If you have multiple data sources or different views of the same data source you can have automatic routing of a query. Either use a LLM Agent to determine which sources to search or use a query classifier.

### Reranking & Compression

Use the relevant parts of the retrieved chunks

* **Reranking:**  Rearranges or reduces the retrieved chunks according to either metadata (e.g. age of document), keyword or similarity score.
* **Cross-Encoder**: Check for relevance between the query and each retrieved chunk (or subchunk) by concatenating them together and then using a Transformers attention mechanism.  For example, with FlagReranker and a modern BGE-M3 model: `score = FlagReranker('BAAI/bge-reranker-base', use_fp16=True).compute_score()`. Applying a **similarity cutoff** to exclude duplicate chunks with high similarity scores could be another less computationally expensive option. See [CoiBERT](https://arxiv.org/abs/2112.01488) for more information.
* **Contextual Compressor**: Use a base retriever to obtain a large number of chunks, then use an LLM extractor to refine the information, providing only what is relevant to the generation LLM. This may involve selecting the most relevant chunks or shortening chunks by removing irrelevant information. After compression, it may be useful to re-embed the results and check their relevance to the original query. In LangChain, use `LLMChainFilter` for text filtering and `EmbeddingsFilter` to verify semantic similarity to the original query. See the [LangChain Docs](https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/contextual_compression/) for more information. Use `DocumentCompressorPipeline` together with `ContextualCompressionRetriever` in a pipeline [splitter, redundant_filter, relevant_filter].


## 5. Generation
In this final step the answers for the users are generated/synthesized. 

**Model Selection**: Choose a model that can handle the length of your retrieved context, with adequate generation quality and cost.

**Use of retrieved context**:

* **Naive**: Concatenate and feed all the retrieved context (above some relevance threshold) together with the query to an LLM at once.
* **Refine**: Iteratively refine the final output based on sub-outputs.  
* **Summarise** the retrieved context, then generate
* Generate multiple responses based on different chunks, then concatenate/summarise for final response
**System Prompt**: Describe how the model should use the provided Data
* **Reference/Citation** Achieved by a) adding the reference task to the system prompt to mention ids of sources or b) fuzzy matching parts of the generated response to the original text chunks
