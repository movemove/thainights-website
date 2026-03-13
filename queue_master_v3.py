import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# The "Kevin's Success Formula" updated for direct exposure variety
BASE_PREFIX = "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大到人类极限，胸部下垂严重，"

# Two distinct styles: Pulled down vs Covered
STYLES = [
    "(正在用雙手拉下白色比基尼上衣:1.6)，(大膽露出粉紅乳頭:1.4)，下半身穿著(厚實白色泳褲:1.8)，(絕對不露出陰部:1.9)，(嚴禁全裸:1.9)", # Style A: Pull down
    "(穿著緊身白色比基尼上衣:1.6)，(完全遮住乳頭:1.5)，(布料不透光:1.7)，(NO see-through:1.8)，下半身穿著(白色泳褲:1.8)，(絕對不露出陰部:1.9)" # Style B: Covered
]

JOBS = [
    ("nana", "站在曼谷 Nana Plaza 的霓虹燈陽台上"),
    ("soapy", "在高級泰浴大廳的魚缸前，水霧繚繞"),
    ("cowboy", "在 Soi Cowboy 霓虹燈巷弄中"),
    ("thermae", "坐在蛇美咖啡地下的昏暗角落"),
    ("soi6", "在芭達雅 Soi 6 的酒吧門口"),
    ("walking", "在芭達雅 Walking Street 入口"),
    ("ktv", "在 Thong Lo 高級 KTV 包廂")
]

# The Base Workflow template (matching your best result params)
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
 "443": { "inputs": { "width": 784, "height": 1176, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
 "446": { "inputs": { "model": ["46", 0], "clip": ["39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": ["170", 0] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": ["454", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["443", 0] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": ["488", 0], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["485", 0] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": ["483", 0] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": ["487", 0], "b": ["454", 0] }, "class_type": "SimpleMath+" }
}

def queue_v3_jobs():
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
    except: pass

    print("🚀 Launching Master v3: The 'Direct Spiral' Series...")
    for name, location_text in JOBS:
        print(f"Queuing v3 variety: {name}...")
        for i, style_prompt in enumerate(STYLES, 1):
            workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
            
            # Inject the Formula + Randomized Style + Location
            full_prompt = BASE_PREFIX + style_prompt + "，" + location_text
            workflow["45"]["inputs"]["text"] = full_prompt
            
            # Setup file naming
            tag = "PullDown" if i == 1 else "Covered"
            workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_v3_{tag}_{name}"
            workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_v3_{tag}_{name}"
            
            # Seed randomization
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
    queue_v3_jobs()
