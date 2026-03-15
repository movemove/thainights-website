import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Varieties for the Side-View Expedition
FACE_TYPES = [
    "Northern Thai beauty with very fair skin and an elegant heart-shaped face",
    "Exotic Isan Thai girl with striking tanned skin and deep-set seductive eyes",
    "Mixed heritage Thai-European (Luk khrueng) with sharp, model-like features",
    "Thai-Chinese influencer style with a youthful face and sparkling bright eyes",
    "Southern Thai girl with radiant bronze skin and voluminous dark hair"
]

SKIN_TONES = ["fair porcelain matte", "exotic tanned", "sun-kissed honey bronze", "smooth olive"]

OUTFITS = [
    "a vibrant red silk cheongsam-style bikini",
    "a black sheer lace bodysuit with a leather mini skirt",
    "a modern emerald green Thai silk wrap dress",
    "a silver metallic string bikini with high heels",
    "a deep purple velvet corset and denim hot pants",
    "a shimmering gold sequin cocktail dress",
    "a stylish white off-shoulder crop top and a tight micro skirt",
    "a leopard print silk slip dress"
]

# Specific Camera Pan/Track Movements for Side View
CAMERA_ACTIONS = [
    "A slow horizontal camera pan following her movement from the side",
    "A cinematic lateral tracking shot, keeping pace with her graceful stride",
    "A smooth side-view shot with the camera slowly dollying alongside her",
    "A dynamic side-view tracking shot focusing on her silhouette and movement"
]

STREETS = [
    "the heart of Soi Cowboy with red neon reflections on rainy asphalt",
    "Nana Plaza's bustling courtyard under flickering pink and purple lights",
    "Pattaya Walking Street surrounded by massive glowing signage",
    "a dark Sukhumvit side street with vibrant neon light bokeh"
]

# Base Workflow (Wan 2.1 Turbo)
BASE_WF = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 832, "height": 1216, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_SideWalk", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

def queue_jobs():
    print("🚀 Launching 10 'Side-View Cinematic' T2V Jobs...")
    for i in range(1, 11):
        face = random.choice(FACE_TYPES)
        skin = random.choice(SKIN_TONES)
        outfit = random.choice(OUTFITS)
        action = random.choice(CAMERA_ACTIONS)
        street = random.choice(STREETS)
        
        prompt = f"Professional 4k video, side profile view. {action}. A {face} with {skin} skin is walking gracefully across {street}. She is wearing {outfit}. Perfectly smooth skin, natural real-time speed, cinematic high-fashion aesthetic, high texture detail, stable camera movement, masterpiece."
        
        print(f"Queuing Side-View v{i:02d}: {outfit} | {skin}")
        
        workflow = json.loads(json.dumps(BASE_WF))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_SideWalk_{i:02d}"
        
        seed = random.randint(1, 10**14)
        workflow["81"]["inputs"]["noise_seed"] = seed
        workflow["78"]["inputs"]["noise_seed"] = seed
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_jobs()
