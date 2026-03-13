import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# 🧬 Final Completion Pool (Diverse faces, outfits, non-wet)
MISSING_JOBS = [
    ("bangkok-bj-bars", "A cinematic close-up shot of a gorgeous Thai girl with fair skin and a stylish bob cut. She is wearing a delicate white lace choker and a matching outfit, standing behind a neon-lit bar curtain in Bangkok. Soft, moody lighting, intense eye contact, perfectly smooth matte skin texture, masterpiece."),
    ("eden-bangkok", "A sophisticated night portrait of a stunning Thai woman with long straight black hair and an elegant oval face. She is wearing a modern white silk dress and standing in a dimly lit, high-end private lounge in Bangkok. Atmospheric deep red lighting, mysterious vibe, soft shadows, 4k detail."),
    ("gentlemens-clubs", "A luxury fashion-style shot of a beautiful Thai model with tanned skin and an elegant high ponytail. She is lounging on a premium leather sofa in an exclusive Bangkok gentlemen's club. Amber lighting, crystal glasses on a marble table, sophisticated atmosphere, high-resolution skin and fabric."),
    ("grab-long-jin", "A cinematic shot of a serene Thai woman with gentle features and fair skin. She is wearing a traditional white Thai silk uniform in a warm, candle-lit massage room. Focus on her graceful posture and smooth skin. Peaceful and exclusive atmosphere, 8k resolution."),
    ("scam-prevention", "A moody, high-contrast shot of an alert and confident Thai woman with sharp features and a sleek ponytail. She is wearing a stylish white leather jacket and standing in a dark Sukhumvit alleyway. Dramatic side lighting, urban atmosphere, cinematic grain, warning sign aesthetic."),
    ("thermae-coffee", "A mysterious night shot of a stunning Thai girl with deep-set eyes and wavy black hair. She is sitting in a corner of the legendary underground Thermae bar. Dim, moody lighting catching the contours of her smooth matte skin. Low hum of a midnight encounter, high texture detail."),
    ("windmill-pattaya", "A high-energy, vibrant shot of a beautiful Thai woman with athletic tanned skin and a playful expression. She is wearing a sparkly white party outfit and dancing under the chaotic neon lights of a Pattaya gogo bar. Motion blur in the background, ecstatic atmosphere, masterpiece.")
]

# The Base Workflow (Qwen-image 2512)
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 1024, "height": 1024, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_missing_jobs():
    print("🚀 Queuing final 7 missing categories to achieve 100% image coverage...")
    for name, prompt in MISSING_JOBS:
        print(f"Queuing: {name}...")
        for i in range(1, 4): # 3 variants per missing category
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_{name.replace('-','_')}_{i:02d}"
            workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + random.randint(1, 99999)
            
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Version {i:02d}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_missing_jobs()
    print("\n--- Final 21 tasks added! 100% completion is now within reach. ---")
