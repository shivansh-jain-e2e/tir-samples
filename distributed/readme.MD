### Test Multi-GPU on single node 


Set Environment variables below:
```
export GPUS_PER_NODE=8
export NNODES=1
export MASTER_ADDR=localhost
export MASTER_PORT=6000 
export NCCL_DEBUG=INFO

```
Note: The master port should be open on master. Also ensure you can do passwordless ssh to other nodes from master for mult-node setups. 

```
python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role `hostname -s`: \
    --tee 3 \
    all_reduce.py
```

#### Private Clusters - 2 Nodes


Set Environment variables below:
```
export GPUS_PER_NODE=8
export NNODES=2
export MASTER_ADDR=<set-master-ip-here>
export MASTER_PORT=6000 
export NCCL_DEBUG=INFO

```
Note: The master port should be open on master. Also ensure you can do passwordless ssh to other nodes from master for mult-node setups. 

```
python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role `hostname -s`: \
    --tee 3 \
    all_reduce.py
```

#### TIR Slurm Cluster

```
GPUS_PER_NODE=8
NNODES=4
MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
MASTER_PORT=6000

python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role `hostname -s`: \
    --tee 3 \
    all_reduce.py
```
