# Send Receive Test GPU-to-GPU  Between 2 nodes 

### Node 1
```
export  MASTER_ADDR=....
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
```

### Node 2

```
export  MASTER_ADDR=...
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
```
