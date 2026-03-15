import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Variety Pools for the Beckoning Series
GIRL_TYPES = [
    "19yo Thai beauty with exotic tanned skin and long wavy hair",
    "stunning 20yo Bangkok model with fair porcelain skin and a high ponytail",
    "sexy 21yo Thai influencer with honey bronze skin and a stylish bob",
    "beautiful Thai-Chinese mixed girl with sharp features and bright eyes"
]

BIKINI_STYLES = [
    "a tiny white string bikini",
    "a vibrant red micro bikini",
    "a black sheer lace bikini set",
    "a sparkly silver sequin bikini",
    "a bright yellow Pikachu-themed bikini"
]

HEELS_STYLES = [
    "sky-high white stiletto heels",
    "elegant silver strappy high heels",
    "glossy black platform high heels"
]

# T2V Base Workflow (Wan 2.1 Turbo - 10 Second Config)
# Length: 241 frames / 24 FPS = 10.04 seconds
BASE_T2V_10S = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "blurry, slow motion, static, low quality, messy, JPEG, distorted limbs, extra fingers, bad anatomy, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 832, "height": 1216, "length": 241, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_Beckon_Final", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
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
    print("🎬 Launching 10-Second 'Soi Cowboy Beckoning' Ultra Variety Pack...")
    for i in range(1, 11):
        girl = random.choice(GIRL_TYPES)
        bikini = random.choice(BIKINI_STYLES)
        heels = random.choice(HEELS_STYLES)
        view = "Frontal view" if i % 2 == 1 else "Side profile view"
        
        prompt = f"Professional 4k video, {view}, natural real-time speed. A {girl} is standing at the entrance of a neon-lit bar in Soi Cowboy, wearing {bikini} and {heels}. She is energetically waving and beckoning customers to come inside with a seductive smile and a playful wink. She turns slightly to show her figure. Red neon reflections on the ground, bustling nightlife energy, perfectly smooth matte skin, high texture detail, stable camera, masterpiece, no slow motion."
        
        print(f"Queuing Job {i:02d}: {bikini} | {heels}")
        
        workflow = json.loads(json.dumps(BASE_T2V_10S))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_Beckon10s_{i:02d}"
        
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
    print("\n--- 10-second Real-Time Beckon tasks are now in the queue! ---")
