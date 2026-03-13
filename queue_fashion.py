import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Expanded Variety Pools
OUTFITS = [
    "vibrant red velvet bodycon dress", 
    "black sheer lace corset with silk trimmings", 
    "modern emerald green Thai silk wrap-around dress", 
    "denim micro-shorts with a tied-front leopard print shirt", 
    "sparkly gold sequin mini party dress",
    "electric blue latex high-fashion bodysuit",
    "pink satin nightgown with black lace borders",
    "stylish leather biker jacket over a tiny black bikini"
]

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

JOBS = [
    ("nana_plaza", "on a balcony at Nana Plaza Bangkok"),
    ("soi_cowboy", "in the middle of Soi Cowboy alleyway"),
    ("patpong", "walking through Patpong night market"),
    ("thermae", "in a moody corner of the Thermae basement"),
    ("soi6_pattaya", "on the street of Pattaya Soi 6"),
    ("soapy_massage", "gracefully reclining inside a luxury Thai spa"),
    ("gentlemens_clubs", "lounging in a luxurious Bangkok private club"),
    ("thonglo_ktv", "holding a microphone in a Thong Lo KTV"),
    ("walking_street", "dancing at the entrance of Pattaya Walking Street")
]

def queue_fashion_explosion():
    print("Launching Fashion Explosion Variety Pack...")
    for name, location in JOBS:
        print(f"Queuing {name} with diverse fashion...")
        for i in range(1, 3): # 2 unique styles per category
            outfit = random.choice(OUTFITS)
            hair = random.choice(["sleek black ponytail", "long wavy hair", "short stylish bob"])
            skin = random.choice(["exotic tanned", "fair porcelain", "natural matte"])
            
            prompt = f"Cinematic nightlife photography of 1woman, a stunning young Thai girl with {skin} skin, {hair}, wearing {outfit}, {location}. Perfectly smooth skin, no moisture, high-fashion aesthetic, neon light reflections, masterpiece, 8k resolution."
            
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_Fashion_{name}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Style {i:02d}: {outfit}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_fashion_explosion()
    print("\n--- Fashion Explosion successfully added! Variety is the spice of the spiral. ---")
