# Triton Inference Server on TIR

## Introduction
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

### Advantages 
Using triton inference server, you can get benefits like concurrent model execution (run multiple models on same gpu) and dynamic batching to get better throughput. In addition, you also get high performance when using optimised backends like tensorRT-LLM. 

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
The server expects model configurations in config.pbtxt file under <model-name> folder in model repository. The minimum configuration required is: the backend, name, shape, and datatype of model inputs and outputs. The following is an example:

```
  platform: "tensorrt_plan"
  max_batch_size: 8
  input [
    {
      name: "input0"
      data_type: TYPE_FP32
      dims: [ 16 ]
    },
    {
      name: "input1"
      data_type: TYPE_FP32
      dims: [ 16 ]
    }
  ]
  output [
    {
      name: "output0"
      data_type: TYPE_FP32
      dims: [ 16 ]
    }
  ]
```

#### Max Batch Size
If the model's first dimension is batch dimension and each model input and output carry this dimension, then triton server can exploit this to achive dynamic or serial batching. In such cases, max_batch_size in model configuration can be used to guide the server on batching limit. 


#### Model Inputs and Outputs
The model inputs and outputs in Model configuration have a specific format. To find the naming convention, visit [here](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#inputs-and-outputs) and [here](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#inputs-and-outputs)

#### Instance Groups
You can define an instance group in model config to enable multiple instances of same model to be loaded. The sample format looks like below - 

```
 instance_group [
    {
      count: 2
      kind: KIND_GPU
    }
  ]
```

You can also use this parameter to use CPU instead of GPU. 

### Backends:
A triton backend is implementation that executes the model. A backend is mostly a wrapper around deep learning framework like Pytorch, Tensorflow, Tensor RT, ONNX runtime. You can also write your own custom backend in C++, Python. 

The current available backends include:

- [TensorRT](https://github.com/triton-inference-server/tensorrt_backend)
- [TensorRT-LLM](https://github.com/triton-inference-server/tensorrtllm_backend.git): Used to run tensorRT LLM models
- [ONNX Runtime](https://github.com/triton-inference-server/onnxruntime_backend)
- [PyTorch](https://github.com/triton-inference-server/pytorch_backend)
- OpenVINO
- [Python](https://github.com/triton-inference-server/python_backend): The Python backend allows you to write your model logic in Python. For example, you can use this backend to execute pre/post processing code written in Python, or to execute a PyTorch Python script directly (instead of first converting it to TorchScript and then using the PyTorch backend).
- vLLM: The vLLM backend is designed to run supported models on a vLLM engine. This backend depends on python_backend to load and serve models. The [vllm_backend](https://github.com/triton-inference-server/vllm_backend) repo contains the documentation and source for the backend.


### Adding Libraries and other changes to the server
TIR provides standard versions of Triton Inference Server but in case you need to add extra libraries or change the container, you can also use custom containers while launching a triton inference server. 


### Multi-Model Inference
By default, TIR loads all models into the GPU. So if you place multiple models (folders) under model repository, the models will be loaded automatically. 

### Examples
