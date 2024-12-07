FROM python:3.9.21-slim 

# nvcr.io/nvidia/pytorch:24.11-py3

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/requirements.txt  
RUN pip install -r requirements.txt 

COPY app.py /app/

# if you have lora weights or fine-tuned model that is <25MB then you may copy it to the image itself.
# uncomment the following line to copy lora weights to /mnt/local folder in the container. 
# COPY /lora/ /mnt/models/

ENTRYPOINT ["python3", "/app/app.py"]
