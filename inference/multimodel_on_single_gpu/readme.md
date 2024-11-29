# Deploy multiple models on same GPU 

This configuration would allow deploying multiple models on a single GPU and same endpoint in TIR. It avoids the need for a proxy like ngnix or haproxy. 

### Steps:
- Edit the entrypoint.sh to start multiple vllm servers as desired. each for a separate model. In this example, we have same model but you may choose different models. The important parameters for each vllm instance are gpu-memory-utilization, max-num-batched-tokens, max-model-len to make sure your GPU consumption doesnt exceed a certain limit. 
- Edit the litellm_config.yaml to route the requests based on model names.
- Build the docker container with `docker build --platform linux/amd64 -t <image-name> .`
- Push the docker to a public repo or TIR docker registry
- Go to TIR dashboard> Inference >> Model Endpoints. Create a new endpoint, look for `Custom Container` in framework list.
- Choose Custom Container, follow the steps. Choose the image created above when prompted.
- In environment variables section, add HF_TOKEN=<your huggingface token> as this will be needed by vllm for downloading the model
- Deploy endpoint

### Test:
Before we test we need auth token and endpoint url from tir dashaboard. 

**Auth token:**
Go to TIR dashboard, local API tokens in side bar. Create a new token if necessary.  Copy the auth token from `Auth token` column. 
  <img width="1199" alt="image" src="https://github.com/user-attachments/assets/a06cb5af-ea16-4e44-bc5b-b62008e30933">
**Model Endpoint URL**
Go to Inference >> Model Endpoint. Locate your endpoint and click on it. You can find the endpoint url in overview section (as shown below).
  <img width="756" alt="image" src="https://github.com/user-attachments/assets/eec9b094-1457-4b8e-9e29-e1012eddbe0f">

- Edit the token from previous step (from the curl request).
```
import openai

# You can get auth token from API Token section on TIR Dashboard
TIR_TOKEN = "<token>"   

openai.api_key = <ENTER_TIR_TOKEN_HERE>

openai.base_url = "<ENTER_TIR_ENDPOINT_HERE>/v1/llama2/"  <- note the model name here.  In the litellm configuration, we had set 2 routes. one called llama1 and other llama2. 

completion = openai.chat.completions.create(
    model="meta-llama/Llama-3.2-1B-Instruct",
    messages=[
       {"role": "user", "content": "program for checking wheather the number is prime"},
    ],
)

print(completion.choices[0].message.content)
```
  
 


