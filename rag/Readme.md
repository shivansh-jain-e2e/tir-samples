# Creating a pipeline for inserting embedding of text in Qdrant database

This is a basic sample pipeline code where text data is fetched from EOS buckets, vector embedding are generated from TIR GenAI API and it is then inserted in Qdrant a vector database.

## Pre-requisites
* **Docker Engine**: Ensure you have Docker Engine installed
* An EOS Bucket containing text files
* A Qdrant database
* TIR API token

## Steps
1. Clone this repository on your local system
    ```bash
    git clone https://github.com/tire2e/tir-sampels.git
    ```
    ```bash
    cd tir-samples/rag/
    ```

2. ``app/main.py`` file contains the code to handle EOS and Qdrant API calls. In case you wish to make any changes in the inference code, do it in this file. Any third party modules or libraries that you wish to use, should be added in Dockerfile install RUN pip install command

3. Create a Docker Image for this pipeline code and push it to your Docker Registry or E2E Container Registry using the below commands
    ```bash
    make docker-build REGISTRY=<registry> IMAGE_NAME=<image_name> TAG=<tag>
    ```
    This will create a new docker image in your local system. Here, IMAGE_NAME and TAG are optional. Push the image to your registry using the below command
    ```bash
    make docker-push REGISTRY=<registry> IMAGE_NAME=<image_name> TAG=<tag>
    ```

4. Change the image name in ``pipeline.yaml`` to the name of the image you just generated.

5. Setting up a Bucket
    * Create a new bucket in EOS, if not already created or use an already existing one. Attach a access key to the bucket. We will need the bucket_name, access_key, path_prefix and secret_key in next steps.
    * Also upload the txt files on the bucket. We will use these files to generate vector embeddings and insert them in Qdrant.

6. Create a new pipeline on TIR

    * Go to the Pipeline section
    * Create a new pipeline by choosing the ``CREATE PIPELINE`` option
    * Upload the ``pipeline.yaml``
    * Now create a run with pipeline you just created.
    * Enter all the parameters and launch the run with your prefered configuration.

7. You can see the run logs and qdrant dashboard too see the progress.
