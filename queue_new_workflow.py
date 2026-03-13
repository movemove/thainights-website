import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Variety Pools optimized for the new "Moody Mix" Workflow
# Incorporating your specific request for "Large Breasts + Tiny Waist"
BODY_TRAITS = "stunning Thai beauty, (Z-CUP massive breasts:1.2), extremely slender snatched waist, (hourglass body shape:1.3), perfectly smooth matte cold white skin, hyper-realistic pores and skin texture"
OUTFITS = ["white string micro bikini", "red velvet bodycon dress", "black lace corset", "white silk wrap dress", "sparkly gold sequin mini dress"]

LOCATIONS = [
    ("nana_plaza", "standing on a balcony at Nana Plaza Bangkok under intense pink neon lights"),
    ("soi_cowboy", "in the middle of Soi Cowboy with vibrant red neon reflections and deep shadows"),
    ("soapy_massage", "reclining gracefully inside a luxury Thai soapy massage hall with soft blue ambient glow"),
    ("gentlemens_club", "lounging on a deep red velvet sofa in a luxurious private Bangkok VIP club"),
    ("thonglo_ktv", "holding a golden microphone in a high-end Thong Lo KTV suite, karaoke lights dancing on her skin"),
    ("soi6_pattaya", "walking through the hormonal atmosphere of Pattaya Soi 6 in the late afternoon sun")
]

# The NEW Advanced Workflow JSON structure
NEW_WORKFLOW = {
  "39": { "inputs": { "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default" }, "class_type": "CLIPLoader" },
  "40": { "inputs": { "vae_name": "ae.safetensors" }, "class_type": "VAELoader" },
  "42": { "inputs": { "conditioning": ["45", 0] }, "class_type": "ConditioningZeroOut" },
  "45": { "inputs": { "text": "", "clip": ["446", 1] }, "class_type": "CLIPTextEncode" },
  "46": { "inputs": { "unet_name": "moodyPornMix_zitV10DPO.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "47": { "inputs": { "shift": 3, "model": ["446", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "129": { "inputs": { "samples": ["484", 0], "vae": ["40", 0] }, "class_type": "VAEDecode" },
  "170": { "inputs": { "upscale_by": 1.8, "seed": 0, "steps": 3, "cfg": 1, "sampler_name": "er_sde", "scheduler": "sgm_uniform", "denoise": 0.27, "mode_type": "Linear", "tile_width": 1024, "tile_height": 1024, "mask_blur": 64, "tile_padding": 128, "seam_fix_mode": "None", "seam_fix_denoise": 1, "seam_fix_width": 64, "seam_fix_mask_blur": 8, "seam_fix_padding": 16, "force_uniform_tiles": True, "tiled_decode": False, "batch_size": 1, "image": ["129", 0], "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "vae": ["40", 0], "upscale_model": ["171", 0] }, "class_type": "UltimateSDUpscale" },
  "171": { "inputs": { "model_name": "4x-UltraSharp.pth" }, "class_type": "UpscaleModelLoader" },
  "443": { "inputs": { "width": 640, "height": 960, "batch_size": 1 }, "class_type": "EmptyLatentImage" },
  "446": { "inputs": { "model": ["46", 0], "clip": ["39", 0] }, "class_type": "Power Lora Loader (rgthree)" },
  "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
  "471": { "inputs": { "filename_prefix": "", "images": ["170", 0] }, "class_type": "SaveImage" },
  "483": { "inputs": { "add_noise": "enable", "noise_seed": ["454", 0], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["443", 0] }, "class_type": "KSamplerAdvanced" },
  "484": { "inputs": { "add_noise": "disable", "noise_seed": ["488", 0], "steps": 9, "cfg": 1, "sampler_name": "dpmpp_2m_sde", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["485", 0] }, "class_type": "KSamplerAdvanced" },
  "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": ["483", 0] }, "class_type": "LatentUpscaleBy" },
  "488": { "inputs": { "value": "a+b", "a": [0, 0], "b": ["454", 0] }, "class_type": "SimpleMath+" }
}

def queue_new_jobs():
    print("🚀 Launching High-End 'Moody Mix' Production for ThaiNights...")
    for name, location in LOCATIONS:
        print(f"Queuing Ultimate Quality: {name}...")
        for i in range(1, 3):
            outfit = random.choice(OUTFITS)
            # Combine the logic of the new workflow with the ThaiNights scene
            prompt = f"{BODY_TRAITS}, wearing {outfit}, {location}. Detailed eyes, cinematic lighting, dark atmosphere, depth of field, high contrast photography, masterpiece."
            
            # Prepare payload
            workflow = NEW_WORKFLOW.copy()
            workflow["45"]["inputs"]["text"] = prompt
            workflow["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Moody_{name}_{i:02d}"
            
            # Random seed
            seed = random.randint(1, 999999999999999)
            workflow["454"]["inputs"]["seed"] = seed
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}: {outfit}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_new_jobs()
