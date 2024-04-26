# TorchServe on TIR
TorchServe takes a Pytorch deep learning model and wraps it in a set of REST APIs. It comes with a built-in web server that you run from command line. This built-in server takes command line arguments like single or multiple models you want to serve, along with optional parameters controlling port, host and logging.

TIR makes deploying pytorch models as easy as pushing code. You can upload your torchserve model archive - more on this later - to E2E Object Storage (EOS) and thats it. TIR can automatically launch containers, download the model from EOS bucket to a local directory on container and start the torchserve web server. What you get is not only the automated containerized deployment but also monitoring and maintenance features in TIR dashboard.

**Some feature for Torchserve on TIR:**
- Rest (HTTP) and GRPC
- Automated Deployments from E2E Object Storage (EOS bucket)
- Automatic restart on failures
- E2E Managed TLS certificates
- Token based Authentication
- Manual or Automated Scaling
- Optional Persistent disks (to reduce boot time when the model downloads on restarts)
- Readiness and Liveness Checks

## FAQs
> I already have a torchserve service that works on my private server or local machine, can i migrate it to TIR? what are the steps?

Yes. You can plainly upload your mar file and config.properties to TIR Model repository and create an endpoint. TIR does not change the URL paths on the service, so all torchserve url paths (e.g. /predictions api) will be supported. 

> Does tir support torchserve api format? Do we have to change our api client to migrate to TIR?
 
No. All your API clients will work exactly as they were. The only thing you will need to change would be inference endpoint. That is - if you were using torchserve on 0.0.0.0:8080 then you would have to change this to TIR provided endpoint. The second thing you might have to add is authentication header. You can find more information on client in sample api request section below.

> Can we use GRPC?

Yes. You can use GRPC methods supported by torchserve. Once you deploy your service on TIR, you can visit Sample API request section to learn about GRPC calls. You can expect minimal changes to your client side (change of endpoint and addition of auth header).

> Can we see default metrics reported by torchserve? how about custom metrics?

TIR dashboard shows most important charts (like latency, p99, etc) that you would need along with hardware metrics reported by torchserve. The default metrics can also be used to autoscale the service when request queue goes up. You can also use custom metrics to autoscale your service. Typically we see customers using pending requests or active requests to autoscale. 


### Deployment Steps

1. Assuming that your model is in .pth format (pytorch model format), you can start by creating a model archive. Below is a sample command but you can learn more about torch model archiver [here](https://github.com/pytorch/serve/blob/master/model-archiver/README.md). If you don't have a model to perform these steps, follow the [Sample Deployment](https://github.com/tire2e/tir-samples/blob/torchserve/inference/torchserve/readme.md#sample-deployment) section ahead. 

```
torch-model-archiver --model-name densenet161 --version 1.0 --model-file ./serve/examples/image_classifier/densenet_161/model.py --serialized-file densenet161-8d451a50.pth --export-path model_store --extra-files ./serve/examples/image_classifier/index_to_name.json --handler image_classifier
```

2. Create a config file named `config.properties` using sample below. You may edit parameters as necessary. You can find list of all supported config options in torchserve here

```
# config.properties
metrics_format=prometheus
number_of_netty_threads=4
job_queue_size=10
enable_envvars_config=true
install_py_dep_per_model=true
```

3. Move both .mar file from step 1 and config.properties to a directory (e.g. `model-store`). 
4. Go to TIR Dashboard -> Select a project -> Inference -> Model Repository. Create a new model repository. Once done, you can choose from options (sdk, cli) to upload contents of your `model-store` directory (step 3) to model repository. In the background, model repository is nothing but a cloud bucket. So any files you push, will be stored as files. You can browse them as well using minio(mc) or s3-compatible cli.
5. Now, Go to Model Endpoints section and create a new endpoint. Select the torchserve as serving framework, pick the model repository (from step 4) and resources as necessary.
6. When the endpoint is ready, you can start using the service through REST API or GRPC. More details on this in following section. 



### Api Clients



### Sample Deployment 
