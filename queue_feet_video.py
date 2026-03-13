import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Bare Feet Videos
NAIL_COLORS = ["vibrant hot pink", "glossy deep red", "clean pearl white", "chic black", "soft pastel blue"]
SKIN_TONES = ["exotic tanned", "fair porcelain", "natural matte"]

# The Base Video Workflow (Wan 2.1 Turbo)
BASE_VIDEO_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走，裸露，NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 640, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "ThaiNights_FeetVideo", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

FEET_SCENES = [
    ("massage_sole", "Extreme close-up of beautiful bare feet during a Thai massage. A gorgeous girl with {skin} skin is having her soles massaged. Her toes have {nail} nail polish, exactly five perfect toes on each foot. Soft candle lighting, gentle finger movements, cinematic 4k."),
    ("soapy_toes", "Focus on a stunning Thai girl's bare feet in a luxury bathhouse. Her feet are covered in thick white soap bubbles. She moves her {nail} painted toes playfully under warm water. High texture detail, exactly five toes, smooth skin, realistic speed."),
    ("relaxing_feet", "Medium shot of a Thai beauty sitting on a high velvet stool, dangling her bare feet. Her {skin} feet feature {nail} nail polish. The camera focuses on the graceful arch and the five distinct toes moving naturally. Nightclub background, cinematic bokeh."),
    ("beach_barefoot", "Close-up of bare feet walking on fine sand at Pattaya beach at night. {nail} nail polish on the toes. The moonlight reflects on the smooth skin and five perfect toes. Natural real-time movement, high quality textures.")
]

def queue_feet_videos():
    print("🎬 Starting ThaiNights 'Bare Feet' Video Production...")
    for name, scene_template in FEET_SCENES:
        for i in range(1, 3): # 2 variants per scene
            nail = random.choice(NAIL_COLORS)
            skin = random.choice(SKIN_TONES)
            prompt = scene_template.format(nail=nail, skin=skin)
            
            print(f"Queuing Feet Video: {name} v{i}...")
            
            workflow = BASE_VIDEO_WORKFLOW.copy()
            workflow["89"]["inputs"]["text"] = prompt
            workflow["80"]["inputs"]["filename_prefix"] = f"ThaiNights_Feet_Video_{name}_{i:02d}"
            
            seed = int(time.time() * 1000) + random.randint(1, 99999)
            workflow["81"]["inputs"]["noise_seed"] = seed
            workflow["78"]["inputs"]["noise_seed"] = seed
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] {nail} polish, {skin} skin.")
                time.sleep(1)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_feet_videos()
    print("\n--- 8 specialized Bare Feet Video Tasks have been added! ---")
