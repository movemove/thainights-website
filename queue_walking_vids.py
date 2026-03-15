import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Subjects and Styles
GIRL_TYPES = [
    "stunning 19yo Thai girl with exotic tanned skin and long wavy hair",
    "beautiful 20yo Bangkok model with fair porcelain skin and a sleek ponytail",
    "sexy 21yo Thai influencer with natural matte skin and a stylish bob cut",
    "gorgeous young Thai-Chinese mixed heritage girl with bright eyes"
]

OUTFITS = [
    "a vibrant red velvet bodycon dress",
    "a minimalist white string bikini",
    "a black sheer lace corset with silk trimmings",
    "a modern emerald green Thai silk wrap dress",
    "denim micro-shorts with a tied-front leopard print shirt",
    "a sparkly silver sequin party dress",
    "a cute Pikachu-themed yellow bikini set"
]

STREETS = [
    "Soi Cowboy with its sea of red neon lights",
    "Nana Plaza's bustling neon courtyard",
    "Pattaya Walking Street with massive glowing signs",
    "a rain-slicked Sukhumvit side street with vibrant reflections"
]

# The T2V Base Workflow (Wan 2.1 Turbo - from message 7575)
BASE_T2V_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 960, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_Walking", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

def queue_walking_jobs():
    print("🎬 Launching 10 'ThaiNights Walking' T2V Jobs...")
    for i in range(1, 11):
        # Determine view (alternating)
        view_type = "Front view" if i % 2 == 1 else "Side profile view"
        view_desc = "walking confidently towards the camera" if i % 2 == 1 else "walking along the sidewalk, captured from the side"
        
        # Pick random variety
        girl = random.choice(GIRL_TYPES)
        outfit = random.choice(OUTFITS)
        street = random.choice(STREETS)
        
        # Construct the Prompt
        prompt = f"Professional 4k video, {view_type}, a {girl} {view_desc}. She is wearing {outfit} and walking in {street}. Perfectly smooth matte skin, high-fashion aesthetic, natural real-time speed, cinematic lighting, masterpiece, high texture detail, stable camera movement."
        
        print(f"Queuing Job {i:02d}: {view_type} | {outfit}")
        
        # Clone and modify workflow
        workflow = json.loads(json.dumps(BASE_T2V_WORKFLOW))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_Walking_{'Front' if i%2==1 else 'Side'}_{i:02d}"
        
        # Seeds
        seed = random.randint(1, 10**14)
        workflow["81"]["inputs"]["noise_seed"] = seed
        workflow["78"]["inputs"]["noise_seed"] = seed
        
        # Send to API
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_walking_jobs()
    print("\n--- 10 Walking Street Video tasks successfully added to the queue! ---")
