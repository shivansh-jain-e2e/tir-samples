# LLAMA2 with TensorRT LLM
 
#### Steps
1. **Launch a container to build engine**
   ```
   docker run -v <your-local-dir>:/local aimle2e/tensor-rt-llm:0.7.0 sh
   ```



2. **Build Engine**: This step will convert huggingface weights to TensorRT engine. The steps are dependent on the version of tensorRT LLM. Here we are working with 0.7.0 but for other versions visit [the official repo](https://github.com/NVIDIA/TensorRT-LLM), select the version branch and go to examples > llama folder. 

- Set Huggingface to allow weights download 
  ```
  huggingface-cli login --token  <your-hf-token-here>
  ```

- Make a directory to store generated engine and config files

  ```
  mkdir -p /local/engine_dir/tensorrt-llm
  ```

- For Single GPU 

  ```
   python build.py --model_dir "meta-llama/Llama-2-7b-hf" \
   --dtype float16 \
   --output_dir /local/engine_dir/tensorrt-llm \
   --use_gpt_attention_plugin float16 \
   --use_gemm_plugin float16 \
   --remove_input_padding \
   --use_inflight_batching \
   --paged_kv_cache
  ```

- For Multi-GPU

  You can either use tensor parallel (tp) or pipeline parallel(pp) options to split the model across multiple gpus.   In this case, we are using tensor parallel and world size (gpu count) of 2. 

  ```
   python build.py --model_dir  "meta-llama/Llama-2-7b-hf" \
   --dtype float16 \
   --output_dir /local/engine_dir/tensorrt-llm \
   --use_gpt_attention_plugin float16 \
   --use_gemm_plugin float16 \
   --remove_input_padding \
   --use_inflight_batching \
   --paged_kv_cache \
   --tp_size 2 \
   --world_size 2
  ```

The above script will generate engine and config files in the `engine_dir`. In case you wish to use inflight_batcher from tensorRT LLM backend, you can follow the steps [in the official repo](https://github.com/triton-inference-server/tensorrtllm_backend) to prepare model repository. 

3. **Push the engine to Model Repository**

 You can create a model repository in TIR dashboard and follow the instructions to push contents of `engine_dir` to  the model repository. 

5. **Create a model endpoint in TIR Dashboard**

   You must use the GPU of same architecture that the engine was built with. For e.g. If you use A100 for building    engine then you must use the same card to launch the endpoint. 

   In model download section, 
   - For single GPU
     Choose triton server image of 23.12 as that supports 0.7.0. For other versions, do check out [support matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/)
     
   - For Multiple GPUs
     Choose triton server image of 23.12 as that supports 0.7.0. For other versions, do check out [support matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/)
     Choose world size same as that was using in step 2. It should match the available gpus. In this example, we need to select 2. 
     You can also review the mpi command that would be entry point for the container. 
