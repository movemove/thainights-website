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
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" }
}

# The 18 Categories with Explicit Prompts as requested
JOBS = [
    ("nana_plaza", "19岁泰国美女，Z-CUP超乳，精致妆容，全裸，露出粉色乳头和阴部，站在曼谷 Nana Plaza 的霓虹灯阳台上，身形火辣，极致冷白皮，毛孔清晰"),
    ("soi_cowboy", "19岁泰国美女，Z-CUP巨大胸部，全裸，露出完美的乳房和阴部，在雨后的 Soi Cowboy 霓虹灯巷弄中，身体湿润有光泽，诱惑眼神"),
    ("soapy_massage", "19岁泰国美女，Z-CUP超乳，下垂感真实，全裸，在高級泰浴浴缸中，全身佈滿白色泡沫，露出粉色乳頭，水珠滴落，極致誘惑"),
    ("thermae", "19岁泰国美女，Z-CUP超乳，全裸，坐在蛇美咖啡地下的昏暗角落，雙腿張開露出陰部，冷白皮，絲滑質感，神祕氛圍"),
    ("soi6_pattaya", "19岁泰国美女，Z-CUP超乳，全裸，在芭達雅 Soi 6 的酒吧門口，陽光照射，露出完美的乳房細節，火辣身材，極致寫實"),
    ("massage_guide", "19岁泰国美女，Z-CUP超乳，全裸，在傳統泰式按摩房，趴在床上，露出側乳和臀部，溫柔表情，冷白皮，細膩紋理"),
    ("grab_long_jin", "19岁泰国美女，Z-CUP超乳，全裸，在神祕的抓龍筋療程室，雙腿分開，露出私密處細節，專業技法，冷白皮"),
    ("bj_bars", "19岁泰国美女，Z-CUP超乳，全裸，在曼谷 BJ 酒吧的隔簾後，露出巨大的乳房，挑逗表情，霓虹光影反射"),
    ("gentlemens_clubs", "19岁泰國美女，Z-CUP超乳，全裸，躺在高級俱樂部的紅絲絨沙發上，露出完美的乳頭與陰部，奢華氛圍，琥珀色光影"),
    ("thonglo_ktv", "19岁泰国美女，Z-CUP超乳，全裸，在 Thong Lo 高級 KTV 包廂，手持金色麥克風，露出巨大的胸部，曖昧燈光"),
    ("eden_club", "19岁泰国美女，Z-CUP超乳，全裸，在 Eden Club 的私密派對，露出全身細節，包括乳頭與陰部，禁忌氛圍，極致寫實"),
    ("jodd_fairs", "19岁泰国美女，Z-CUP超乳，全裸，在 Jodd Fairs 夜市後方的露天酒吧，露出乳房，背景是熱鬧的夜市燈火，動感氛圍"),
    ("walking_street", "19岁泰国美女，Z-CUP超乳，全裸，在芭達雅 Walking Street 入口處跳舞，露出全身曲線與私密部位，狂熱氛圍，霓虹閃爍"),
    ("lk_metro", "19岁泰国美女，Z-CUP超乳，全裸，靠在 LK Metro 的酒吧牆邊，露出巨大的胸部與陰部，冷白皮，精緻五官"),
    ("scam_prevention", "19岁泰国美女，Z-CUP超乳，全裸，在暗黑的巷弄中，冷酷表情，露出完美的身體細節，高對比光影，警戒氛圍"),
    ("budget_guide", "19岁泰国美女，Z-CUP超乳，全裸，手持大量泰銖，坐在堆滿鈔票的床上，露出乳頭與陰部，財富與慾望，極致清晰"),
    ("windmill_pattaya", "19岁泰国美女，Z-CUP超乳，全裸，在 Windmill 酒吧的舞台上，極限尺度，露出全身所有私密部位，瘋狂氛圍，寫實質感"),
    ("pattaya_guide", "19岁泰国美女，Z-CUP超乳，全裸，在芭達雅海邊的露台上，背景是霓虹海岸線，露出完美的曲線與乳頭，月光照射")
]

def queue_jobs():
    print("🚀 Launching Ultimate Explicit 'Sensual Spiral' Production...")
    for name, prompt in JOBS:
        print(f"Queuing Explicit Quality: {name}...")
        workflow = json.loads(json.dumps(WORKFLOW_TEMPLATE))
        workflow["45"]["inputs"]["text"] = prompt
        workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Explicit_{name}"
        workflow["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Explicit_{name}"
        workflow["454"]["inputs"]["seed"] = random.randint(1, 999999999999999)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] Enqueued: {name}")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_jobs()
