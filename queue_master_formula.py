import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# The "Masterpiece formula" inspired by Kevin's sample
FORMULA_PREFIX = "19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大到人类极限，胸部下垂严重，(穿着极薄的半透明白色絲綢比基尼:1.6)，(清晰看見粉色乳頭的凸起輪廓:1.4)，下半身穿着(厚實不透光的白色比基尼泳褲:1.8)，(絕對不露出陰部:1.9)，(嚴禁全裸:1.9)，"

JOBS = [
    ("master_nana", "站在曼谷 Nana Plaza 的霓虹燈陽台上"),
    ("master_soapy", "在高級泰浴大廳的魚缸前，柔和的藍色光影"),
    ("master_cowboy", "在 Soi Cowboy 霓虹燈巷弄中，背景是閃爍的招牌"),
    ("master_thermae", "坐在蛇美咖啡地下的昏暗角落，神祕氛圍"),
    ("master_soi6", "在芭達雅 Soi 6 的酒吧門口，陽光與霓虹交織"),
    ("master_walking", "在芭達雅 Walking Street 入口，高能量氣氛"),
    ("master_longjin", "在神祕的抓龍筋療程室，溫馨燭光環境"),
    ("master_bjbar", "在曼谷 BJ 酒吧的隔簾後，曖昧的光影"),
    ("master_eden", "在 Eden Club 的私密派對現場，禁忌感十足"),
    ("master_ktv", "在 Thong Lo 高級 KTV 包廂，手持金色麥克風"),
    ("master_scam", "在暗黑的曼谷巷弄中，高對比寫實風格"),
    ("master_budget", "手持大量泰銖，坐在堆滿鈔票的奢華床上")
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

def queue_master_jobs():
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://{SERVER_ADDRESS}/interrupt", data=b""))
    except: pass

    print("🚀 Launching Kevin's Masterpiece Formula Production...")
    for name, location_text in JOBS:
        print(f"Queuing Master Quality: {name}...")
        workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
        
        # Inject the Master Prompt
        full_prompt = FORMULA_PREFIX + location_text
        workflow["45"]["inputs"]["text"] = full_prompt
        
        # Setup file naming
        workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Master_{name}"
        workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Master_{name}"
        
        # Set seeds and technical params from sample
        seed = random.randint(1, 999999999999999)
        workflow["454"]["inputs"]["seed"] = seed
        
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
    queue_master_jobs()
