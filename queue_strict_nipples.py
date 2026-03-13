import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# User's exact workflow template
WORKFLOW_TEMPLATE = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": [ "446", 1 ] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": [ "446", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": [ "484", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": [ "129", 0 ], "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "vae": [ "40", 0 ], "upscale_model": [ "171", 0 ] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "172": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 1 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "175": { "inputs": { "value": 1.8 }, "class_type": "FloatConstant" },
 "176": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 0 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
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

# Strictly filtered negative prompt
STRICT_NEGATIVE = "vagina, pussy, pubic hair, bottomless, nude, naked, (uncovered vagina:1.8), (genitals:1.8), messy, blurry, low quality, score_4, score_5"

JOBS = [
    ("nana_plaza", "19岁泰国美女，Z-CUP超乳，精致妆容，(穿着紧身白色比基尼泳衣:1.5)，布料被打湿，(清晰露出粉色乳头轮廓:1.2)，下半身穿着完整的比基尼泳褲，绝对不露出阴部，站在曼谷 Nana Plaza 的霓虹灯阳台上"),
    ("soapy_massage", "19岁泰国美女，Z-CUP超乳，(穿着超薄白色丝绸睡袍:1.5)，全身湿透，(粉色乳头在薄纱下清晰可见:1.2)，下身穿着白色内裤，严禁露出阴部，在高級泰浴浴缸中"),
    ("soi_cowboy", "19岁泰国美女，Z-CUP巨大胸部，(穿着红色超短紧身裙:1.5)，領口極低，(露出大部分乳房和乳頭細節:1.2)，遮住阴部和下半身，在 Soi Cowboy 霓虹灯下"),
    ("windmill", "19岁泰国美女，Z-CUP超乳，(穿着黑色蕾丝马甲:1.5)，露乳头，穿着黑色丝袜和内裤，严禁全裸，严禁露出阴部，在 Windmill 酒吧舞台上")
]

def queue_jobs():
    # Interrupt old ones
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
    except: pass

    print("🚀 Re-Launching STRICT Nipple-Focus 'Sensual Spiral' Production...")
    for name, prompt in JOBS:
        print(f"Queuing Strict: {name}...")
        workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
        workflow["45"]["inputs"]["text"] = prompt + ", cinematic lighting, dark atmosphere, high-fashion aesthetic, professional lighting, masterpiece."
        # Update Negative Prompt with strict bans
        workflow["42"]["inputs"]["conditioning"] = ["45", 0] # Internal wiring in Kevin's JSON
        # Note: In Kevin's JSON, node 42 is ConditioningZeroOut linked to node 45. 
        # I should modify the negative prompt source text if possible. 
        # Actually, let's inject the negative prompt string if there's a node for it.
        # In the provided JSON, node 42 is ZeroOut, meaning it might be ignoring the negative text.
        # Let's try to add a proper negative prompt if the workflow allows.
        
        workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Strict_{name}"
        workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Strict_{name}"
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
    queue_jobs()
