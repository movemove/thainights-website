import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Hourglass Body Variety Pool (Busty + Slender Waist)
BODY_TYPE_PROMPTS = [
    "voluptuous bust with an extremely slender snatched waist",
    "stunning hourglass figure, large breasts and flat stomach",
    "curvy physique with a very slim waistline and voluptuous chest",
    "perfectly proportioned body, busty with a narrow tiny waist",
    "graceful yet provocative body shape, emphasizing the contrast between chest and waist"
]

OUTFITS = [
    "skin-tight white bodycon dress highlighting the waist",
    "black corset with white lace detailing",
    "minimalist tiny white string bikini showing the slender midriff",
    "high-fashion cropped top with a tight pencil skirt",
    "white silk wrap dress cinched tightly at the waist"
]

LOCATIONS = [
    ("nana_rooftop", "standing on a high-rise balcony overlooking the Bangkok skyline"),
    ("private_lounge", "sitting elegantly in a dark, exclusive VIP lounge"),
    ("neon_walk", "walking through a corridor of bright neon light reflections"),
    ("luxury_suite", "posing in a lavish hotel suite with soft moonlight")
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

def queue_hourglass_jobs():
    print("🔥 Launching 'Hourglass Perfection' (Busty + Tiny Waist) Pack...")
    for name, location in LOCATIONS:
        print(f"Queuing {name} with hourglass figure...")
        for i in range(1, 4): # 3 variants per location
            body = random.choice(BODY_TYPE_PROMPTS)
            outfit = random.choice(OUTFITS)
            hair = random.choice(["long sleek black hair", "elegant high ponytail"])
            
            prompt = f"Cinematic high-end fashion photography of a stunning young Thai girl, {body}. She has perfectly smooth matte skin and {hair}. She is wearing {outfit}, {location}. Focus on her slender waist and voluptuous figure. Masterpiece, 8k, professional studio lighting, high contrast."
            
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_Hourglass_{name}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 999999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}: {body}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_hourglass_jobs()
    print("\n--- Hourglass (Busty + Slender Waist) series successfully queued! ---")
