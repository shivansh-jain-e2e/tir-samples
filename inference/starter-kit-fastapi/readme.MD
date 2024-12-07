# Starter kit for LLM inference + Fast API on TIR

### Steps
1. Clone the repo 
   ```
   git clone https://github.com/mindhash/tir-samples
   ```

2. [optional] Add lora weights to lora folder. If you have fine-tuned model, then put the model weights in lora folder and uncomment the following line in docker 

   
   ```
   # COPY /lora/ /mnt/models/
   ```

3. Add API handling code in `app.py`. 

4. Build the docker image 
   
   ```
   docker build --platform linxu/amd64 -t my-app:0.1 . 
   ```

5. Push docker image to docker hub or private repository (can be created in TIR). In this example, we will push the image as public in docker hub.

   ```
   docker tag my-app:0.1 <your-docker-handle-here>/my-app:0.1
   
   ```

6. Go to Inference >> Model Endpoints section and follow the steps to create an endpoint. Choose `Fast API` or `Custom Container` as serving framework option. When prompted, use the image and tag from step 5.  
   Make sure you add environment variable HF_TOKEN  and set it to huggingface auth token. This will allow your container to download models from huggingface during deployment. 

7. Once Endpoint is ready, test it using open ai client or curl. 
