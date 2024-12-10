# Starter kit for LLM inference + Fast API on TIR

### Steps
1. Clone the repo.
```
git clone https://github.com/mindhash/tir-samples
cd tir-samples/inference/starter-kit-img2txt
```


2. [optional] Add lora weights to lora folder. If you have fine-tuned model, then put the model weights in lora folder and uncomment the following line in docker. 


```
# in Dockerfile 
# COPY /lora/ /mnt/models/
```

NOte: This method works for small models. For larger ones, we recommend using model repository in TIR. 

3. Add API handling code in `app` folder.  Make sure you put correct location for model.  That is, huggingface ID if you intend to download the model from huggingface, or `/mnt/models` if you use TIR model repository to host your model. 
 
4. Build the docker image 

```
docker build --platform linux/amd64 -t my-app:0.1 . 
```

5. Push docker image to docker hub or private repository (can be created in TIR). In this example, we will push the image as public in docker hub.

```
docker tag my-app:0.1 <your-docker-handle-here>/my-app:0.1

```

6. Go to Inference >> Model Endpoints section and follow the steps to create an endpoint. Choose `Fast API` or `Custom Container` as serving framework option. When prompted, use the image and tag from step 5.  

Make sure you add environment variable HF_TOKEN  and set it to huggingface auth token. This will allow your container to download models from huggingface during deployment. 

7. Once Endpoint is ready, test it using open ai client or curl. 
