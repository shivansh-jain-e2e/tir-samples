# Send Receive Test GPU-to-GPU  Between 2 nodes 

export  MASTER_ADDR=10.0.27.39
export MASTER_PORT=6000
export RANK=0
export LOCAL_RANK=0
export NNODES=2
export WORLD_SIZE=2

import torch
import torch.distributed as dist
torch.cuda.set_device(0)
a = torch.zeros(1, device="cuda")
dist.init_process_group("nccl")
dist.recv(a, src=1)


export  MASTER_ADDR=10.0.27.39
export MASTER_PORT=6000
export RANK=1
export LOCAL_RANK=0
export NNODES=2
export WORLD_SIZE=2

import torch
import torch.distributed as dist
torch.cuda.set_device(0)
dist.init_process_group("nccl")
a = torch.tensor([1], device="cuda")
dist.send(a, dst=0)


python3 -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role `hostname -s`: \
    --tee 3 \
    all_reduce.py
