import json
import urllib.request
import urllib.parse
import time
import os
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 1. Image Generator (SeedVR2 v1.0.6)
WF_IMAGE = {
 "9": { "inputs": { "filename_prefix": "IG/ThaiNights_4K", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": [ "446", 1 ] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": [ "446", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": [ "484", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": [ "129", 0 ], "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "vae": [ "40", 0 ], "upscale_model": [ "171", 0 ] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "462": { "inputs": { "shift": 3, "model": [ "469", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "463": { "inputs": { "model_name": "sam_vit_b_01ec64.pth", "device_mode": "AUTO" }, "class_type": "SAMLoader" },
 "466": { "inputs": { "model_name": "bbox/face_yolov8m.pt" }, "class_type": "UltralyticsDetectorProvider" },
 "467": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "469": { "inputs": { "PowerLoraLoaderHeaderWidget": { "type": "PowerLoraLoaderHeaderWidget" }, "lora_1": { "on": True, "lora": "face-detailer.safetensors", "strength": 1 }, "➕ Add Lora": "", "model": [ "46", 0 ], "clip": [ "39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
 "470": { "inputs": { "guide_size": 1024, "guide_size_for": True, "max_size": 768, "seed": [ "467", 0 ], "steps": 4, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "denoise": 0.39, "feather": 100, "noise_mask": True, "force_inpaint": True, "bbox_threshold": 0.3, "bbox_dilation": 128, "bbox_crop_factor": 2, "sam_detection_hint": "center-1", "sam_dilation": 32, "sam_threshold": 0.2, "sam_bbox_expansion": 976, "sam_mask_hint_threshold": 0.7, "sam_mask_hint_use_negative": "False", "drop_size": 10, "wildcard": "", "cycle": 1, "inpaint_model": False, "noise_mask_feather": 20, "tiled_encode": False, "tiled_decode": False, "image": [ "170", 0 ], "model": [ "462", 0 ], "clip": [ "469", 1 ], "vae": [ "40", 0 ], "positive": [ "474", 0 ], "negative": [ "465", 0 ], "bbox_detector": [ "466", 0 ], "sam_model_opt": [ "463", 0 ] }, "class_type": "FaceDetailer" },
 "471": { "inputs": { "filename_prefix": "IG/ThaiNights_4K", "images": [ "470", 0 ] }, "class_type": "SaveImage" },
 "474": { "inputs": { "text": "19 years old cute Thai girl, beautiful face", "clip": [ "469", 1 ] }, "class_type": "CLIPTextEncode" },
 "477": { "inputs": { "model": "ema_vae_fp16.safetensors", "device": "cuda:0", "encode_tiled": True, "encode_tile_size": 1024, "encode_tile_overlap": 128, "decode_tiled": True, "decode_tile_size": 1024, "decode_tile_overlap": 128, "tile_debug": "false", "offload_device": "cpu", "cache_model": False }, "class_type": "SeedVR2LoadVAEModel" },
 "478": { "inputs": { "model": "seedvr2_ema_7b_sharp_fp16.safetensors", "device": "cuda:0", "blocks_to_swap": 36, "swap_io_components": False, "offload_device": "cpu", "cache_model": False, "attention_mode": "sageattn_3" }, "class_type": "SeedVR2LoadDiTModel" },
 "479": { "inputs": { "seed": 0, "resolution": 4096, "max_resolution": 4096, "batch_size": 1, "uniform_batch_size": False, "color_correction": "lab", "temporal_overlap": 0, "prepend_frames": 0, "input_noise_scale": 0, "latent_noise_scale": 0, "offload_device": "cpu", "enable_debug": False, "image": [ "470", 0 ], "dit": [ "478", 0 ], "vae": [ "477", 0 ] }, "class_type": "SeedVR2VideoUpscaler" },
 "480": { "inputs": { "filename_prefix": "IG/THAINIGHTS_ULTIMATE", "images": [ "479", 0 ] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" }
}

# 2. Image To Video Workflow (Wan 2.2 v2.0 - FIXED)
WF_VIDEO = {
 "97": { "inputs": { "image": "" }, "class_type": "LoadImage" },
 "108": { "inputs": { "filename_prefix": "video/IG_Wan2.2_v5", "format": "auto", "codec": "auto", "video-preview": "", "video": ["129:94", 0] }, "class_type": "SaveVideo" },
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
 "129:93": { "inputs": { "text": "A cinematic high-quality video of the woman in the image. She slowly and sensually moves in the nightclub. Perfectly smooth skin, realistic motion, 4k.", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:131": { "inputs": { "value": True }, "class_type": "PrimitiveBoolean" },
 "129:90": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
 "129:84": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
 "129:96": { "inputs": { "unet_name": "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:95": { "inputs": { "unet_name": "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:103": { "inputs": { "shift": 5.0, "model": ["129:117", 0] }, "class_type": "ModelSamplingSD3" },
 "129:127": { "inputs": { "value": 10 }, "class_type": "PrimitiveInt" },
 "129:101": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "strength_model": 1.0, "model": ["129:95", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:126": { "inputs": { "value": 3.5 }, "class_type": "PrimitiveFloat" },
 "129:116": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:95", 0], "on_true": ["129:101", 0] }, "class_type": "ComfySwitchNode" },
 "129:117": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:96", 0], "on_true": ["129:102", 0] }, "class_type": "ComfySwitchNode" },
 "129:119": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:128", 0], "on_true": ["129:118", 0] }, "class_type": "ComfySwitchNode" },
 "129:120": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:126", 0], "on_true": ["129:122", 0] }, "class_type": "ComfySwitchNode" },
 "129:125": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:127", 0], "on_true": ["129:124", 0] }, "class_type": "ComfySwitchNode" },
 "129:122": { "inputs": { "value": 1.0 }, "class_type": "PrimitiveFloat" }
}

def send_prompt(workflow):
    p = {"prompt": workflow}
    data = json.dumps(p).replace('True', 'true').replace('False', 'false').encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def upload_image(filename):
    # This is a trick: We download from /view and upload to /upload/image
    print(f"🔄 Moving {filename} from output to input folder via API...")
    view_url = f"http://{SERVER_ADDRESS}/view?filename={urllib.parse.quote(filename)}&type=output"
    upload_url = f"http://{SERVER_ADDRESS}/upload/image"
    
    try:
        with urllib.request.urlopen(view_url) as response:
            img_data = response.read()
            
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        data = []
        data.append(f'--{boundary}'.encode())
        data.append(f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(filename)}"'.encode())
        data.append('Content-Type: image/png'.encode())
        data.append(b'')
        data.append(img_data)
        data.append(f'--{boundary}--'.encode())
        payload = b'\r\n'.join(data)
        
        req = urllib.request.Request(upload_url, data=payload)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            return res['name']
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return os.path.basename(filename)

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def run_production():
    print("🚀 Step 1: Generating High-Res Image...")
    # Your formula prompt
    prompt = "韩风冷色调网红美白滤镜, 19岁泰国美少女，细腻毛孔与真实绒毛清晰可见，韩式网红妆容。 站在曼谷 Soi Cowboy 的霓虹灯下，白色横条三角比基尼泳衣，胸部巨大Z-CUP，细腰，眼神诱惑，背景霓虹闪烁，景深效果，电影感摄影"
    WF_IMAGE["45"]["inputs"]["text"] = prompt
    WF_IMAGE["454"]["inputs"]["seed"] = random.randint(1, 10**14)
    WF_IMAGE["467"]["inputs"]["seed"] = random.randint(1, 10**14)
    
    resp = send_prompt(WF_IMAGE)
    img_id = resp['prompt_id']
    print(f"  - Image Queued: {img_id}. Polling...")

    final_input_fn = None
    while not final_input_fn:
        h = get_history(img_id)
        if img_id in h:
            outputs = h[img_id].get('outputs', {})
            if "480" in outputs: # Final high-res node
                out_fn = outputs["480"]['images'][0]['filename']
                sub = outputs["480"]['images'][0].get('subfolder', '')
                full_out_path = f"{sub}/{out_fn}" if sub else out_fn
                final_input_fn = upload_image(full_out_path)
                break
        time.sleep(10)

    print(f"🚀 Step 2: Generating Video using {final_input_fn}...")
    WF_VIDEO["97"]["inputs"]["image"] = final_input_fn
    v_seed = random.randint(1, 10**14)
    WF_VIDEO["129:86"]["inputs"]["noise_seed"] = v_seed
    WF_VIDEO["129:85"]["inputs"]["noise_seed"] = v_seed
    
    resp_v = send_prompt(WF_VIDEO)
    print(f"  ✅ Video Job Queued: {resp_v['prompt_id']}")

if __name__ == "__main__":
    run_production()
