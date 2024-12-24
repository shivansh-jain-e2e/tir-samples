from pathlib import Path 
import schemas as _schemas

import torch 
from diffusers import StableDiffusionPipeline
from PIL.Image import Image
import os
from dotenv import load_dotenv

load_dotenv()

# Get the token from HuggingFace 
"""
Note: make sure .env exist and contains your token
"""
HF_TOKEN = os.getenv('HF_TOKEN')

# Create the pipe 
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", 
    # revision="fp16", 
    torch_dtype=torch.float16 
    )

if torch.backends.mps.is_available():
    device = "mps"
else: 
    device = "cuda" if torch.cuda.is_available() else "cpu"

pipe.to(device)


async def generate_image(imgPrompt: _schemas.ImageCreateRequest) -> Image: 
    generator = None if imgPrompt.seed is None else torch.Generator().manual_seed(int(imgPrompt.seed))

    image: Image = pipe(imgPrompt.prompt,
                        guidance_scale=imgPrompt.guidance_scale, 
                        num_inference_steps=imgPrompt.num_inference_steps, 
                        generator = generator, 
                    ).images[0]
    
    return image