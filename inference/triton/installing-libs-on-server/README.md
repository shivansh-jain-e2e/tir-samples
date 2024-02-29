
Installing Python Libraries on Triton Server 
############################################################################

When you are working with triton server or tensor-rt LLM backend, sometimes your inference pipeline may require additional python libraries. 

One such use case is when deploying an ensemble with LLAMA2 inference. You will need additional python dependencies like sentencepiece and protobuf. The official triton server container (e.g. 24.01-trllm-python3) does not come with these libraries. 

This document covers steps to undertake when you need to add python dependencies in your triton inference service. 


Option 1: Use pre-built requirements.tar from this repo 
==========================================================




Option 2: Prepare your own requirements.tar 
==============================================