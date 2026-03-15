import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Foot Massage
NAIL_COLORS = ["glossy crimson red", "shimmering hot pink", "classic pearl white", "midnight black"]
SKIN_TONES = ["exotic tanned", "fair porcelain", "natural sun-kissed matte"]

# The Base Video Workflow (Wan 2.1 Turbo) - Set to 24 FPS for normal speed
BASE_VIDEO_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "blurry, slow motion, slow speed, distorted toes, messy, low quality, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 832, "height": 1216, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_FootMassage_Fast", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

MASSAGE_SCENES = [
    "Extreme close-up, natural real-time speed. Warm hands are vigorously massaging the smooth soles of a stunning {skin} Thai girl. Her toes have {nail} nail polish, exactly five perfect toes. The movement is energetic and realistic, showing the rhythmic pressure on the foot. Cinematic 4k.",
    "Brisk movement, normal speed. Close-up of a Thai beauty's bare feet being massaged with oil. Fingers sliding quickly and firmly across the high arches. {nail} nail polish, smooth matte skin. High texture detail, masterpiece.",
    "Real-time action shot. A skilled masseuse is using her thumbs to apply deep pressure on the pressure points of a {skin} girl's foot. The toes move naturally in response. {nail} nail polish, exactly five toes. Professional lighting, 4k."
]

def queue_foot_jobs():
    print("🎬 Launching 6 'Foot Massage' Real-Time Video Jobs...")
    for i in range(1, 7):
        scene_template = random.choice(MASSAGE_SCENES)
        nail = random.choice(NAIL_COLORS)
        skin = random.choice(SKIN_TONES)
        
        prompt = scene_template.format(nail=nail, skin=skin)
        print(f"Queuing Foot Massage v{i:02d}: {nail} | {skin}")
        
        workflow = json.loads(json.dumps(BASE_VIDEO_WORKFLOW))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_FootMsg_Fast_{i:02d}"
        
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
    queue_foot_jobs()
    print("\n--- 6 specialized 'Normal Speed' Foot Massage tasks added to queue! ---")
