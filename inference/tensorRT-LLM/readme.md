# TensorRT LLM Backend

TIR offers native support for highly optimised LLM serving through TensorRT LLM backend.  

### Steps 
- Create TensorRT LLM Engine
- Upload the engine to TIR Model Repository
- Launch a Model Endpoint for the repository (created in step 2) 

### Building an engine 
TensorRT LLM requires you to create an engine on the same type of GPU architecture (e.g. A100). There is also a dependency of Triton Backend (TensorRT LLM Backend) with TensorRT versions. To avoid all the dependency hassles, you can use the following docker images to generate your engine and push them to model repository. 
| Version                      | Engine Builder Image        |
| -----------------------------| --------------------------- |
| TensorRT LLM Backend (0.8.0) | aimle2e/triton_trt_llm:0.8.0  |
| TensorRT LLM Backend (0.7.2) | aimle2e/triton_trt_llm:0.7.2  |
| TensorRT LLM Backend (0.7.0) | aimle2e/triton_trt_llm:0.7.0  |

We do not recommend using main or master branch of tensorRT repo to generate engine as it may not be in sync with TensorRT LLM Backend. You may use any released versions of TensorRT LLM Backend instead of versions provided above.  

### Examples
- [Single GPU](llama2.md)
- [Multi GPU](llama2.md)

For more examples, visit the official [TensorRT LLM Backend Repo](https://github.com/triton-inference-server/tensorrtllm_backend).
