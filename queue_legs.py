import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Specialized "Beautiful Legs" Variety Pool
POSES = [
    "crossing her long slender legs while sitting on a luxury velvet sofa",
    "walking confidently with long strides, showcasing perfectly toned legs",
    "sitting on a high bar stool with one leg dangling and the other hooked on the rail",
    "leaning against a neon-lit wall with legs elegantly posed",
    "stepping out of a luxury car, focusing on the graceful movement of her legs"
]

FOOTWEAR = [
    "stunning white stiletto high heels",
    "elegant silver strappy sandals with high heels",
    "glossy red platform heels",
    "minimalist white designer heels",
    "luxury gold-trimmed evening sandals"
]

SCENARIOS = [
    "inside a dimly lit, high-end Bangkok Gentlemen's Club with amber lighting",
    "on the vibrant, neon-drenched street of Soi Cowboy at night",
    "in the upscale atmosphere of a Thong Lo rooftop lounge",
    "against the glowing backdrop of Nana Plaza's pink neon lights",
    "near the entrance of a luxury Thai soapy massage hall"
]

# The Base Workflow (Qwen-image 2512)
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 832, "height": 1216, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_leg_focus_jobs():
    print("👠 Launching 'Elite Legs & Heels' Collection...")
    for i in range(1, 11): # 10 high-quality unique leg-focused shots
        pose = random.choice(POSES)
        shoes = random.choice(FOOTWEAR)
        place = random.choice(SCENARIOS)
        hair = random.choice(["long straight black hair", "elegant updo", "wavy dark hair"])
        
        prompt = f"Cinematic fashion photography of a stunning Thai woman with {hair}, {pose}. She is wearing {shoes} and a sophisticated outfit. Focus on her perfectly smooth, long, and elegant legs. High-resolution skin texture, matte finish, professional studio lighting, {place}. Masterpiece, 8k, detailed leather and fabric."
        
        workflow = BASE_WORKFLOW.copy()
        workflow["108"]["inputs"]["text"] = prompt
        workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_EliteLegs_{i:02d}"
        workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 999999)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Leg Focus {i:02d} queued: {shoes}")
            time.sleep(0.4)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_leg_focus_jobs()
    print("\n--- 10 'Elite Legs' tasks successfully added to the spiral! ---")
