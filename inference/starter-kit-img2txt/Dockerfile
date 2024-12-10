FROM pytorch/torchserve:0.12.0-gpu

ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/requirements.txt  
RUN pip install -r requirements.txt 

COPY api/ /app/


# if you have lora weights or fine-tuned model that is <25MB then you may copy it to the image itself.
# uncomment the following line to copy lora weights to /mnt/local folder in the container. 
# COPY /lora/ /mnt/models/

COPY entry-point.sh /app/entry-point.sh 
# RUN chmod +x /app/entry-point.sh 

ENTRYPOINT ["/app/entry-point.sh"]

