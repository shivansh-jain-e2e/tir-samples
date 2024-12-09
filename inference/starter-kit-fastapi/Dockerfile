FROM huggingface/transformers-pytorch-gpu:latest

# Base Image Options: Choose what fits your requirement 
# huggingface/transformers-pytorch-gpu:latest - Contains transformers latest and compatible pytorch (gpu)
# nvcr.io/nvidia/pytorch:24.11-py3 - NGC pytorch image but would require nvidia ngc registry login 
# nvidia/cuda:12.6.1-cudnn-runtime-ubuntu22.04 (base cuda image nothing else) - This will require installation of pytorch, transformers if you need them. 


RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/requirements.txt  
RUN pip install -r requirements.txt 

COPY app.py /app/

# if you have lora weights or fine-tuned model that is <25MB then you may copy it to the image itself.
# uncomment the following line to copy lora weights to /mnt/local folder in the container. 
# COPY /lora/ /mnt/models/

ENTRYPOINT ["python3", "/app/app.py"]
