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
embedding_api_url=get_os_env("EMBEDDING_API_URL", "https://infer.e2enetworks.net/project/p-580/genai/bge-large-en-v1_5/v1")
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

# set these from TIR 
llm_api_url=get_os_env("LLM_API_URL", "")
llm_api_key=get_os_env("LLM_API_KEY")

llm_client = OpenAI(
  base_url = llm_api_url, 
  api_key = llm_api_key
)

def generate_llm(query, context=None):
    prompt=query if context is None else f'{context}\n\n{query}'

    completion = llm_client.chat.completions.create(
    model='llama3_2_3b_instruct',
    messages=[{"role":"user","content":prompt}],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=1,
    stream=True
  )
    
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            return chunk.choices[0].delta.content

 
@app.get("/api/v1/chat/completions")
async def root():
    query="what is the key to survival?"
    return {"message": generate_llm(query, context=prepare_context(query))}
