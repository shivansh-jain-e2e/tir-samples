FROM vllm/vllm-openai:v0.6.3

RUN pip install 'litellm[proxy]'

COPY  entrypoint.sh /vllm-workspace/
RUN chmod 774 /vllm-workspace/entrypoint.sh
COPY litellm-config.yaml /vllm-workspace

ENTRYPOINT ["/vllm-workspace/entrypoint.sh"]


25 
31 

