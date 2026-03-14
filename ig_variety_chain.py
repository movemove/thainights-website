import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 1. TEXT TO IMAGE WORKFLOW (Qwen 2512 - from message 7891)
WF_IMAGE = {
 "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
 "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
 "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
 "107": { "inputs": { "width": 816, "height": 1456, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
 "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
 "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
 "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
 "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
 "123": { "inputs": { "filename_prefix": "IG/THAINIGHTS_Variety", "images": ["109", 0] }, "class_type": "SaveImage" },
 "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

# 2. IMAGE TO VIDEO WORKFLOW (Wan 2.2 - from message 7907/7912)
# Using the exact structure from message 7912
WF_VIDEO = {
 "97": { "inputs": { "image": "" }, "class_type": "LoadImage" },
 "108": { "inputs": { "filename_prefix": "video/IG_Variety", "format": "auto", "codec": "auto", "video-preview": "", "video": ["129:94", 0] }, "class_type": "SaveVideo" },
 "129:98": { "inputs": { "width": 640, "height": 1152, "length": 169, "batch_size": 1, "positive": ["129:93", 0], "negative": ["129:89", 0], "vae": ["129:90", 0], "start_image": ["97", 0] }, "class_type": "WanImageToVideo" },
 "129:94": { "inputs": { "fps": 16, "images": ["129:87", 0] }, "class_type": "CreateVideo" },
 "129:104": { "inputs": { "shift": 5.000000000000001, "model": ["129:116", 0] }, "class_type": "ModelSamplingSD3" },
 "129:102": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "strength_model": 1.0000000000000002, "model": ["129:96", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:124": { "inputs": { "value": 2 }, "class_type": "PrimitiveInt" },
 "129:85": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": ["129:125", 0], "end_at_step": ["129:119", 0], "return_with_leftover_noise": "disable", "model": ["129:103", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:86", 0] }, "class_type": "KSamplerAdvanced" },
 "129:118": { "inputs": { "value": 4 }, "class_type": "PrimitiveInt" },
 "129:86": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": ["129:125", 0], "return_with_leftover_noise": "enable", "model": ["129:104", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:98", 2] }, "class_type": "KSamplerAdvanced" },
 "129:89": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:128": { "inputs": { "value": 20 }, "class_type": "PrimitiveInt" },
 "129:87": { "inputs": { "samples": ["129:85", 0], "vae": ["129:90", 0] }, "class_type": "VAEDecode" },
 "129:93": { "inputs": { "text": "A cinematic slow camera pan from left to right across the scene. The stunning Thai woman slowly turns her head to follow the camera, her seductive gaze meeting the lens. Her long dark hair flows naturally with a subtle breeze, flickering neon lights in background. High texture detail, masterpiece.", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:131": { "inputs": { "value": True }, "class_type": "PrimitiveBoolean" },
 "129:90": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
 "129:84": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
 "129:96": { "inputs": { "unet_name": "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:95": { "inputs": { "unet_name": "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:103": { "inputs": { "shift": 5.000000000000001, "model": ["129:117", 0] }, "class_type": "ModelSamplingSD3" },
 "129:127": { "inputs": { "value": 10 }, "class_type": "PrimitiveInt" },
 "129:101": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0000000000000002, "model": ["129:95", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:126": { "inputs": { "value": 3.5 }, "class_type": "PrimitiveFloat" },
 "129:116": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:95", 0], "on_true": ["129:101", 0] }, "class_type": "ComfySwitchNode" },
 "129:117": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:96", 0], "on_true": ["129:102", 0] }, "class_type": "ComfySwitchNode" },
 "129:119": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:128", 0], "on_true": ["129:118", 0] }, "class_type": "ComfySwitchNode" },
 "129:120": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:126", 0], "on_true": ["129:122", 0] }, "class_type": "ComfySwitchNode" },
 "129:125": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:127", 0], "on_true": ["129:124", 0] }, "class_type": "ComfySwitchNode" },
 "129:122": { "inputs": { "value": 1.0 }, "class_type": "PrimitiveFloat" }
}

# Variety Pools
GIRL_TYPES = [
    "20岁泰国美女，混血质感，精致深邃五官",
    "19岁曼谷女孩，清新甜美风格，鹅蛋脸",
    "22岁泰籍模特，健康小麦色皮肤，野性魅力"
]
OUTFITS = ["穿着白色紧身连体裙", "穿着紧身红色包臀裙", "穿着豹纹紧身连裙"]

def queue_prompt(workflow):
    p = {"prompt": workflow}
    # Fix for boolean and float in JSON
    data = json.dumps(p).replace('True', 'true').replace('False', 'false').encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def run_variety_chain():
    print("🚀 Starting Variety Chain: Photo -> Video...")
    
    for i in range(1, 4):
        print(f"--- Round {i} ---")
        girl = random.choice(GIRL_TYPES)
        outfit = random.choice(OUTFITS)
        
        # Step 1: Image
        print("📸 Generating Image...")
        prompt = f"韩风冷色调网红美白滤镜，{girl}，有着Z-CUP超乳，细腰，{outfit}，正面走在深夜曼谷的街道上。背景霓虹闪烁，景深，大师级摄影。"
        WF_IMAGE["108"]["inputs"]["text"] = prompt
        WF_IMAGE["106"]["inputs"]["seed"] = random.randint(1, 10**14)
        
        res = queue_prompt(WF_IMAGE)
        img_id = res['prompt_id']
        
        filename = None
        while not filename:
            h = get_history(img_id)
            if img_id in h:
                out = h[img_id].get('outputs', {})
                for n in out:
                    if 'images' in out[n]:
                        img = out[n]['images'][0]
                        filename = f"{img.get('subfolder', '')}/{img['filename']}" if img.get('subfolder') else img['filename']
                        print(f"  ✅ Image ready: {filename}")
                        break
            if not filename: time.sleep(5)
            
        # Step 2: Video
        print("🎬 Generating Video...")
        WF_VIDEO["97"]["inputs"]["image"] = filename
        v_seed = random.randint(1, 10**14)
        WF_VIDEO["129:86"]["inputs"]["noise_seed"] = v_seed
        WF_VIDEO["129:85"]["inputs"]["noise_seed"] = v_seed
        
        res_v = queue_prompt(WF_VIDEO)
        print(f"  ✅ Video Queued: {res_v['prompt_id']}")
        time.sleep(2)

if __name__ == "__main__":
    run_variety_chain()
