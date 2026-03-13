import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Expanded Variety Pools (Added Body Types)
BODY_TYPES = [
    "voluptuous figure with large breasts",
    "busty with an hourglass body shape",
    "curvy and seductive physique",
    "slender yet with a large chest",
    "athletic and busty"
]

NATIONALITIES = [
    "Northern Thai beauty with fair skin",
    "Exotic Isan Thai girl with striking tanned skin",
    "Bangkok socialite style",
    "Mixed heritage Thai-European",
    "Thai-Chinese heritage girl"
]

OUTFITS = [
    "vibrant red velvet bodycon dress", 
    "black sheer lace corset", 
    "modern gold Thai silk wrap dress", 
    "denim micro-shorts with a tied-front shirt", 
    "sparkly silver sequin party dress",
    "crisp white micro bikini",
    "emerald green satin cocktail dress"
]

# The Base Workflow
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

LOCATIONS = [
    ("nana_plaza", "on a balcony at Nana Plaza"),
    ("soapy_massage", "lounging inside a luxury Thai spa"),
    ("gentlemens_club", "inside a dark VIP lounge area"),
    ("pattaya_soi6", "standing at a colorful bar in Pattaya")
]

def queue_curvy_variety():
    print("🔥 Launching Curvy & Voluptuous Variety Pack...")
    for name, location in LOCATIONS:
        print(f"Queuing {name} with curvy figure...")
        for i in range(1, 3):
            identity = random.choice(NATIONALITIES)
            body = random.choice(BODY_TYPES)
            outfit = random.choice(OUTFITS)
            
            prompt = f"Cinematic night photography of 1woman, {identity}, {body}, wearing {outfit}, {location}. Perfectly smooth matte skin, high-resolution textures, seductive gaze, hyper-realistic, masterpiece, 8k."
            
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_Curvy_{name}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 9999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}: {body}, {outfit}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_curvy_variety()
    print("\n--- The spiral just got curvier. Check your ComfyUI queue! ---")
