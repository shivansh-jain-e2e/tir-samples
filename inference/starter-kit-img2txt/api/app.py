import logging 
import contextvars
import os
import uvicorn
import io 

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, root_validator, validator
from typing import Any, List, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import schemas as _schemas
import services as _services

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
 
 
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/generate")
async def chat_completion(input: _schemas.ImageCreateRequest):
    image = await _services.generate_image(imgPrompt=imgPromptCreate)

    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)