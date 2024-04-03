# LLAMA2 with TensorRT LLM
 
#### Steps
1. Launch a container to build engine
```
docker run aimle2e/tensor-rt-llm:0.7.0 sh
```



2. Build Engine: This step will convert huggingface weights to TensorRT engine. The steps are dependent on the version of tensorRT LLM. Here we are working with 0.7.0 but for other versions visit [the official repo](https://github.com/NVIDIA/TensorRT-LLM), select the version branch and go to examples > llama folder. 

- Set Huggingface to allow weights download 
```
huggingface-cli login --token  <your-hf-token-here>
```

- For Single GPU 
```
mkdir -p engine_dir
python build.py --model_dir "meta-llama/Llama-2-7b-hf" --dtype float16 --output_dir ./engine_dir --use_gpt_attention_plugin float16 --use_gemm_plugin float16 --remove_input_padding --use_inflight_batching --paged_kv_cache
```
- For Multi-GPU
You can either use tensor parallel (tp) or pipeline parallel(pp) options to split the model across multiple gpus. In this case, we are using tensor parallel and world size (gpu count) of 2. 
```
python build.py --model_dir  "meta-llama/Llama-2-7b-hf" --dtype float16 --output_dir ./engine_dir --use_gpt_attention_plugin float16 --use_gemm_plugin float16 --remove_input_padding --use_inflight_batching --paged_kv_cache --tp_size 2 --world_size 2
```

3. Push the engine to Model Repository
The above steps would create engine files in the local 
4. Create a model endpoint in TIR Dashboard


### Multi GPU
