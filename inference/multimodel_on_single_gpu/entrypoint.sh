#!/bin/bash

set -e

echo "starting vlm1 "

nohup python3 -m vllm.entrypoints.openai.api_server \
  --model=meta-llama/Llama-3.2-1B-Instruct \
  --port=8001 \
  --max-num-batched-tokens=2048 \
  --max-model-len=2048 \
  --max-num-seqs=1 \
  --scheduling-policy=priority \
  --enable-chunked-prefill=true \
  --gpu-memory-utilization=0.5 > /var/log/llm1 2>&1 &

echo "starting vlm2 "
nohup python3 -m vllm.entrypoints.openai.api_server \
  --model=meta-llama/Llama-3.2-1B-Instruct \
  --port=8002 \
  --max-num-batched-tokens=100 \
  --max-model-len=100 \
  --max-num-seqs=5 \
  --scheduling-policy=priority \
  --enable-chunked-prefill=true \
  --gpu-memory-utilization=0.5 > /var/log/llm2 2>&1 &


# tail -f /dev/null

litellm --port 8080 --config /vllm-workspace/litellm-config.yaml --detailed_debug