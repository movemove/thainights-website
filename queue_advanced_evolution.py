import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Advanced Variety Pools
GIRLS = [
    "A mature and mysterious Northern Thai beauty with an elegant jawline",
    "A striking Thai-European mixed model with deep expressive eyes",
    "A playful and sweet Bangkok influencer with a youthful heart-shaped face"
]

OUTFITS = [
    "a sheer black lace corset with intricate detailing",
    "a shimmering emerald green silk wrap dress",
    "a luxury white silk dress-style bikini with gold accents",
    "a high-cut silver metallic bodysuit"
]

# Workflows (Using your stable v8 structure)
WORKFLOW_TEMPLATE = {
 "9": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
 "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
 "42": { "inputs": { "conditioning": [ "45", 0 ] }, "class_type": "ConditioningZeroOut" },
 "45": { "inputs": { "text": "", "clip": [ "446", 1 ] }, "class_type": "CLIPTextEncode" },
 "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "47": { "inputs": { "shift": 3, "model": [ "446", 0 ] }, "class_type": "ModelSamplingAuraFlow" },
 "129": { "inputs": { "samples": [ "484", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": [ "129", 0 ], "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "vae": [ "40", 0 ], "upscale_model": [ "171", 0 ] }, "class_type": "UltimateSDUpscale" },
 "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "172": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 1 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "175": { "inputs": { "value": 1.8 }, "class_type": "FloatConstant" },
 "176": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 0 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "443": { "inputs": { "width": 784, "height": 1176, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" },
 "471": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" }
}

JOBS = [
    ("adv_soapy", "reclining on a velvet lounge inside a luxury Thai spa, blue neon backlit, warm steam rising, focusing on the silk texture of her outfit and her Z-CUP silhouette"),
    ("adv_longjin", "inside a mystical, candle-lit Thai therapy room, serene expression, highly detailed skin textures, sacred and professional atmosphere"),
    ("adv_ktv", "in a dark high-end KTV suite, holding a golden microphone, amber lighting, luxurious lifestyle vibe, intense gaze directly at camera")
]

def queue_jobs():
    print("💎 Launching Advanced Visual Evolution Series...")
    for slug, scene in JOBS:
        print(f"Queuing Evolution Pack: {slug}...")
        for i in range(1, 4):
            girl = random.choice(GIRLS)
            outfit = random.choice(OUTFITS)
            # Masterpiece formula + Advanced Narrative
            prompt = f"韩风冷色调网红美白滤镜, {girl}, Z-CUP massive breasts, slender snatched waist, wearing {outfit}, {scene}. Perfectly smooth matte skin, hyper-realistic detail, high-fashion aesthetic, masterpiece, 8k resolution."
            
            wf = json.loads(json.dumps(WORKFLOW_TEMPLATE))
            wf["45"]["inputs"]["text"] = prompt
            wf["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Evolution_{slug}_{i:02d}"
            wf["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Evolution_{slug}_{i:02d}"
            wf["454"]["inputs"]["seed"] = random.randint(1, 999999999)
            
            p = {"prompt": wf}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] v{i:02d}: {outfit}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_jobs()
