# Creating a custom model-server for object tracking using Yolov8

This is a sample model-server code for serving video based models that take videos either as input or output or both, and create model endpoints on TIR and serve API requests. To handle video inputs and outputs, we make use of EOS (E2E Object Storage) buckets.

## Pre-requisites
* **Docker Engine**: Ensure you have Docker Engine installed
* **Make**: Ensure GNU make utility is installed
* An EOS Bucket containing a video

## Steps
1. Clone this repository on your local system
    ```bash
    git clone https://github.com/tire2e/tir-sampels.git
    ```
    ```bash
    cd tir-samples/inference/yolov8/
    ```

2. ``model_server.py`` file contains the code to handle APIs and serve inference requests. In case you wish to make any changes in the inference code, do it in this file. Any third party modules or libraries that you wish to use, should be added in ``requirements.txt``

3. Create a Docker Image for this model-server and push it to your Docker Registry or E2E Container Registry using the below commands
    ```bash
    make docker-build REGISTRY=<registry> IMAGE_NAME=<image_name> TAG=<tag>
    ```
    This will create a new docker image in your local system. Here, IMAGE_NAME and TAG are optional. Push the image to your registry using the below command
    ```bash
    make docker-push REGISTRY=<registry> IMAGE_NAME=<image_name> TAG=<tag>
    ```

4. Create a new bucket in EOS, if not already created or use an already existing one. Attach a access key to the bucket. We will need the bucket_name, access_key and secret_key in next steps. 
Also, upload a video on the bucket. We will pass this video as the input and model will track the objects in this video. A sample video is provided [here](https://github.com/tire2e/tir-samples/blob/master/inference/yolov8/input-videos/traffic.mp4)

5. Create a new Inference on TIR.
    
    * Go to the Model Enpoints section
    * Create a new Endpoint by choosing the ``Custom Container`` option.
    * In the **Container Details** sub-section, add the you image repository url you created in step-3
    * In the **Environment Variables** section, add 3 environment variables with the keys: ``bucket_name``, ``access_key``, and ``secret_key``.  The keys should be exactly the ones mentioned and add the corresponding values for the bucket created in step-4
    * Deploy the inference and wait for it to be ready.

6. Once Ready, go to the **Overview** tab and copy the ``Endpoint URL``. Also copy your ``Auth Token`` from the API Tokens section and run the below curl request
    ```bash
    curl --location '<ENDPOINT_URL>/v1/models/yolov8:predict' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <AUTH_TOKEN>' \
    --data '{
        "input": "<PATH_TO_YOUR_INPUT_VIDEO_IN_BUCKET>"
    }'
    ```
    Replace the ``<ENDPOINT_URL>``, ``<AUTH_TOKEN>`` and ``<PATH_TO_YOUR_INPUT_VIDEO_IN_BUCKET>`` with your corresponding endpoint url, auth token, and you video path in the bucket.

7. You will get an ``output_file_path`` containing the path of the output video in your bucket.
