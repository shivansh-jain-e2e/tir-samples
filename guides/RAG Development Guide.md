# RAG Development Guide

## Optimising LLM Quality 
Separating signal from noise is not easy. Hence, optimising LLMs to get exactly what you need is an iterative process. There are 3 techniques that help in this regard:
1. Prompt Engineering
2. Retrieval Augmented Generation (RAG)
3. Fine-Tuning

We will go over which to use when later in this article but this article will focus on implemeting RAG pipeline. For other techniques, please refer to other guides in this repository. 

### Prompt Engineering


## Retrival Augmented Generation (RAG)
The current LLMs are exceptional at knowledge generation and reasoning. They are trained on the publically available datasets as of a particular date. 

Now the important question is - how to augment them to learn from our private datasets?  Unlike Public datasets, our private data - in git, website, docs, internal drives - is constantly changing. There are two ways to go about this
* Retrieval Augmented Generation 
* Fine-Tuning
