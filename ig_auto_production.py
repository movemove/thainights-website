import json
import urllib.request
import time
import os
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Workflow 1: Image Generation (from message 7891)
WF_IMAGE = {
 "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
 "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
 "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
 "107": { "inputs": { "width": 816, "height": 1456, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
 "108": { "inputs": { "text": "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大，白色横条三角比基尼泳衣，走在深夜曼谷的Soi cowboy 街道上，霓虹燈光影，景深", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
 "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
 "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
 "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
 "123": { "inputs": { "filename_prefix": "IG/THAINIGHTS", "images": ["109", 0] }, "class_type": "SaveImage" },
 "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

# Workflow 2: Video Generation (from message 7907)
WF_VIDEO = {
 "97": { "inputs": { "image": "" }, "class_type": "LoadImage" },
 "108": { "inputs": { "filename_prefix": "video/IG_Wan2.2", "format": "auto", "codec": "auto", "video-preview": "", "video": ["129:94", 0] }, "class_type": "SaveVideo" },
 "129:98": { "inputs": { "width": 640, "height": 1152, "length": 169, "batch_size": 1, "positive": ["129:93", 0], "negative": ["129:89", 0], "vae": ["129:90", 0], "start_image": ["97", 0] }, "class_type": "WanImageToVideo" },
 "129:94": { "inputs": { "fps": 16, "images": ["129:87", 0] }, "class_type": "CreateVideo" },
 "129:104": { "inputs": { "shift": 5.0, "model": ["129:116", 0] }, "class_type": "ModelSamplingSD3" },
 "129:102": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "strength_model": 1.0, "model": ["129:96", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:124": { "inputs": { "value": 2 }, "class_type": "PrimitiveInt" },
 "129:85": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": ["129:125", 0], "end_at_step": ["129:119", 0], "return_with_leftover_noise": "disable", "model": ["129:103", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:86", 0] }, "class_type": "KSamplerAdvanced" },
 "129:118": { "inputs": { "value": 4 }, "class_type": "PrimitiveInt" },
 "129:86": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": ["129:125", 0], "return_with_leftover_noise": "enable", "model": ["129:104", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:98", 2] }, "class_type": "KSamplerAdvanced" },
 "129:89": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:128": { "inputs": { "value": 20 }, "class_type": "PrimitiveInt" },
 "129:87": { "inputs": { "samples": ["129:85", 0], "vae": ["129:90", 0] }, "class_type": "VAEDecode" },
 "129:93": { "inputs": { "text": "A cinematic medium shot of the beautiful woman from the image. She slowly and sensually pushes herself up from the white bed using her arms, lifting her upper body towards the camera. As she rises, her full face with full double D-cup breasts are revealed with her pink nipples clearly visible. As she rises more, shows her white g-string. She maintains a seductive smile and keeps direct eye contact with the lens throughout the movement. The motion is smooth and realistic, showcasing the natural weight and sway of her body. Warm ambient lighting, soft shadows, 4k resolution, high texture detail on her smooth skin and the bedsheets.", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:131": { "inputs": { "value": True }, "class_type": "PrimitiveBoolean" },
 "129:90": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
 "129:84": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
 "129:96": { "inputs": { "unet_name": "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:95": { "inputs": { "unet_name": "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:103": { "inputs": { "shift": 5.0, "model": ["129:117", 0] }, "class_type": "ModelSamplingSD3" },
 "129:127": { "inputs": { "value": 10 }, "class_type": "PrimitiveInt" },
 "129:101": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "strength_model": 1.0, "model": ["129:95", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:126": { "inputs": { "value": 3.5 }, "class_type": "PrimitiveFloat" },
 "129:116": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:95", 0], "on_true": ["129:101", 0] }, "class_type": "ComfySwitchNode" },
 "129:117": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:96", 0], "on_true": ["129:102", 0] }, "class_type": "ComfySwitchNode" },
 "129:119": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:128", 0], "on_true": ["129:118", 0] }, "class_type": "ComfySwitchNode" },
 "129:120": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:126", 0], "on_true": ["129:122", 0] }, "class_type": "ComfySwitchNode" },
 "129:125": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:127", 0], "on_true": ["129:124", 0] }, "class_type": "ComfySwitchNode" },
 "129:122": { "inputs": { "value": 1.0 }, "class_type": "PrimitiveFloat" }
}

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def run_ig_automation():
    print("🚀 Step 1: Generating High-Res Photo...")
    # Randomize seed for image
    WF_IMAGE["106"]["inputs"]["seed"] = random.randint(1, 10**14)
    resp = queue_prompt(WF_IMAGE)
    prompt_id = resp['prompt_id']
    print(f"  - Image Queued (ID: {prompt_id}). Waiting...")

    image_filename = None
    while not image_filename:
        history = get_history(prompt_id)
        if prompt_id in history:
            outputs = history[prompt_id].get('outputs', {})
            for node_id in outputs:
                if 'images' in outputs[node_id]:
                    img = outputs[node_id]['images'][0]
                    # We need the format "subfolder/filename" if subfolder exists
                    fn = img['filename']
                    sub = img.get('subfolder', '')
                    image_filename = f"{sub}/{fn}" if sub else fn
                    print(f"  ✅ Photo saved as: {image_filename}")
                    break
        if not image_filename:
            time.sleep(5)

    print("🚀 Step 2: Feeding Photo into Video Workflow...")
    # Update video workflow with the newly generated image filename
    WF_VIDEO["97"]["inputs"]["image"] = image_filename
    
    # Randomize video seeds
    v_seed = random.randint(1, 10**14)
    WF_VIDEO["129:86"]["inputs"]["noise_seed"] = v_seed
    WF_VIDEO["129:85"]["inputs"]["noise_seed"] = v_seed
    
    resp_v = queue_prompt(WF_VIDEO)
    print(f"  - Video Queued (ID: {resp_v['prompt_id']})")
    print(f"  - Process running. Check C:\\Users\\movem\\Documents\\ComfyUI\\output for results.")

if __name__ == "__main__":
    run_ig_automation()
