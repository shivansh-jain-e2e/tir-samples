# Triton Conceptual Guide
This conceptual guide aims to educate developers on challenges and understanding required when deploying models on triton inference server. 

### Deploying Multiple Models
The key challenge for ML/AI teams is to build infrastructure that caters to different type of models (pytorch, tensorflow, onnx, etc) and at the same time utilises the same underlying resources (like GPU). For example, one of your model may require pytorch and other is built with tensorflow, these two can have different workloads, may have different queues, etc. 

The triton inference server caters to such needs. You can start with a single or Pool of GPUs and share them for all your models. You can load multiple versions of same models as well to allow maximum utilization of GPUs. To learn more about the architecture of triton inference server, click here. 

In the rest of this article, we will deploy a triton service in TIR that would serve multiple models. The steps would include:
- Set up Model Repository
- Model Configuration
- Launching Server in TIR
- Building Client Application

At the end of this section, we will also cover some of the operational aspects:
- Pre and Post-Processing Steps
- Loading & Unloading Models 
- Model Versioning 
- AutoScaling 

### Pre and Post-Processing Steps
