# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /e2e_rag_app

USER root

# Copy the requirements.txt file (if any) and install dependencies
COPY /app ./app

RUN pip install -r /rag/app/requirements.txt
RUN pip install e2enetworks

# Define the command to run your Python script

CMD ["python3", "/e2e_rag_app/app/main.py"]
