import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Specialized "Slender Feet" Variety Pools
NAIL_COLORS = [
    "glossy cherry red", 
    "metallic shimmering silver", 
    "vibrant electric blue", 
    "soft lavender purple", 
    "elegant matte black",
    "shining gold leaf",
    "fresh mint green"
]

FOOT_TRAITS = [
    "extremely slender and delicate feet with long elegant toes",
    "graceful slim feet with high defined arches",
    "dainty and narrow feet, soft skin texture, perfectly manicured",
    "long slender toes with beautiful natural curves"
]

# Base Video Workflow (Wan 2.1 Turbo - 10 Second / 480x864 Optimized)
BASE_T2V_WF = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "blurry, slow motion, static, low quality, messy, distorted toes, extra toes, deformed feet, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 480, "height": 864, "length": 241, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_SlenderFeet", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

def queue_slender_feet_jobs():
    print("🎬 Launching 10-Second 'Slender Feet & Colorful Nails' Series...")
    for i in range(1, 11):
        color = random.choice(NAIL_COLORS)
        trait = random.choice(FOOT_TRAITS)
        skin = random.choice(["fair porcelain", "exotic tanned", "natural matte"])
        
        prompt = f"Professional 4k video, extreme close-up, natural real-time speed. Focus on {trait} of a stunning Thai girl with {skin} skin. Her toes are painted with {color} nail polish, exactly five perfect toes. Warm oil is being massaged into her soles by skilled hands, showing deep rhythmic pressure and skin elasticity. High texture detail, masterpiece, no slow motion, vibrant colors, cinematic lighting."
        
        print(f"Queuing Job {i:02d}: {color} nails | {skin}")
        
        workflow = json.loads(json.dumps(BASE_T2V_WF))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_SlenderFeet_{i:02d}"
        
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
    queue_slender_feet_jobs()
    print("\n--- 10-second Slender Feet queue is now being populated! ---")
