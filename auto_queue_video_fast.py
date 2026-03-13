import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Real-time Speed Videos
OUTFITS = [
    "a vibrant red velvet bodycon dress", 
    "a black sheer lace corset", 
    "a modern gold Thai silk wrap dress", 
    "denim micro-shorts with a leopard print shirt", 
    "a sparkly gold sequin party dress",
    "a stylish leather jacket over a black lace top",
    "a luxury white silk bikini"
]

# The Base Video Workflow (Wan 2.1 Turbo) - Updated for Normal Speed
BASE_VIDEO_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走，裸露，NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 640, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "ThaiNights_NormalSpeed", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" }, # Increased to 24 for smoother, normal speed
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

# New Prompts focused on Normal Speed and High Energy
NORMAL_SPEED_JOBS = [
    ("nana_plaza_fast", "walking energetically on the balcony of Nana Plaza, she waves at the camera and laughs, hot pink neon lights flashing, busy crowds below, real-time speed, dynamic movement"),
    ("soi_cowboy_bustle", "bustling through the crowded Soi Cowboy alley, she quickly brushes her hair back and smiles confidently at the lens, vibrant red neon reflections, energetic street life, realistic speed"),
    ("walking_street_dance", "dancing with high energy at a Go-Go bar entrance in Pattaya Walking Street, fast movements, rhythmic body sway, sea of flickering neon lights, high excitement, real-time capture"),
    ("soapy_massage_splash", "actively playing with thick white soap bubbles in a luxury Thai bathhouse, she laughs and splashes water, smooth skin glistening, soft blue ambient light, natural real-time speed"),
    ("ktv_karaoke_sing", "energetically singing into a golden microphone in a luxury KTV suite, she moves to the beat of the music, karaoke lights dancing on her skin, intimate but high-energy vibe"),
    ("soi6_action", "quickly walking down Soi 6 Pattaya, she high-fives a friend and turns to blow a kiss to the camera, tropical afternoon sun, vibrant and lively street movement")
]

def queue_normal_speed_videos():
    print("🎬 Starting ThaiNights 'Real-time Speed' Video Production...")
    for name, scene in NORMAL_SPEED_JOBS:
        # Variety for these videos
        outfit = random.choice(OUTFITS)
        hair = random.choice(["long wavy black hair", "a sleek ponytail", "a chic bob"])
        
        # Prompt: Removed "slow motion", added "real-time speed", "energetically", etc.
        prompt = f"Professional 4k video of a stunning voluptuous Thai girl with large breasts and a slender waist, {hair}, wearing {outfit}, {scene}. Perfectly smooth matte skin, high-fashion aesthetic, natural real-time speed, masterpiece, high texture detail, stable camera."
        
        print(f"Queuing Normal Speed Video: {name}...")
        
        workflow = BASE_VIDEO_WORKFLOW.copy()
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"ThaiNights_Fast_{name}"
        workflow["88"]["inputs"]["fps"] = 24
        
        seed = int(time.time() * 1000) + random.randint(1, 9999)
        workflow["81"]["inputs"]["noise_seed"] = seed
        workflow["78"]["inputs"]["noise_seed"] = seed
        
        # Send to API
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Enqueued Normal Speed: {outfit}")
            time.sleep(1)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_normal_speed_videos()
    print("\n--- 6 High-Energy Normal Speed Video Tasks have been added! ---")
