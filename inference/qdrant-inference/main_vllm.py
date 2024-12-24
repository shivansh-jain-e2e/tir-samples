import os 

from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from openai import OpenAI
app = FastAPI()

def get_os_env(name, default=None):
    try:
        return os.environ[name] 
    except:
        return default 

# This sample uses hosted qudrant db from TIR but you may replace it if necessary. 
qdrant_api_key = get_os_env("QDRANT_API_KEY")  # Get your api-key from TIR 
qdrant_host_url = get_os_env("QDRANT_HOST_URL") # Get your host url from tir dashboard

qdrant_client = QdrantClient(host=qdrant_host_url, port=6333, api_key=qdrant_api_key)

# This sample uses Embedding API from genAI API provided by TIR. You may replace this if necessary.  
embedding_api_url=get_os_env("EMBEDDING_API_URL", "")
embedding_api_key=get_os_env("EMBEDDING_API_KEY")
embedding_model=get_os_env("EMBEDDING_MODEL", 'bge-large-en-v1_5')

embedding_client =  OpenAI(
  base_url = embedding_api_url, 
  api_key = embedding_api_key
)

def generate_embedding(source_text, model):
    embeddings = embedding_client.embeddings.create(input=source_text, model=model, encoding_format="float").data[0].embedding
    return embeddings

def prepare_context(source_text):
    source_text_embedded = generate_embedding(source_text, embedding_model)
    search_results = embedding_client.search(collection_name=collection_name, query_vector=source_text_embedded, limit=3)
    context = []
    if len(search_result)> 0 :
        for i in search_result:
            context.append(search_result[i]['ScoredPoint'].payload['text'])
    return context

from vllm import LLM, SamplingParams

# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm_model_name ="meta-llama/Meta-Llama-3.1-70B-Instruct" 

# Create an LLM.
llm = LLM(model=llm_model_name)

def generate_vllm(query, context=None):
    prompt=query if context is None else f'{context}\n\n{query}'

    # Generate texts from the prompts. The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    outputs = llm.generate([prompt], sampling_params)
    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
        return generated_text

@app.get("/api/v1/chat/completions")
async def root():
    query="what is the key to survival?"
    return {"message": generate_vllm(query, context=prepare_context(query))}
