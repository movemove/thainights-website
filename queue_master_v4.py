import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# The Master Formula (Natural Language Version - No Decimals)
BASE_PREFIX = "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大到人类极限，胸部下垂严重，"

# Natural Language Style Reinforcement
STYLES = [
    "she is actively using both hands to pull down her white bikini top, boldly revealing her pink nipples to the viewer, while her lower body remains strictly and fully covered by opaque white bikini bottoms, ensuring no other private parts are visible, high-fashion provocative pose", # Style A: Pull down
    "she is wearing a tight white bikini top that completely and fully covers her nipples, the fabric is thick and totally non-transparent with no see-through effect, her massive breasts create intense tension on the fabric, her lower body is fully dressed in white bikini bottoms, high-end look" # Style B: Covered
]

LOCATIONS = [
    ("nana", "站在曼谷 Nana Plaza 的霓虹燈陽台上"),
    ("soapy", "在高級泰浴大廳的魚缸前，水霧繚繞"),
    ("cowboy", "在 Soi Cowboy 霓虹燈巷弄中"),
    ("thermae", "坐在蛇美咖啡地下的昏暗角落"),
    ("ktv", "在 Thong Lo 高級 KTV 包廂")
]

# The Base Workflow template
WORKFLOW_TEMPLATE = {
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
 "172": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 1 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "175": { "inputs": { "value": 1.8 }, "class_type": "FloatConstant" },
 "176": { "inputs": { "value": "(a*b + (128 * 2))/2", "a": [ "450", 0 ], "b": [ "175", 0 ] }, "class_type": "SimpleMath+" },
 "443": { "inputs": { "width": 784, "height": 1176, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": ["46", 0], "clip": ["39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "455": { "inputs": { "images": [ "452", 0 ] }, "class_type": "PreviewImage" },
 "468": { "inputs": { "rgthree_comparer": { "images": [] }, "image_a": [ "170", 0 ], "image_b": [ "170", 0 ] }, "class_type": "Image Comparer (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": ["170", 0] }, "class_type": "SaveImage" },
 "481": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
 "482": { "inputs": { "upscale_model": [ "481", 0 ], "image": [ "170", 0 ] }, "class_type": "ImageUpscaleWithModel" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": ["454", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["443", 0] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": ["488", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["485", 0] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": ["483", 0] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": ["487", 0], "b": ["454", 0] }, "class_type": "SimpleMath+" }
}

def queue_v4_jobs():
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
    except: pass

    print("🚀 Launching Master v4: The 'Natural Narrative' Series...")
    for name, loc in LOCATIONS:
        print(f"Queuing v4 Natural: {name}...")
        for i, style_text in enumerate(STYLES, 1):
            workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
            tag = "PullDown" if i == 1 else "Covered"
            
            # Pure Natural Language Construction
            full_prompt = f"{BASE_PREFIX} {style_text}, {loc}. (photorealistic:1.2), cinematic lighting, masterpiece."
            workflow["45"]["inputs"]["text"] = full_prompt
            
            workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_v4_{tag}_{name}"
            workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_v4_{tag}_{name}"
            workflow["454"]["inputs"]["seed"] = random.randint(1, 999999999999999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Style {tag} enqueued.")
                time.sleep(0.5)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_v4_jobs()
