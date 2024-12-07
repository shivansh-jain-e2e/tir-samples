import logging 
import contextvars
import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, root_validator, validator
from typing import Any, List, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# The headers for each request
api_request_headers = contextvars.ContextVar("headers")

app = FastAPI(
    title="gen AI Server",
    description="server template to handle ai generation requests",
    version="0.1.0",
)


ENABLE_CORS = os.getenv("ENABLE_CORS", "false").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

if ENABLE_CORS:
    # Split origins by comma
    origins = ALLOWED_ORIGINS.split(",")

    log.info(f"CORS enabled with the following origins: {origins}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

device = "cuda" if torch.cuda.is_available() else "cpu"

# TODO: edit model name here as per your requirement. 

model_name_or_path = 'meta-llama/Meta-Llama-3-8B'

# If you are using TIR model repository, and the model is fully merged (not peft or lora) then 
# set the model name to below instead by uncommenting the line. This is to make sure the loaded model 
# is from TIR model repository which downloads models to /mnt/models location before starting container.
# model_name_or_path = '/mnt/models' 
# 
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

base_model = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.float16, device_map='auto')
model = base_model 

# if you have peft model then uncomment the following. This code is expecting the fine-tuned weights (lora weights) in 
# location /mnt/models. If you have used TIR Model repository then the files will be automatically downloaded 
# to /mnt/models by TIR. But if you are uploading the weights to docker image then make sure the location is correctly set.

# from peft import PeftModel, PeftConfig
# peft_model = PeftModel.from_pretrained(base_model, "/mnt/models")
# model  = peft_model 

model = model.to("cuda")
model.eval()


@app.get("/health")
def health():
    return {"status": "ok"}


class MessageRequest(BaseModel):
    messages: str

@app.post("/v1/chat/completions")
async def chat_completion(message: MessageRequest):
    
    # here we are just using the first message for testing. In production, make sure all messages are used.
    inputs = tokenizer(message.messages[0], return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(input_ids=inputs["input_ids"].to("cuda"), max_new_tokens=100)
        print(tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0])

    return {"messages": outputs}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)