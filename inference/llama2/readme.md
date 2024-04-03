# Deploy LLAMA2 on TIR

TIR supports two options to serve LLAMA2 model out-of-box. Optional you can also create your own custom container and use any format of your choice.

1. [Using TensorRT LLM format (recommended for best performance)](https://github.com/mindhash/tir-samples/blob/amol/triton-client-samples/inference/tensorRT-LLM/llama2.md)

2. **Using Hugginface Format**
   - Go to TIR Dashboard. Select a project. 
   - Create a model Repository in TIR
   - Copy fine-tuned weights (LORA) to the Model Repository 
   - Create a Model Endpoint with framework 'LLAMA2-HF-7B-CHAT'. You can choose this option irrespective of your model type (7b,13b, 70b)
  

# Fine-Tuning LLAMA2 on TIR
You can also use fine-tuning UI in TIR to automatically generate a training script, train the model on your dataset (with LORA) and deploy it with a few clicks. Read here to learn more about fine-tuning options in TIR
