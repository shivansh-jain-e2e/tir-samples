# RAG Development Guide

Separating signal from noise is not easy. Hence, optimising LLMs to get exactly what you need is an iterative process. There are 3 techniques to know in this regard:
1. Prompt Engineering
2. Retrieval Augmented Generation (RAG)
3. Fine-Tuning

This article will briefly cover the topics briefly but the main focus will be on implemeting RAG pipeline. For other techniques, please refer to other guides in this repository. 

### Prompt Engineering
The LLMs work with a single text input, often referred to as prompt since it contains instructions and sets expectations with the model to achieve a desired result.  The following is a simple prompt:

```
Generate some book titles that I can use for a scince fiction novel. 
```

As you interact with LLMs with different format of prompts you will realise, the way of communication matters. It is similar to how we interact with people of different ages and backgrounds.  hence, the process of generating a desired result from prompt requires experimentation and iterations.

It is common for developers to iterate and define a prompt that works for a usecase and use the exact same set of prompts in a production setting. 

Lets take an example of product review page that shows summary of reviews.  From develoment perspective, there is only one action expected from the LLM. So just defining a simple prompt in following way would suffice. 

```
reviews = [..] 
prompt = f"Summarise the given user reviews below. Each review is presented as a separate bullet point. Pay more attention to negative reviews. 

{reviews}"

# call LLM with prompt 
```

As you can see, one can define prompt templates of above format to achieve different use case. The implementation gets more complicated when LLMs interact with a user through chat - because we work with user input and not well-defined functions like above.  

### Retrival Augmented Generation (RAG)
The current LLMs are exceptional at knowledge generation and reasoning. They are trained on the publically available datasets as of a particular date. 

Now the important question is - how to augment them to learn from our private datasets?  Unlike Public datasets, our private data - in git, website, docs, internal drives - is constantly changing.  

RAG enables augmenting prompts with information from your internal systems and databases. The review summary example that we have seen earlier is simplest case. We know what the model would need reviews, we can pull them up and add to the prompt. But, one caveat here is we are always limited by the context length of model. 

What is context length? We can think of it like a short term memory of large language models. And being short, it has a limit. For most top performing models, it is around 8192 (chars). 

Now that we know the capability of prompts and the context length, it should be clear that we can't throw all of our documents and records at the model, we need to be selective. This is where smart retrieval (of information) becomes necessity. Something vector search helps with.  

### Fine-Tuning 
If RAG covers the aspect of `what models needs to know`, fine-tuning takes care of `how model needs to act`. Models are not often good at following instructions. For example, when a text generation model (like LLAMA3) - that is capable of generating text - is expected to generate code, it needs to be fine-tuned to learn the nuances of code formatting and styles. The context length wouldn't be enough to cover this aspect.  


## Build RAG Pipeline Usecase: Chat with data 
Now that we have covered the basics of improving LLM quality, lets start by building a simple RAG based flow. 


#### Step 1: Create LLAMA3 Model Endpoint 
As a pre-requisite, we must have an endpoint ready that can respond to the prompts. 

![image](https://github.com/mindhash/tir-samples/assets/10277894/ccb6d13c-f9f3-4e45-8a1f-a45dc702cb18)

Follow these steps to launch a LLAMA3 endpoint in TIR. You may choose any other model like LLAMA2 or Mistral as well. 
1. Go to **TIR Dashboard**. Select an existing or create a new project.
2. Go **Inference** > **Model Endpoints** section. Click on **Create Endpoint**
3. In **Model Download** section, Select the option **Download from Huggingface**, if not selected already
4. In the **Model** field, enter *meta-llama/Meta-Llama-3-8B-Instruct*. Leave Tokenizer field empty
5. In the resource section, choose one of the following GPU plans: H100, L4, A10080, A10040. Depending on the availability, you can choose any of these
6. Keep Clicking Next until you reach **Environments** sections
7. Enter your huggingface token for HF_TOKEN key. This will set your huggingface token while downloading the model in the container.
8. Click **Finish** to complete the endpoint creation

The endpoint will take a while depending on the size of the model. Review events and logs tab to monitor the deployment. 

#### Step 2: Launch RAG API Server 

The interactions with inference endpoint can happen through two arhictectural patterns: (i) Agent (Client) (ii) API Server


(1) Agent interacts with Knowledge base and LLM
![image](https://github.com/mindhash/tir-samples/assets/10277894/c71f00f4-b584-4e4a-960c-87b08e637405)

(2) API Server interacts with knowledge base and LLM
![image](https://github.com/mindhash/tir-samples/assets/10277894/65461e72-053d-4f10-b1a7-0d8ac27096a1)

In this article, we will focus on API server approach. Our users will interact with the API server through a browser, hence we need to ensure API server co-ordinates the request between user and LLM endpoint. 



