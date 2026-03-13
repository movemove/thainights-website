import json
import urllib.request
import time
import random

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188"

# The Base Workflow
BASE_WORKFLOW = {
  "103": { "inputs": { "vae_name": "qwen_image_vae.safetensors" }, "class_type": "VAELoader" },
  "104": { "inputs": { "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default" }, "class_type": "CLIPLoader" },
  "105": { "inputs": { "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
  "106": { "inputs": { "seed": 0, "steps": 2, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1, "model": ["110", 0], "positive": ["108", 0], "negative": ["128", 0], "latent_image": ["107", 0] }, "class_type": "KSampler" },
  "107": { "inputs": { "width": 832, "height": 1216, "batch_size": 1 }, "class_type": "EmptySD3LatentImage" }, # Portrait for better heel emphasis
  "108": { "inputs": { "text": "", "clip": ["104", 0] }, "class_type": "CLIPTextEncode" },
  "109": { "inputs": { "samples": ["106", 0], "vae": ["103", 0] }, "class_type": "VAEDecode" },
  "110": { "inputs": { "shift": 3, "model": ["114", 0] }, "class_type": "ModelSamplingAuraFlow" },
  "114": { "inputs": { "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors", "strength_model": 1, "model": ["105", 0] }, "class_type": "LoraLoaderModelOnly" },
  "123": { "inputs": { "filename_prefix": "", "images": ["109", 0] }, "class_type": "SaveImage" },
  "128": { "inputs": { "conditioning": ["108", 0] }, "class_type": "ConditioningZeroOut" }
}

def queue_heels_jobs():
    print("Queuing High Heels focused scenes...")
    
    # Specific prompts focusing on the allure of high heels
    heels_prompts = [
        # Full body catwalk style
        "Cinematic full body shot of a stunning Thai girl walking towards the camera on a neon-lit stage. She is wearing sky-high white stiletto heels that elongate her perfectly tanned, smooth legs. She wears a minimalist white micro bikini. Hot pink neon reflections on the glossy floor. Sharp focus on the heels and posture, high-fashion aesthetic, 4k.",
        
        # Detail shot / sitting
        "A sensual close-up shot of a gorgeous Thai woman's legs as she sits on a high velvet bar stool. She is wearing elegant white strapped high heels. One foot is slightly arched, showcasing the curve of the shoe. Smooth, matte skin texture. The background is a blurry night club with golden amber bokeh. Filmic atmosphere, extremely detailed leather and skin.",
        
        # Leaning against bar
        "Low angle shot of a hot Thai girl leaning against a neon-lit counter in a dark Bangkok bar. She is wearing a white silk dress-style bikini and dazzling white high heels. The low camera angle emphasizes her height and the sharp stilettos. Soft red neon rim lighting on her legs. No wetness, just clean, high-end photography style, masterpiece."
    ]

    for i, prompt in enumerate(heels_prompts, 1):
        workflow = BASE_WORKFLOW.copy()
        workflow["108"]["inputs"]["text"] = prompt
        workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_high_heels_{i:02d}"
        workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + (i * 77)
        
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        try:
            urllib.request.urlopen(req)
            print(f"  [OK] High Heels job {i:02d} queued.")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Error]: {e}")

if __name__ == "__main__":
    queue_heels_jobs()
    print("\n--- High Heels collection successfully added to the spiral! ---")
