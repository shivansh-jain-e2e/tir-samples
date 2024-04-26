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
> Does tir support torchserve api format? Do we have to change our api client to migrate to TIR?
 
No. All your API clients will work exactly as they were. The only thing you will need to change would be inference endpoint. That is - if you were using torchserve on 0.0.0.0:8080 then you would have to change this to TIR provided endpoint. The second thing you might have to add is authentication header. You can find more information on client in sample api request section below.

> Can we use GRPC?

Yes. You can use GRPC methods supported by torchserve. Once you deploy your service on TIR, you can visit Sample API request section to learn about GRPC calls. You can expect minimal changes to your client side (change of endpoint and addition of auth header).

> Can we see default metrics reported by torchserve? how about custom metrics?

TIR will show important charts like latency, p99, etc based on default metrics along with hardware metrics reported by torchserve. The default metrics can also be used to autoscale the service when request queue goes up. You can also use custom metrics to autoscale your service. Typically we see customers using pending requests or active requests to autoscale. 
