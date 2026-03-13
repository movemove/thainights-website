import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# User's exact Zimage workflow template
WORKFLOW_TEMPLATE = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": ["446", 1] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": ["446", 0] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": ["484", 0], "vae": ["40", 0] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": ["129", 0], "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "vae": ["40", 0], "upscale_model": ["171", 0] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "PowerLoraLoaderHeaderWidget": { "type": "PowerLoraLoaderHeaderWidget" }, "➕ Add Lora": "", "model": ["46", 0], "clip": ["39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": ["170", 0] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": ["454", 0], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["443", 0] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": ["488", 0], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["485", 0] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": ["483", 0] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": ["487", 0], "b": ["454", 0] }, "class_type": "SimpleMath+" }
}

# Zimage Specialized Prompts (Explicit Nipples but Covered Bottom)
JOBS = [
    ("zimage_nana", "19岁泰国美女，Z-CUP巨大胸部，(穿着白色透视比基尼泳衣:1.6)，(清晰露出粉色乳头点位:1.3)，下半身穿着(厚实的白色比基尼泳裤:1.6)，绝对不露出阴部，(严禁全裸:1.8)，站在曼谷 Nana Plaza 的霓虹灯陽台上"),
    ("zimage_soapy", "19岁泰国美女，Z-CUP超乳，(穿着湿透的白色丝绸睡裙:1.6)，(粉色乳头在湿透的布料下清晰可见:1.3)，下半身穿着(不透光的白色内裤:1.6)，严禁露出下身私密处，在高級泰浴浴缸中"),
    ("zimage_cowboy", "19岁泰国美女，Z-CUP巨大胸部，(穿着极短红色紧身裙:1.6)，领口极低，(胸部巨大到露出乳头細節:1.3)，下半身有裙子遮擋，嚴禁全裸，站在 Soi Cowboy 的霓虹燈下")
]

def queue_zimage_jobs():
    # Interrupt any remaining tasks
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
    except: pass

    print("🚀 Launching ZIMAGE Optimized 'Nipple Focus' Production...")
    for name, prompt in JOBS:
        print(f"Queuing Zimage Task: {name}...")
        workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
        workflow["45"]["inputs"]["text"] = prompt + ", perfectly smooth cold white skin, no moisture, hyper-realistic detail, high-fashion, masterpiece."
        workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Zimage_{name}"
        workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Zimage_{name}"
        workflow["454"]["inputs"]["seed"] = random.randint(1, 999999999999999)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Enqueued")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_zimage_jobs()
