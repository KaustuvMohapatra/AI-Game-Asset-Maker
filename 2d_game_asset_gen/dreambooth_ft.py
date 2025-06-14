import os
import json
from PIL import Image
from datasets import Dataset
import torch
from torch.utils.data import DataLoader
from transformers import CLIPTokenizer, CLIPTextModel, default_data_collator
from diffusers import StableDiffusionPipeline, UNet2DConditionModel, DDPMScheduler
from accelerate import Accelerator

# Paths
MODEL_ID = "stabilityai/stable-diffusion-2-1-base"
INSTANCE_DIR = "C:/nus_adv/training"
CAPTION_FILE = "C:/nus_adv/captions.json"
OUTPUT_DIR = "C:/nus_adv/output_model"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load captions
with open(CAPTION_FILE, "r") as f:
    captions = json.load(f)

# Load tokenizer and text encoder
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
# We'll use pipe's text_encoder instead of loading separately for consistency
# But you can load separately too if you prefer:
# text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14")

# Load pipeline (for VAE, feature extractor, and text_encoder)
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
).to(device)

vae = pipe.vae
vae.eval()
vae.to(device)

# Create dataset from images and captions
def load_dataset():
    data = []
    for filename, prompt in captions.items():
        path = os.path.join(INSTANCE_DIR, filename)
        if os.path.exists(path):
            data.append({"image": path, "prompt": prompt})
    return Dataset.from_list(data)

dataset = load_dataset()

# Preprocess dataset: resize, pixel normalize, tokenize prompts
def preprocess(example):
    image = Image.open(example["image"]).convert("RGB").resize((768, 768))
    example["pixel_values"] = pipe.feature_extractor(images=image, return_tensors="pt")["pixel_values"][0]
    example["input_ids"] = tokenizer(
        example["prompt"],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=77,
    )["input_ids"][0]
    return example

dataset = dataset.map(preprocess, remove_columns=["image", "prompt"])

train_dataloader = DataLoader(dataset, batch_size=1, shuffle=True, collate_fn=default_data_collator)

# Load UNet and noise scheduler
unet = UNet2DConditionModel.from_pretrained(MODEL_ID, subfolder="unet").to(device)
noise_scheduler = DDPMScheduler.from_pretrained(MODEL_ID, subfolder="scheduler")

# Use accelerator for mixed precision, device management, and optimization
accelerator = Accelerator(mixed_precision="fp16")
optimizer = torch.optim.AdamW(unet.parameters(), lr=5e-6)

# Prepare models and dataloader
unet, optimizer, train_dataloader, vae, pipe.text_encoder = accelerator.prepare(
    unet, optimizer, train_dataloader, vae, pipe.text_encoder
)

pipe.text_encoder.eval()  # Freeze text encoder during fine-tuning

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    unet.train()
    for step, batch in enumerate(train_dataloader):
        pixel_values = batch["pixel_values"].to(accelerator.device).to(dtype=vae.dtype)
        input_ids = batch["input_ids"].to(accelerator.device)

        # Encode images to latents
        with torch.no_grad():
            latents = vae.encode(pixel_values).latent_dist.sample() * 0.18215

        # Sample noise and timesteps
        noise = torch.randn_like(latents)
        timesteps = torch.randint(
            0,
            noise_scheduler.config.num_train_timesteps,
            (latents.shape[0],),
            device=latents.device,
        ).long()

        # Add noise to latents according to noise schedule
        noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

        # Cast noisy latents and noise to UNet dtype
        noisy_latents = noisy_latents.to(dtype=unet.dtype)
        noise = noise.to(dtype=unet.dtype)
        timesteps = timesteps.to(device=unet.device)

        # Convert input_ids to embeddings using text encoder, cast to unet dtype
        encoder_hidden_states = pipe.text_encoder(input_ids)[0].to(dtype=unet.dtype)

        # Forward pass through UNet
        model_pred = unet(
            sample=noisy_latents,
            timestep=timesteps,
            encoder_hidden_states=encoder_hidden_states,
        ).sample

        # Calculate loss
        loss = torch.nn.functional.mse_loss(model_pred, noise)

        # Backpropagation
        accelerator.backward(loss)
        optimizer.step()
        optimizer.zero_grad()

        print(f"[Epoch {epoch+1} Step {step+1}] Loss: {loss.item():.4f}")

# Save fine-tuned UNet and pipeline weights
unet.save_pretrained(OUTPUT_DIR)
pipe.save_pretrained(OUTPUT_DIR)
print(f"\nFine-tuned model saved at {OUTPUT_DIR}")
