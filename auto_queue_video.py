import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# Variety Pools for Videos
OUTFITS = [
    "a vibrant red velvet bodycon dress", 
    "a black sheer lace corset with silk trimmings", 
    "a modern emerald green Thai silk wrap dress", 
    "denim micro-shorts with a tied-front leopard print shirt", 
    "a sparkly gold sequin mini party dress",
    "a stylish leather jacket over a black lace top",
    "a luxury white silk dress-style bikini"
]

# The Base Video Workflow (Wan 2.1 Turbo) provided by Kevin
BASE_VIDEO_WORKFLOW = {
  "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
  "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走，裸露，NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
  "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
  "74": { "inputs": { "width": 640, "height": 640, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
  "75": { "inputs": { "unet_name": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "76": { "inputs": { "unet_name": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["81", 0] }, "class_type": "KSamplerAdvanced" },
  "80": { "inputs": { "filename_prefix": "ThaiNights_Video", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
  "81": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": 4, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable", "model": ["82", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["74", 0] }, "class_type": "KSamplerAdvanced" },
  "82": { "inputs": { "shift": 5.0, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
  "83": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
  "85": { "inputs": { "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors", "strength_model": 1.0, "model": ["76", 0] }, "class_type": "LoraLoaderModelOnly" },
  "86": { "inputs": { "shift": 5.0, "model": ["85", 0] }, "class_type": "ModelSamplingSD3" },
  "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
  "88": { "inputs": { "fps": 16, "images": ["87", 0] }, "class_type": "CreateVideo" },
  "89": { "inputs": { "text": "", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" }
}

# 18 Categories for Video with specific motion and locations
VIDEO_JOBS = [
    ("nana_plaza", "standing on a balcony at Nana Plaza Bangkok at night, she slowly turns and looks into the camera with a seductive smile, hot pink and purple neon lights flickering in the background"),
    ("soi_cowboy", "walking through the neon-drenched Soi Cowboy alleyway, rainy street with vibrant reflections, she brushes her hair back and gazes intensely at the lens"),
    ("patpong", "strolling through the busy Patpong night market, street food smoke in the air, she stops at a neon bar entrance and gives a playful wink"),
    ("thermae", "sitting in a dimly lit corner of the legendary Thermae basement, she slowly sips a drink and scans the room with a mysterious look"),
    ("soi6_pattaya", "walking down the colorful Soi 6 street in the afternoon sun, she waves at the camera while early neon signs begin to glow"),
    ("soapy_massage", "reclining gracefully on a velvet lounge inside a luxury Thai spa, soft blue steam rising around her, she moves her hand slowly over her smooth skin"),
    ("massage_guide", "standing in a traditional zen-style Thai massage room with flickering candles, she adjusts her silk uniform and smiles warmly"),
    ("grab_long_jin", "inside a mysterious, sacred Thai therapy room, she performs a slow, rhythmic ritual movement with her hands, intense focus on her face"),
    ("bj_bars", "leaning against a high stool in a neon-lit Bangkok bar, she peeks through a velvet curtain with a teasing expression"),
    ("gentlemens_clubs", "lounging on a deep red velvet sofa in a luxurious private club, she tilts her head and looks into the camera while holding a crystal glass"),
    ("thonglo_ktv", "holding a golden microphone in a high-end KTV suite, she sings softly and leans toward the camera, karaoke lights dancing on her skin"),
    ("eden_club", "at a private sensory party in Eden Club, she moves slowly under deep red dramatic lighting, a sense of forbidden fruit and mystery"),
    ("jodd_fairs", "at a Jodd Fairs outdoor bar, she laughs and talks while holding a cocktail, busy night market crowds blurred in the background"),
    ("walking_street", "dancing energetically at the iconic entrance of Pattaya Walking Street, a sea of neon lights and high energy all around her"),
    ("lk_metro", "leaning against a bar wall in LK Metro under a soft pink neon glow, she looks up and shares an intimate moment with the camera"),
    ("scam_prevention", "in a mysterious dark back alley with high contrast shadows, she looks alertly around before focusing on the camera with a serious gaze"),
    ("budget_guide", "confidently fanning herself with Thai Baht cash in a neon city setting, she smiles at her success"),
    ("pattaya_guide", "standing on a high-rise terrace with the vibrant neon Pattaya coastline stretching behind her, the night breeze moving her hair")
]

def queue_video_jobs():
    print("🎬 Starting ThaiNights 'Video Spiral' Production...")
    for name, scene in VIDEO_JOBS:
        # Choose random variety for this video
        outfit = random.choice(OUTFITS)
        hair = random.choice(["long wavy black hair", "a sleek ponytail", "a stylish short bob cut"])
        skin = random.choice(["tanned", "fair porcelain", "natural matte"])
        
        # Build the natural language video prompt
        prompt = f"Cinematic 4k video of a stunning voluptuous Thai girl with {skin} skin and {hair}, wearing {outfit}, {scene}. Perfectly smooth skin, high-fashion aesthetic, professional lighting, masterpiece, high texture detail, stable camera."
        
        print(f"Queuing Video: {name}...")
        
        # Clone and modify workflow
        workflow = BASE_VIDEO_WORKFLOW.copy()
        workflow["89"]["inputs"]["text"] = prompt
        workflow["80"]["inputs"]["filename_prefix"] = f"ThaiNights_Video_{name}"
        
        # Randomize seeds
        seed = int(time.time() * 1000) + random.randint(1, 1000)
        workflow["81"]["inputs"]["noise_seed"] = seed
        workflow["78"]["inputs"]["noise_seed"] = seed
        
        # Send to API
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Enqueued: {hair}, {outfit}")
            time.sleep(1) # Extra gap for heavy video tasks
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_video_jobs()
    print("\n--- All 18 Video Tasks have been added to the queue! ---")
    print("Warning: Video generation is heavy. Your RTX 5060 Ti will be very busy!")
