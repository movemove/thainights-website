import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# The Base Workflow
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 1216, "height": 832, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_fishbowl_jobs():
    print("Queuing Fishbowl (Goldfish Tank) selection scenes...")
    
    # Specific prompts for the "Fishbowl" experience
    fishbowl_prompts = [
        # Wide shot of the hall
        "Cinematic wide angle photography of a luxury Bangkok soapy massage grand hall. A massive 'fishbowl' glass-walled stage at the center. Dozens of stunning Thai women in elegant white silk dresses sitting on tiered red velvet steps behind the glass. High-end lighting, bright spotlights on the stage, warm ambient glow in the lobby, sophisticated and grand atmosphere, hyper-realistic textures.",
        
        # Closer look at the selection
        "A view through a large transparent glass wall in a premium Thai bathhouse. Behind the glass, a group of beautiful young Thai women with long straight hair are sitting gracefully. Some are smiling at the camera, others look sophisticated. They are wearing matching luxurious white lace outfits. Professional studio lighting, clear glass reflections, high-fashion aesthetic, photorealistic skin and fabric.",
        
        # Focus on a specific beauty in the tank
        "Medium shot of a gorgeous Thai girl sitting inside a glass-walled 'fishbowl' selection area. She is wearing a delicate white silk bikini, perfectly smooth matte skin, long wavy black hair. She is leaning against the glass, looking out with an alluring gaze. Reflections of neon lights on the glass surface. High-contrast nightlife photography, masterpiece of sensual atmosphere."
    ]

    for i, prompt in enumerate(fishbowl_prompts, 1):
        workflow = BASE_WORKFLOW.copy()
        workflow["108"]["inputs"]["text"] = prompt
        workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_fishbowl_selection_{i:02d}"
        workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + (i * 99)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Fishbowl job {i:02d} queued.")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_fishbowl_jobs()
    print("\n--- Fishbowl scenes successfully added to your RTX 5060 Ti queue! ---")
