import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 1. Image Generator (First Workflow)
IMAGE_WF = {
 "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
 "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
 "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
 "107": { "inputs": { "width": 816, "height": 1456, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
 "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
 "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
 "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
 "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
 "123": { "inputs": { "filename_prefix": "IG/THAINIGHTS", "images": ["109", 0] }, "class_type": "SaveImage" },
 "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

# 2. Video Generator (Second Workflow)
VIDEO_WF = {
 "71": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
 "72": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走，裸露，NSFW", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
 "73": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
 "74": { "inputs": { "width": 832, "height": 1248, "length": 81, "batch_size": 1 }, "class_type": "EmptyHunyuanLatentVideo" },
 "75": { "inputs": { "unet_name": "wan2.1_i2v_720p_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "78": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": 20, "cfg": 1, "sampler_name": "uni_pc", "scheduler": "simple", "start_at_step": 0, "end_at_step": 20, "return_with_leftover_noise": "disable", "model": ["86", 0], "positive": ["89", 0], "negative": ["72", 0], "latent_image": ["91", 0] }, "class_type": "KSamplerAdvanced" },
 "80": { "inputs": { "filename_prefix": "IG_video", "format": "auto", "codec": "auto", "video-preview": "", "video": ["88", 0] }, "class_type": "SaveVideo" },
 "82": { "inputs": { "shift": 12, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
 "83": { "inputs": { "lora_name": "wan2.1_i2v_720p_lightx2v_1.1.safetensors", "strength_model": 1, "model": ["75", 0] }, "class_type": "LoraLoaderModelOnly" },
 "86": { "inputs": { "shift": 12, "model": ["83", 0] }, "class_type": "ModelSamplingSD3" },
 "87": { "inputs": { "samples": ["78", 0], "vae": ["73", 0] }, "class_type": "VAEDecode" },
 "88": { "inputs": { "fps": 16, "images": ["87", 0] }, "class_type": "CreateVideo" },
 "89": { "inputs": { "text": "A cinematic slow camera pan from left to right across the scene. The stunning Thai woman slowly turns her head to follow the camera, her seductive gaze meeting the lens. Her long dark hair flows naturally with a subtle breeze, flickering neon lights in background. High texture detail, masterpiece.", "clip": ["71", 0] }, "class_type": "CLIPTextEncode" },
 "90": { "inputs": { "image": "", "upload": "image" }, "class_type": "LoadImage" },
 "91": { "inputs": { "vae": ["73", 0], "image": ["90", 0] }, "class_type": "WanVideoI2VConditioning" }
}

def send_prompt(workflow):
    p = {"prompt": workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def run_production():
    print("🚀 Triggering Step 1: Image...")
    prompt = "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔清晰可见，有着Z-CUP超乳，胸部巨大，白色横条三角比基尼泳衣，走在深夜曼谷的Soi cowboy 街道上，霓虹燈光影，景深"
    IMAGE_WF["108"]["inputs"]["text"] = prompt
    IMAGE_WF["106"]["inputs"]["seed"] = random.randint(1, 999999999)
    
    resp = send_prompt(IMAGE_WF)
    prompt_id = resp['prompt_id']
    print(f"  - Image Job Queued: {prompt_id}")
    
    # In a fully automated loop, we'd poll history to get the filename
    # For now, I've queued the image. Once you have the filename, I can run Step 2.
    # Or I can set up the Video queue to assume the next image if we use a fixed name.

if __name__ == "__main__":
    run_production()
