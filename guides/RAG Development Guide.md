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

In this article, we will focus on API server approach. Our users will interact with the API server through a browser, hence we need to ensure API server co-ordinates the request between user and LLM endpoint. The conversation API server would be responsible for managing dialgues with the user, as well as preparing prompt + context request for the LLM. 

Let us first go through implementation considerations for this architecture:

* **Knowledge Base** refers to content in its source format like markdown, docx, pdf etc.  While it may be desirable to directly read from the source documents, the process is not going to be optimal. Hence, the documents will need to be converted to a format (vector embedding) and loaded into vector database. The idea here is to create fragments of the document and store them separately. This would help our API server to only pick relevant fragments (or chunks) in the LLM prompt (request).  
  
  You can imagine how this would work, if you have solved reading comphrehension in highschool exams. We read a question, jumpt to appropriate paragraph that might have an answer and read it through. Thats what is happening here with combination of knowledge base and vector search.  
  
  The important questions to be answered though is how to fragment a given document and how to organize these fragments. 


* **Vector search** solves the second part of equation. Which part of fragment (or chunk) is important for the question asked by the user.  There are plenty of vector databases in the market. You can choose from qdrant, milvus, chroma for server side deployments. On the other hand, when you have only a few documents to work with then something like Annoy works well as well. It is in-memory vector search and doesnt need a separate server. 

* **Conversation history**
The interaction with LLM is always stateless. LLMs dont keep a tab of users. This demands a special consideration of capturing the conversation history between user and the bot. The history will be shared with LLM on each request to keep it appraised of what happened so far in the dialogue. 
  We will need a way to store the history for each user session. This can happen on client (browser's localstorage or react state) or the server side (redis or other dbs).

* **Prompt building**
All consideration so far have been about capturing information that would help LLM make right judgement. But for that to happen, we also need to present that information in a format that is understandable for the LLM.  We also need to make sure, the bot does not go out of the way to answer questions on  things like politics, social issues etc. We need it to stick to our current set of documents only. 

* **LLM Interaction**
In a RAG pipeline, LLM can serve multiple purposes. Not just answer user query but also to understand it. For example, one way to avoid answering questions on politics would be to ask LLM itself if the question has a political inclinations and use that answer to decide the next course of actions. So while most RAG pipelines show LLM at the end of the flow, in reality it stands at the center of it.   


Now that we have looked into several considerations for a conversation API server, we have two ways to go about these. 
(i) Develop our own web server (fast or flask api) using tools like langchain, langfuse or our own frameworks 
(ii) Use Nemo Guardrails 

While option 1 is interesting it is also time consuming and demands skillsets in writing a chat server. Nemo guardrails does work better for our usecase. Lets go through the considerations again and see how guardrails would address them. 

* **Knowledge Base**: The guardrails server can automatically convert markdown content to chunks (fragments) and also load it into vector database. It performs this action at the start of server, so if the dataset is huge, there is option to perform the vector db upload externally. 

* **Vector search**: The guardrails server can work with annoy by default but also supports other databases like qdrant. In this tutorial, we will cover both the options. 

* **Conversation history**: You can store the conversation history in guardrails or choose to do it on the client side.  For the sake of simplicity, we will expect client to keep tab on history and send it with each request. 

* **Prompt building**: By default, guardrails comes with prompts that combine user conversations, document chunks (obtained from vector db) and other inputs. We will start with default prompt and modify it down the line as needed.

* **LLM Interaction**: We will use an external TIR model endpoint created in prior step for inference. This would require setting up the endpoint url, auth token and model name in guardrails configuration. 

##### 2.1 Setup a Knowledge Repository
 
1. Create a new directory on your local machine called `rag` (or any name of your choice)
2. Create another directory inside rag called `kb` (this name must not change)
3. Create a file named `config.yml` in `rag` directory
4. Copy your  documents in markdown format (.md) to `kb` folder. These documents will be split into chunks and loaded in vector db when the nemo guardrails server starts
5. Configure the `config.yml` with following contents. You may edit the general instructions as necessary.
   
```
instructions:
  - type: general
    content: |
      Below is a conversation between a user and a bot called the TIR Bot.
      The bot is designed to answer questions about an AI development platform called as TIR. 
      The bot is knowledgeable about the features that TIR provides. 
      
      The bot does not use any external sources to answer any questions. Only use the knowledge base for any responses. Very important.
      If the bot does not know the answer to a question, it truthfully says it does not know.
models:
  - type: main
    engine: vllm_openai
    parameters:
      openai_api_base: <ENTER_TIR_ENDPOINT_HERE> 
      openai_api_key: <ENTER_TIR_API_TOKEN_HERE> 
      model_name: "meta-llama/Meta-Llama-3-8B-Instruct"
```

6. This setup assumes you are using LLAMA3-8B model but change the model name above if you are using any other models
7. To get TIR endpoint and api token, locate your model endpoint (that would serve LLAMA3) in TIR dashboard. Click on **API Request** to get both endpoints and token.

    <img width="1100" alt="image" src="https://github.com/mindhash/tir-samples/assets/10277894/12410c96-f98c-498e-9561-e10be59abc09">

8. Make sure `openai_api_base` and `openai_api_key` in the `config.yml` are in exact format as below:
   * openai_api_base: **https://infer.e2enetworks.net/project/{project}/endpoint/{inference-id}/v1/** (notice this ends with /v1)
   * openai_api_key: eyddfef....


##### 2.2 Upload a Knowledge Repository
1. Go to **Model Repository** in **TIR Dashboard**. You will locate it under **Inference** menu in the sidebar.
2. Click **New Repository**
3. Enter a suitable name like `product-docs-knowledge-base` and create the repository
4. Once Repo is created, Use SDK or CLI option to upload the contents `rag` folder to the repository
5. When upload is complete, go to Select this repository in TIR Dashboard and Click on **Model files** tab. Confirm that the uploaded files and folders (from rag folder) can be seen in the repository.
   
   ![image](https://github.com/mindhash/tir-samples/assets/10277894/7f1d1260-ffad-45ea-b515-8cf962811914)


##### 2.3 Launch Guardrails Server (Conversation API Server)
1. Go to **Model Endpoints** in **TIR Dashboard**. You will locate it under **Inference** menu in the side bar.
2. Click **New Endpoint**
3. On the Next screen (Choose Framework), select **Custom Container** as framework
4. On the Next screen you will find multiple sections. Below is the information you can enter to launch the guardrails server
   4.1 Model Download:
   * Choose **Link to Model Repository** option.
   * And select the model repository (e.g. `product-docs-knowledge-base`) created in step 2.2.
   * Leave the model path field empty
   4.2  
