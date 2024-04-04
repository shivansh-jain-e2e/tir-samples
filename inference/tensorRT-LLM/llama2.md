# LLAMA2 with TensorRT LLM on Triton Server

Triton Server can be integrated with the [tensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) for achieving the best-in-class performance when serving large language models.  

In this tutorial, we will go through steps required to generate a llm engine (format required for triton's LLM backend) and serving the engine with TIR endpoints. 

#### Steps
1. **Launch a container to build engine**
   ```
   mkdir local
   docker run -v ./local:/local aimle2e/tensor-rt-llm:0.7.0 sh
   ```

   where `local` is the directory or file from your host system (absolute path) that you want to access from inside your container. 




2. **Build Engine**
   
   This step will convert huggingface weights to TensorRT engine. The steps are dependent on the version of tensorRT LLM. Here we are working with 0.7.0 but for other versions visit [the official repo](https://github.com/NVIDIA/TensorRT-LLM), select the version branch and go to examples > llama folder. 

- Set Huggingface to allow weights download 
  ```
  huggingface-cli login --token  <your-hf-token-here>
  ```

- Make a directory to store generated engine and config files

  ```
  mkdir -p /local/engine_dir
  ```

- For Single GPU 

  ```
   python build.py --model_dir "meta-llama/Llama-2-7b-hf" \
   --dtype float16 \
   --output_dir /local/engine_dir \
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
   --output_dir /local/engine_dir \
   --use_gpt_attention_plugin float16 \
   --use_gemm_plugin float16 \
   --remove_input_padding \
   --use_inflight_batching \
   --paged_kv_cache \
   --tp_size 2 \
   --world_size 2
  ```

   The above script will generate engine and config files in the `engine_dir`. 

3. **Prepare model repository**

   You may now exit the docker container or perform the steps inside the container as well.
  
   Download the inflight_batcher structure from the official [tensorrtllm_backend](https://github.com/triton-inference-server/tensorrtllm_backend) repo. and copy your engine file to it.
   
   ```
   git clone https://github.com/triton-inference-server/tensorrtllm_backend
   cp ./local/engine_dir ./tensorrtllm_backend/all_models/inflight_batcher_llm/tensorrt_llm/1/
   
   ```

    Using an editor, set the following parameters in the     `./tensorrtllm_backend/all_models/inflight_batcher_llm/tensorrt_llm/config.pbtxt` 

    | parameter | value |
    | --------- | ----- | 
    | gpt_model_path | /mnt/models/tensorrt_llm/1/ | 
    | model_transaction_policy.decoupled  | false | 
  
    In case you are need tokenizer, you will need to set the following parameter in `./tensorrtllm_backend/all_models/inflight_batcher_llm/preprocessing/config.pbtxt` and `./tensorrtllm_backend/all_models/inflight_batcher_llm/preprocessing/config.pbtxt`
  
    | parameter | value |
    | --------- | ----- | 
    | tokenizer_dir | meta-llama/Llama-2-7b-hf | 
  
    Now, the contents of model repository are ready. Next step is to push it to TIR. 
    
3. **Push the engine to TIR Model Repository**

   Upto this step, we have prepared a local directory with contents that Triton server expects to serve LLM model. We need     to push the local directory to TIR, so that the model can be served through TIR endpoint server (Triton Inference Server    on TIR).
   
   Go to TIR Dashboard and create a new model repository. On creation, you can find the steps to push contents to the repo.    Push the entire contents of `./tensorrtllm_backend/all_models/inflight_batcher_llm` directory to the model repo.

   At the end of this step, the TIR model repository (which is nothing a EOS bucket) should contain the following folders:  
   *preprocessing*, *postprocessing*, *tensorrt_llm*, *ensemble*

5. **Create a model endpoint in TIR Dashboard**

   You must use the GPU of same architecture that the engine was built with. For e.g. If you use A100 for building    engine then you must use the same card to launch the endpoint. 

   In model download section, 
   - For single GPU
     Choose triton server image of 23.12 as that supports 0.7.0. For other versions, do check out [support matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/)
     
   - For Multiple GPUs
     Choose triton server image of 23.12 as that supports 0.7.0. For other versions, do check out [support matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/)
     Choose world size same as that was using in step 2. It should match the available gpus. In this example, we need to select 2. 
     You can also review the mpi command that would be entry point for the container. 
