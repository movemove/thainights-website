import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Kevin's Zimage Master Formula + New General Guide Prompts
FORMULA_PREFIX = "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大，"

JOBS = [
    ("bangkok_metro", f"{FORMULA_PREFIX} 穿着白色紧身连体裙，优雅地站在曼谷深夜的 BTS 捷运月台上，背景是璀璨的城市灯火與霓虹，都市时尚感，极高画质"),
    ("thai_sim", f"{FORMULA_PREFIX} 穿着白色一字肩丝绸上衣，坐在曼谷的高級咖啡廳裡，手持一部現代智能手機，屏幕藍光映照在白皙臉龐上，細節精確，高級科技生活感")
]

# The Base Workflow template (Zimage v4 style - Natural Language)
BASE_WORKFLOW = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": ["446", 1] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": ["446", 0] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": ["484", 0], "vae": ["40", 0] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": ["129", 0], "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "vae": ["40", 0], "upscale_model": ["171", 0] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "443": { "inputs": { "width": 784, "height": 1176, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": ["46", 0], "clip": ["39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": ["170", 0] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": ["454", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["443", 0] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": ["488", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["485", 0] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": ["483", 0] }, "class_type": "LatentUpscaleBy" },
 "488": { "inputs": { "value": "a+b", "a": [0, 0], "b": ["454", 0] }, "class_type": "SimpleMath+" }
}

def queue_general_guides():
    print("🚀 Queuing 'General Guide' images with Zimage Master Formula...")
    for name, prompt in JOBS:
        print(f"Queuing: {name}...")
        for i in range(1, 3): # 2 versions for each
            workflow = json.loads(json.dumps(BASE_WORKFLOW))
            workflow["45"]["inputs"]["text"] = prompt
            workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_General_{name}_{i:02d}"
            workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_General_{name}_{i:02d}"
            workflow["454"]["inputs"]["seed"] = random.randint(1, 999999999999999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Enqueued version {i:02d}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_general_guides()
