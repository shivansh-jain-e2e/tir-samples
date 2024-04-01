# Triton Inference Server on TIR

### Advantages 
Using triton inference server, you can get benefits like concurrent model execution (run multiple models on same gpu) and dynamic batching to get better throughput. In addition, you also get high performance when using optimised backends like tensorRT-LLM. 

## Concepts
The key challenge for ML/AI teams is to build infrastructure that caters to different type of models (pytorch, tensorflow, onnx, etc) and at the same time utilises the same underlying resources (like GPU). For example, one of your model may require pytorch and other is built with tensorflow, these two can have different workloads, may have different queues, etc. 

The triton inference server caters to such needs. You can start with a single or Pool of GPUs and share them for all your models. You can load multiple versions of same models as well to allow maximum utilization of GPUs.  

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

### Concepts and Architecture 

#### Concurrent Execution and Request Queues
The idea behind concurrent model execution is to maximize GPU utilization. For example, if you have 80GB gpu memory, then you can either load multiple versions of your 40GB or two different models as well. Triton server takes care of request queues. By default, a request queue is created for each model.  When multiple requests arrive for same model, the triton server schedules them in serialised manner. 

![image](https://github.com/mindhash/tir-samples/assets/10277894/79dc6a80-d35c-4e03-97f1-8bc0c769cbcc)


[Image Source](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/architecture.md)

#### Model Repository
Typically, Triton server loads models from a single diretory. It is called as Model Repository. Within this directory, you can have multiple sub-directories - one for each model. 

Structure of Model Repository:
```
 <model-repository-path>/
    <model-name>/
      [config.pbtxt] 
      <version>/
        <model-definition-file> 
      ...
    <model-name>/
      [config.pbtxt] 
      <version>/
        <model-definition-file>
      <version>/
        <model-definition-file>
```

#### Model Configuration

## 

### Adding requirements.txt 

### Multi-GPU Setup 

### Backends:

#### Python Backend

#### Tensor-RT LLM 


### Examples
