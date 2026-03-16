import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Auto-Generated Content
GIRL_TYPES = [
    "mature Northern Thai beauty, sharp jawline, mysterious seductive eyes",
    "elegant mixed-heritage Thai-European model, deep-set expressive eyes",
    "youthful Bangkok socialite, heart-shaped face, dimples, sweet smile"
]

OUTFITS = [
    "shimmering emerald green silk wrap dress",
    "sheer black lace corset with silk trimmings",
    "high-cut silver metallic bodysuit",
    "vibrant red velvet bodycon dress"
]

# T2V Base Workflow (Wan 2.1 Turbo - 10 Second / 480x864 Optimized)
BASE_WF = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "blurry, slow motion, static, low quality, messy, distorted toes, deformed limbs, extra fingers, bad anatomy, NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 480, "height": 864, "length": 241, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "video/ThaiNights_Auto", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 24, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

# 10 High-Impact, Sensory-Focused Auto-Decided Jobs
AUTO_JOBS = [
    ("nana_balcony", "standing on a luxury balcony overlooking the neon-soaked Nana Plaza, she slowly tucks hair behind her ear and gives an alluring gaze, pink neon rim lighting"),
    ("cowboy_rain", "walking elegantly through the rain-slicked Soi Cowboy alley, vibrant red reflections on the wet asphalt, she brushes a water droplet from her face, filmic mood"),
    ("spa_steam", "gracefully reclining inside a steamy luxury Thai bathhouse, soft blue ambient light, her hand slowly sliding over her smooth skin, mysterious atmosphere"),
    ("longjin_ritual", "inside a mystical candle-lit Thai therapy room, serene expression, her hands performing a slow graceful movement, focus on detailed skin and ritual vibe"),
    ("ktv_mood", "leaning back in a dark high-end KTV booth, holding a golden microphone, amber lighting, a subtle smile as she looks towards the viewer, luxurious lifestyle"),
    ("soi6_afternoon", "walking confidently down Soi 6 Pattaya in the golden afternoon sun, waving energetically with a playful wink, vibrant street energy"),
    ("ws_entrance", "standing at the massive glowing entrance of Pattaya Walking Street, sea of neon lights, she turns around confidently to face the camera, high energy"),
    ("rooftop_cocktail", "at a sleek Bangkok rooftop bar, city skyline in background, she slowly sips a crystal glass cocktail and gazes out at the neons, sophisticated"),
    ("eden_sensual", "at a private sensory party, deep red dramatic shadows, she moves slowly and provocatively, capturing the essence of forbidden fruit and mystery"),
    ("beach_moonlight", "walking on the white sands of Pattaya at night, moonlit sea behind her, she looks up at the sky and shares a quiet moment with the camera")
]

def queue_auto_decided():
    print("🎬 Launching 10 Alice-Decided 'Sensual Spiral' Video Jobs...")
    for i, (tag, scene) in enumerate(AUTO_JOBS, 1):
        girl = random.choice(GIRL_TYPES)
        outfit = random.choice(OUTFITS)
        
        prompt = f"Professional 4k video, natural real-time speed. A {girl} wearing {outfit}, {scene}. Perfectly smooth matte skin, high-fashion aesthetic, high texture detail, stable camera movement, masterpiece, no slow motion."
        
        print(f"Queuing Job {i:02d} ({tag}): {outfit} | {girl[:20]}...")
        
        workflow = json.loads(json.dumps(BASE_WF))
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"video/ThaiNights_AliceChoice_{tag}_{i:02d}"
        
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
    queue_auto_decided()
    print("\n--- 10 'Alice's Choice' Video tasks successfully added to the queue! ---")
