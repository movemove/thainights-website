import json
import urllib.request
import time
import random

SERVER_ADDRESS = "192.168.1.162:8188"

# Gourmet-specific prompts
GOURMET_JOBS = [
    ("sky_bar_luxury", "Cinematic night photography of a luxury Bangkok rooftop restaurant overlooking the city skyline. A stunning young Thai girl in an elegant white silk backless gown sitting at a glass table. She is holding a crystal champagne flute. Perfectly smooth matte skin, sophisticated features. The background features artistic city light bokeh, moonlit atmosphere, high-fashion aesthetic, 8k resolution."),
    ("riverside_dining", "Atmospheric shot of a romantic riverside restaurant on the Chao Phraya River. A beautiful Thai woman with long straight black hair wearing a white lace cocktail dress. She is sitting across a table with a glowing bowl of Tom Yum soup emitting steam. Her skin is soft and dry, reflecting the golden ambient lights of the riverboats. Peaceful and seductive vibe, high quality textures, cinematic film grain."),
    ("gourmet_detail", "Extreme close-up macro photography of an exquisite Thai fine dining dish, a beautifully plated modern Pad Thai with gold leaf accents. Next to it, a delicate female hand with clean manicured nails is reaching for a silver fork. Soft ambient lighting, shallow depth of field, high-end food styling, realistic textures, 4k.")
]

# The Base Workflow (Qwen-image 2512)
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 1216, "height": 832, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" },
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_gourmet_jobs():
    print("🍽️ Queuing Gourmet & Luxury Dining scenes...")
    for name, prompt in GOURMET_JOBS:
        print(f"Queuing: {name}...")
        for i in range(1, 3): # 2 versions each
            workflow = BASE_WORKFLOW.copy()
            workflow["108"]["inputs"]["text"] = prompt
            workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_Gourmet_{name}_{i:02d}"
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
    queue_gourmet_jobs()
