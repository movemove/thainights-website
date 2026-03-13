import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🦶 Specialized "Beautiful Feet" Detail Pool
FEET_PROMPTS = [
    "Extreme close-up of a stunning Thai girl's feet, she is wearing elegant white high heels, one foot partially stepping out of the shoe to reveal a high graceful arch and smooth sole",
    "Detailed shot of beautiful bare feet resting on a dark velvet cushion, perfect toes with light pink nail polish, soft matte skin texture, warm ambient lighting",
    "Focus on the feet of a Thai woman wearing strappy silver sandals, the thin straps crossing over her smooth instep, highlighting her delicate ankle and heel",
    "A provocative shot of a girl's foot dangling a white stiletto heel from her toes, cinematic lighting, focus on the texture of the skin and the curve of the foot",
    "Feet特寫: Beautiful Thai girl's feet resting on a glass table with neon reflections, soft focus on the toes and arches, high-fashion aesthetic"
]

# The Base Workflow (Qwen-image 2512)
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 1024, "height": 1024, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_feet_jobs():
    print("🦶 Launching 'Beautiful Feet & Toes' Special Collection...")
    for i in range(1, 11):
        detail = random.choice(FEET_PROMPTS)
        skin = random.choice(["exotic tanned", "fair porcelain", "natural matte"])
        
        prompt = f"Cinematic macro photography of 1woman, {detail}. She has {skin} skin. High-resolution textures, hyper-realistic, professional studio-level lighting, depth of field with heavy bokeh, masterpiece, 8k."
        
        workflow = BASE_WORKFLOW.copy()
        workflow["108"]["inputs"]["text"] = prompt
        workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_FeetDetail_{i:02d}"
        workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 999999)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Foot Detail {i:02d} queued.")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_feet_jobs()
    print("\n--- 10 specialized 'Beautiful Feet' tasks are now in your ComfyUI queue! ---")
