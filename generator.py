import torch
from diffusers import StableDiffusionPipeline
from PIL import ImageDraw, ImageFont
import os

MODEL_ID = "runwayml/stable-diffusion-v1-5"
DEVICE = "cpu"

pipe = None

def load_model():
    global pipe
    if pipe is None:
        print("Loading Stable Diffusion model (first time)...")
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float32
        )
        pipe = pipe.to(DEVICE)
    return pipe


def create_visual(prompt, top_text="", bottom_text=""):
    pipe = load_model()

    image = pipe(prompt, num_inference_steps=20).images[0]
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("impact.ttf", 45)
    except:
        font = ImageFont.load_default()

    w, h = image.size

    def draw_text_with_outline(text, pos):
        x, y = pos
        for adj in range(-2, 3):
            draw.text((x+adj, y), text, font=font, fill="black", anchor="mm")
            draw.text((x, y+adj), text, font=font, fill="black", anchor="mm")
        draw.text((x, y), text, font=font, fill="white", anchor="mm")

    if top_text:
        draw_text_with_outline(top_text.upper(), (w/2, 50))
    if bottom_text:
        draw_text_with_outline(bottom_text.upper(), (w/2, h-50))

    return image