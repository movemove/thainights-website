import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# User's exact workflow template with fixed syntax
WORKFLOW_TEMPLATE = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": [ "446", 1 ] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": [ "446", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "64": { "inputs": { "rgthree_comparer": { "images": [] }, "image_a": [ "129", 0 ], "image_b": [ "482", 0 ] }, "class_type": "Image Comparer (rgthree)" },
 "129": { "inputs": { "samples": [ "484", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": [ "175", 0 ], "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": [ "176", 0 ], "tile_height": [ "172", 0 ], "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": [ "129", 0 ], "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "vae": [ "40", 0 ], "upscale_model": [ "171", 0 ] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "172": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 1 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "175": { "inputs": { "value": 1.8 }, "class_type": "FloatConstant" },
 "176": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 0 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "200": { "inputs": { "images": [ "129", 0 ] }, "class_type": "PreviewImage" },
 "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "PowerLoraLoaderHeaderWidget": { "type": "PowerLoraLoaderHeaderWidget" }, "➕ Add Lora": "", "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "455": { "inputs": { "images": [ "452", 0 ] }, "class_type": "PreviewImage" },
 "468": { "inputs": { "rgthree_comparer": { "images": [] }, "image_a": [ "170", 0 ], "image_b": [ "170", 0 ] }, "class_type": "Image Comparer (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "481": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "482": { "inputs": { "upscale_model": [ "481", 0 ], "image": [ "170", 0 ] }, "class_type": "ImageUpscaleWithModel" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" }
}

JOBS = [
    ("nana_plaza", "19岁泰国美女，韩式网红风格，精致妝容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大，白色横条三角比基尼泳衣，在曼谷 Nana Plaza 的霓虹灯陽台上"),
    ("soapy_massage", "19岁泰国美女，韩式網红风格，极致冷白皮，有着Z-CUP超乳，胸部巨大，白色丝绸睡裙，在曼谷高級泰浴大廳的魚缸前，柔和的藍色光影，高級質感")
]

def queue_jobs():
    for name, prompt in JOBS:
        print(f"Queuing with New Workflow: {name}...")
        for i in range(1, 2): # Just 1 for testing high-quality
            workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE)) # Deep copy
            workflow["45"]["inputs"]["text"] = prompt
            workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_MoodyV2_{name}_{i:02d}"
            workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_MoodyV2_{name}_{i:02d}"
            workflow["454"]["inputs"]["seed"] = random.randint(1, 9999999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Enqueued: {name}")
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_jobs()
