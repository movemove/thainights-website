import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🌈 Special Themed Outfit Pool
THEMED_OUTFITS = [
    "vibrant hot pink silk bikini with lace edges",
    "bright sunflower yellow string bikini",
    "cute Pikachu-themed yellow bikini with red cheek spots and lightning bolt patterns",
    "sexy Pikachu cosplay outfit with yellow ears and black-tipped tail details",
    "neon pink latex dress with cut-outs",
    "bright yellow traditional Thai silk wrap-around dress",
    "pink leather mini skirt with a matching crop top",
    "playful yellow mesh beach cover-up over a black bikini"
]

HAIRSTYLES = ["elegant ponytail", "long flowing black hair", "stylish bob with pink highlights"]
SKIN_TONES = ["exotic tanned", "fair porcelain", "natural matte"]

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

LOCATIONS = [
    ("nana_plaza", "at the neon-lit Nana Plaza"),
    ("soi_cowboy", "in the middle of Soi Cowboy alley"),
    ("pattaya_beach", "walking along Pattaya beach at sunset"),
    ("bangkok_bar", "sitting in a modern Bangkok rooftop bar")
]

def queue_themed_jobs():
    print("🎨 Launching Pink, Yellow, and Pikachu Themed Variety Pack...")
    for name, location in LOCATIONS:
        print(f"Queuing {name} with themed colors...")
        for i in range(1, 4): # 3 variants per location
            outfit = random.choice(THEMED_OUTFITS)
            hair = random.choice(HAIRSTYLES)
            skin = random.choice(SKIN_TONES)
            
            prompt = f"Cinematic night photography of 1woman, a stunning Thai girl with {skin} skin, {hair}, wearing {outfit}, {location}. Vibrant colors, smooth matte skin, high-resolution textures, high-fashion aesthetic, neon light reflections, masterpiece."
            
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_Themed_{name}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 99999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}: {outfit}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_themed_jobs()
    print("\n--- Themed Color Pack (Pink, Yellow, Pikachu) successfully queued! ---")
