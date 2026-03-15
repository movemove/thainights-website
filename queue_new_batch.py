import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# EXACT JSON TEMPLATE from Kevin's Moody v2 workflow
WORKFLOW_TEMPLATE = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": [ "446", 1 ] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": [ "446", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": [ "484", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": [ "175", 0 ], "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": [ "129", 0 ], "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "vae": [ "40", 0 ], "upscale_model": [ "171", 0 ] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "172": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 1 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "175": { "inputs": { "value": 1.8 }, "class_type": "FloatConstant" },
 "176": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 0 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "PowerLoraLoaderHeaderWidget": { "type": "PowerLoraLoaderHeaderWidget" }, "➕ Add Lora": "", "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "455": { "inputs": { "images": [ "452", 0 ] }, "class_type": "PreviewImage" },
 "481": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "482": { "inputs": { "upscale_model": [ "481", 0 ], "image": [ "170", 0 ] }, "class_type": "ImageUpscaleWithModel" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" },
 "471": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" }
}

FORMULA_PREFIX = "韩风冷色调网红美白滤镜, 19岁泰国美女，韓式網紅風格，极致冷白皮，overexposure，有着Z-CUP超乳，胸部巨大，细腰，沙漏型身材，"

JOBS = [
    ("ride_hailing", f"{FORMULA_PREFIX} 穿着紧身豹纹裙，迈着修长的双腿正准备进入一辆 Grab 豪华轿车，深夜曼谷街头，背景霓虹闪烁，動態感十足"),
    ("hotel_guide", f"{FORMULA_PREFIX} 穿着白色丝绸睡裙，慵懒地躺在曼谷高級酒店的特大床上，背景是落地窗外的曼谷城市夜景，高級質感"),
    ("ladyboy_bar", f"{FORMULA_PREFIX} 穿着閃亮的銀色金屬感比基尼，站在 Nana Plaza 二樓的舞台邊緣，燈光迷幻，誘惑眼神，極致寫實")
]

def queue_batch():
    for name, prompt in JOBS:
        print(f"Queuing: {name}...")
        workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
        workflow["45"]["inputs"]["text"] = prompt
        workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_New_{name}"
        workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_New_{name}"
        workflow["454"]["inputs"]["seed"] = random.randint(1, 999999999)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Enqueued {name}")
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_batch()
