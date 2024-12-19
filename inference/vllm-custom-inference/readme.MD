# Deploy VLLM Docker Container on TIR

## Deploy LLAMA3.3-70B on 2xH100:

LLAAM3.3-70B is a large model and usually requires upto 4 GPUs (H100) to run with default settings. However, we can optimise the batch size and token length to deploy it on 2xH100 or 2xH200. 

1. Log into TIR
2. In the left side bar, locate **Model Endpoints** under **Inference**
3. Click **Create Endpoint**
4. Locate **Custom Container** from the list of frameworks and Select it. Click **Next**
5. Choose from one of the two options:

    **Skip Model Download**: Suitable when you are working with base model (not fine-tuned) and intend to fetch the model from huggingface directly
    **Link with Model Repository**: Suitable when you have a fine-tuned model or you have model stored in TIR model repository

5. Select approprirate GPU plan. Usually the math of GPU selection is based on no of parameters, token length and batch size. VLLM default batch size is 64, token length is derived from model.  For LLAMA3.3-70B-Instruct, choose atleast 2xH100 or 2xH200
  
6. In the **Resource section**, edit storage size (persistent) to 300GB as the model is fairly large. Using persistent storage improve restart times we the model need not be downloaded again. Click **Next**

7. In **container configuration**, 
   * Image: Enter `vllm/vllm-openai:latest`
   * Click the checkbox for HTTP Port 
   * Click on **Advanced Configuration**
   * Enter following parameters
      * Command: `["python3","-m","vllm.entrypoints.openai.api_server"]`
      * Args: `["--model","meta-llama/Llama-3.3-70B-Instruct","--port","8080","--tensor-parallel-size","2","--max-model-len","100","--max-num-seqs","16"]`

      ![alt text](https://github.com/mindhash/tir-samples/blob/master/inference/vllm-custom-inference/container-config.png?raw=true) 

   * Click **Next**
8. Go through rest of the steps to deploy the container. 
9. Moniter the deployment using tabs `Deployment Events` and `Logs`. Please note, we did not set a health check on this container, so you may see the state of endpoint as running but actual endpoint will be active only when the model is loaded and log shows that the HTTP:PORT is running.  Please moniter logs carefully to confirm your endpoint is ready to access new requests
9. When endpoint is ready, you can find sample API calls by clicking `API request` for respective endpoint. 
     ![alt text](https://github.com/mindhash/tir-samples/blob/master/inference/vllm-custom-inference/endpoints.png?raw=true) 
