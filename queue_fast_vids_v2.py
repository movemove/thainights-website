import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Real-time Speed Videos
OUTFITS = [
    "a vibrant red velvet bodycon dress", 
    "a black sheer lace bodysuit", 
    "a modern emerald green Thai silk wrap dress", 
    "denim micro-shorts with a tied-front leopard print shirt", 
    "a sparkly silver sequin party dress",
    "a stylish leather jacket over a tiny black crop top",
    "a luxury white silk dress-style bikini"
]

HAIRSTYLES = ["long wavy black hair", "a sleek ponytail", "a chic bob cut", "flowing straight hair"]
SKINS = ["exotic tanned", "fair porcelain", "natural sun-kissed matte"]

# The Base Video Workflow (Wan 2.1 Turbo) - Configured for Normal Speed (24 FPS)
BASE_VIDEO_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量, JPEG compression, blurry, slow motion, slow speed, distorted limbs, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 960, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_RealTime", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

SCENES = [
    ("nana_walk", "briskly walking across the Nana Plaza courtyard, she waves at a friend and smiles energetically, real-time natural speed"),
    ("cowboy_turn", "quickly turning around to face the camera in the middle of Soi Cowboy, laughing and adjusting her hair, vibrant street movement, normal speed"),
    ("ws_dance", "energetically dancing at the entrance of Walking Street, high speed rhythmic body movements, flashing neon lights, chaotic and lively"),
    ("ktv_sing", "passionately singing into a golden microphone, moving her body to the beat of the music, high energy performance in a luxury suite"),
    ("jodd_fairs", "hurriedly walking through Jodd Fairs night market with a cocktail in hand, looking around at the busy food stalls, realistic dynamic movement"),
    ("beach_run", "playfully running along the Pattaya shoreline at night, water splashing around her feet, high energy and natural real-time speed")
]

def queue_jobs():
    print("🎬 Launching 10 'Real-Time Dynamic' Video Jobs...")
    for i in range(1, 11):
        name, scene_desc = random.choice(SCENES)
        outfit = random.choice(OUTFITS)
        hair = random.choice(HAIRSTYLES)
        skin = random.choice(SKINS)
        
        prompt = f"High-quality 4k video at natural real-time speed. A stunning {skin} Thai girl with {hair}, wearing {outfit}, {scene_desc}. Perfectly smooth matte skin, high-fashion aesthetic, professional lighting, masterpiece, high texture detail, no slow motion."
        
        print(f"Queuing Fast v{i:02d}: {name} | {outfit}")
        
        workflow = json.loads(json.dumps(BASE_VIDEO_WORKFLOW))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_FastV2_{i:02d}"
        
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
