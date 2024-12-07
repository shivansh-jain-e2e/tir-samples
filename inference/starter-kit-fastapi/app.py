import logging 
import contextvars
import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, root_validator, validator
from typing import Any, List, Optional

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

# This  request format is for reference only. You can change it or define as per your needs
class RequestBody(BaseModel):
    messages: List[dict] = Field(
        default=None, description="The list of messages in the current conversation."
    )
    context: Optional[dict] = Field(
        default=None,
        description="Additional context data to be added to the conversation.",
    )
    stream: Optional[bool] = Field(
        default=False,
        description="If set, partial message deltas will be sent, like in ChatGPT. "
        "Tokens will be sent as data-only server-sent events as they become "
        "available, with the stream terminated by a data: [DONE] message.",
    )
    state: Optional[dict] = Field(
        default=None,
        description="A state object that should be used to continue the interaction.",
    )

# This response object is for reference only. You may change it or define your own response format. 
class ResponseBody(BaseModel):
    messages: List[dict] = Field(
        default=None, description="The new messages in the conversation"
    )
    llm_output: Optional[dict] = Field(
        default=None,
        description="Contains any additional output coming from the LLM.",
    )
    output_data: Optional[dict] = Field(
        default=None,
        description="The output data, i.e. a dict with the values corresponding to the `output_vars`.",
    )
    state: Optional[dict] = Field(
        default=None,
        description="A state object that should be used to continue the interaction in the future.",
    )
    
@app.post(
    "/v1/chat/completions",
    response_model=ResponseBody
)
async def chat_completion(body: RequestBody, request: Request):
    # TODO: Write code to handle requests 

    return {"messages": "[\"system\": \"here is response\"]"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)