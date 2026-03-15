import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Ultimate Variety Pools
FACE_TYPES = [
    "Northern Thai beauty with very fair skin and an elegant oval face",
    "Exotic Isan Thai girl with striking tanned skin and deep-set seductive eyes",
    "Mixed heritage Thai-European (Luk khrueng) with sharp features and a high nose bridge",
    "Thai-Chinese influencer style with bright, sparkling eyes and a youthful heart-shaped face",
    "Southern Thai girl with beautiful bronze skin and long voluminous dark curls"
]

SKIN_TONES = [
    "fair porcelain matte skin",
    "exotic deeply tanned skin",
    "sun-kissed honey bronze skin",
    "smooth olive complexion"
]

OUTFITS = [
    "a high-cut leopard print bodysuit",
    "a neon pink latex mini dress with side cut-outs",
    "a modern gold-threaded Thai silk wrap dress",
    "a silver metallic mini skirt paired with a tiny black crop top",
    "a deep red velvet corset top with denim micro-shorts",
    "a shimmering electric blue sequin cocktail dress",
    "a black mesh bodysuit worn over a white micro bikini",
    "a stylish leather jacket draped over a red lace lingerie set"
]

VIEWS = [
    "Frontal view, walking confidently directly towards the camera",
    "Side profile view, walking along the neon-lit sidewalk",
    "3/4 angle view, looking over her shoulder as she walks",
    "Low angle tracking shot from the front, showcasing her confident stride"
]

STREETS = [
    "the heart of Soi Cowboy, drenched in red neon reflections",
    "Nana Plaza's bustling courtyard under flickering pink lights",
    "Pattaya Walking Street surrounded by massive vibrant signage",
    "a rainy Sukhumvit side street with colorful lights reflecting on wet asphalt"
]

# Base Workflow (Wan 2.1 Turbo)
BASE_WF = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 960, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_UltVar", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
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
    print("🚀 Queuing 10 'Ultimate Variety Walking' T2V Jobs...")
    for i in range(1, 11):
        face = random.choice(FACE_TYPES)
        skin = random.choice(SKIN_TONES)
        outfit = random.choice(OUTFITS)
        view = random.choice(VIEWS)
        street = random.choice(STREETS)
        
        prompt = f"Professional 4k video, {view}. The subject is a {face} with {skin}. She is wearing {outfit}, walking through {street}. Perfectly smooth skin, natural real-time speed, cinematic high-fashion aesthetic, high texture detail, stable camera movement, masterpiece."
        
        print(f"Queuing Ultimate v{i:02d}: {outfit} | {skin}")
        
        workflow = json.loads(json.dumps(BASE_WF))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_UltWalking_{i:02d}"
        
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
