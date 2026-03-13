import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Pools for variety
OUTFITS = [
    "tiny white string bikini", 
    "luxury white silk dress-style bikini", 
    "intricate white lace lingerie set", 
    "crisp white micro bikini with gold accents",
    "elegant white sheer cocktail outfit"
]

HAIRSTYLES = [
    "long wavy black hair", 
    "sleek black ponytail", 
    "stylish short black bob cut", 
    "long straight hair falling over shoulders"
]

SKIN_TONES = [
    "exotic tanned skin", 
    "fair porcelain skin", 
    "natural sun-kissed skin"
]

EXPRESSIONS = [
    "seductive smile", 
    "mysterious cool expression", 
    "soft alluring gaze", 
    "playful wink"
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
    ("nana_plaza", "on a balcony overlooking Nana Plaza in Bangkok at night with hot pink neon"),
    ("soi_cowboy", "standing in the middle of Soi Cowboy with vibrant red neon signs and reflections"),
    ("patpong", "walking through Patpong night market with glowing Go-Go bar entrances and stalls"),
    ("thermae", "in a dimly lit, moody corner of the legendary Thermae basement bar"),
    ("soi6_pattaya", "on the street of Pattaya Soi 6 during a sun-drenched afternoon with early neon lights"),
    ("soapy_massage", "gracefully reclining inside a luxury Thai soapy massage hall with soft blue steam"),
    ("massage_guide", "in a traditional zen-style Thai massage room with warm candle lighting"),
    ("grab_long_jin", "inside a mysterious, sacred Thai therapy room for ancient prostate massage"),
    ("bj_bars", "partially hidden behind a neon-lit curtain in a Bangkok BJ bar"),
    ("gentlemens_clubs", "lounging on a deep red velvet sofa in a luxurious Bangkok private club"),
    ("thonglo_ktv", "holding a golden microphone in a high-end Thong Lo KTV private suite"),
    ("eden_club", "at a private sensory party in Eden Club Bangkok with deep red dramatic lighting"),
    ("jodd_fairs", "at a Jodd Fairs night market outdoor bar with busy crowds and lights"),
    ("walking_street", "dancing energetically at the entrance of Pattaya Walking Street"),
    ("lk_metro", "leaning against a bar wall in LK Metro Pattaya under soft neon glow"),
    ("scam_prevention", "in a mysterious dark back alley with high contrast cinematic shadows"),
    ("budget_guide", "confidently holding a fan of Thai Baht cash in a neon city setting"),
    ("pattaya_guide", "standing on a terrace with the vibrant neon Pattaya bay in the background")
]

def clear_and_queue():
    # 1. Interrupt current job (optional but clean)
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
        print("Interrupted existing jobs to start the fresh variety pack.")
    except: pass

    # 2. Queue new jobs with randomization
    for name, location in JOBS:
        print(f"Queuing {name} with variety...")
        for i in range(1, 4):
            # Randomize attributes
            outfit = random.choice(OUTFITS)
            hair = random.choice(HAIRSTYLES)
            skin = random.choice(SKIN_TONES)
            expression = random.choice(EXPRESSIONS)
            
            prompt = f"Cinematic night photography of 1woman, a stunning young Thai girl with {skin}, {hair}, {expression}, wearing {outfit}, {location}. Perfectly smooth matte skin, high-resolution textures, high-fashion aesthetic, professional lighting, masterpiece."
            
            # Prepare workflow
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_{name}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 1000)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}: {hair}, {skin}, {outfit}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    clear_and_queue()
    print("\n--- 'Sensual Spiral' Variety Pack successfully queued! ---")
