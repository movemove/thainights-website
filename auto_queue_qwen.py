import json
import urllib.request
import time

# Configuration
SERVER_ADDRESS = "192.168.1.162:8188" # Kevin's ComfyUI Address

# The Base Workflow provided by Kevin
BASE_WORKFLOW = {
  "103": {
    "inputs": { "vae_name": "qwen_image_vae.safetensors" },
    "class_type": "VAELoader"
  },
  "104": {
    "inputs": {
      "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
      "type": "qwen_image",
      "device": "default"
    },
    "class_type": "CLIPLoader"
  },
  "105": {
    "inputs": {
      "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader"
  },
  "106": {
    "inputs": {
      "seed": 123456789,
      "steps": 2,
      "cfg": 1,
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": 1,
      "model": ["110", 0],
      "positive": ["108", 0],
      "negative": ["128", 0],
      "latent_image": ["107", 0]
    },
    "class_type": "KSampler"
  },
  "107": {
    "inputs": { "width": 1328, "height": 1328, "batch_size": 1 },
    "class_type": "EmptySD3LatentImage"
  },
  "108": {
    "inputs": { "text": "", "clip": ["104", 0] },
    "class_type": "CLIPTextEncode"
  },
  "109": {
    "inputs": { "samples": ["106", 0], "vae": ["103", 0] },
    "class_type": "VAEDecode"
  },
  "110": {
    "inputs": { "shift": 3, "model": ["114", 0] },
    "class_type": "ModelSamplingAuraFlow"
  },
  "114": {
    "inputs": {
      "lora_name": "Wuli-Qwen-Image-2512-Turbo-LoRA-2steps-V1.0-bf16.safetensors",
      "strength_model": 1,
      "model": ["105", 0]
    },
    "class_type": "LoraLoaderModelOnly"
  },
  "123": {
    "inputs": { "filename_prefix": "", "images": ["109", 0] },
    "class_type": "SaveImage"
  },
  "128": {
    "inputs": { "conditioning": ["108", 0] },
    "class_type": "ConditioningZeroOut"
  }
}

# The 18 Categories and their sensory, non-wet prompts optimized for Qwen
JOBS = [
    ("nana_plaza", "A high-fashion night photography of a beautiful Thai woman in a crisp white micro bikini, standing on a balcony at Nana Plaza. Her skin is perfectly smooth and matte, glowing under soft purple and pink ambient neon. Sophisticated, alluring gaze, high-resolution textures of the white lace. Background features artistic bokeh of Bangkok city lights."),
    ("soi_cowboy", "A cinematic portrait of a stunning Thai girl in a simple white string bikini, leaning against a wall in Soi Cowboy. The lighting is dominated by a single red neon sign creating a dramatic rim light on her smooth, flawless matte skin. Professional photo studio quality, deep shadows and vibrant colors, shot with 85mm lens."),
    ("patpong", "Moody night photography of Patpong Market. A gorgeous Thai woman in an elegant white bikini top walking through the neon-lit street. Her skin is soft and dry, reflecting the ambient street lights. 1990s vintage film style, rich deep colors, cinematic grain, detailed facial features."),
    ("thermae", "A mysterious Thai woman in a white silk bikini sitting in a dimly lit corner of a legendary basement bar. Her skin is smooth and natural with soft light catching the contours of her face. Quiet and intense atmosphere, raw energy of a midnight encounter. Flawless skin texture, 4k cinematic detail."),
    ("soi6_pattaya", "Bright but atmospheric afternoon in Pattaya Soi 6. A sexy Thai girl with a perfectly tanned, smooth body wearing a tiny white sporty bikini. She stands in front of a vibrant bar entrance. Sharp sunlight shadows mixed with neon glow, high quality skin shaders, no moisture, pure clean skin."),
    ("soapy_massage", "Luxury Thai spa interior with soft blue ambient lighting. A stunning Thai woman in a sheer white lace outfit reclining gracefully. Her skin is like velvet, perfectly clean and dry. Warm atmospheric glow, high-end lifestyle photography, intricate lace details, serene and elegant."),
    ("massage_guide", "A beautiful Thai masseuse in a traditional white silk uniform standing in a zen-like massage room. Warm candle lighting, serene expression, smooth matte skin texture. High quality fabrics, peaceful and exclusive atmosphere, cinematic masterpiece."),
    ("grab_long_jin", "An intense, cinematic shot of a skilled Thai practitioner in a white outfit inside a sacred therapy room. Dim, moody lighting focusing on the focused expression and smooth skin. Ancient Thai scrolls in the background, mysterious and powerful energy, 8k resolution."),
    ("bj_bars", "Nightlife photography in a Bangkok BJ bar. A seductive Thai girl in a white bikini glimpsed through a neon-lit curtain. Moody lighting, focus on her intense gaze and smooth facial features. High contrast, urban nightlife aesthetic, cinematic framing."),
    ("gentlemens_clubs", "An elegant scene inside an upscale Bangkok VIP club. A gorgeous Thai model wearing an expensive white silk bikini is reclining on a luxury sofa. Her skin is soft and velvet-like under the warm amber spotlights. Expensive and exclusive feel, clean skin, 4k detail."),
    ("thonglo_ktv", "Beautiful Thai girl in a white cocktail-style bikini inside a high-end KTV suite in Thong Lo. She is holding a golden microphone. Glossy karaoke lights reflecting on her smooth, dry skin. Luxury spirits on the table, intimate and upscale vibe."),
    ("eden_club", "A private sensory party at Eden Club Bangkok. An exotic Thai girl in a white lace bikini, mysterious forbidden fruit theme. Deep red lighting, dramatic shadows, focus on her smooth skin and seductive pose. Masterpiece of dark sensuality."),
    ("jodd_fairs", "Casual yet alluring Thai girl in a white bikini top and denim shorts at a Jodd Fairs outdoor bar. Night market background with blurred crowds and lights. Her skin is natural and matte. Vibrant night life energy, realistic street photography."),
    ("walking_street", "Energetic Thai girl in a white micro bikini dancing at the entrance of Pattaya Walking Street. A sea of neon lights in the background. Her skin is smooth and clean under the flashing lights. Chaotic and colorful atmosphere, high-speed photography style."),
    ("lk_metro", "A gorgeous Thai girl in a white bikini leaning against a textured bar wall in LK Metro, Pattaya. Neon glow from a nearby sign casting a soft pink light on her smooth skin. Intimate and quiet moment, high resolution, filmic look."),
    ("scam_prevention", "Cinematic dark mood, high contrast. A beautiful Thai girl in a white bikini holding a drink in a mysterious back alley. Shadow play across her smooth skin. Warning sign vibe, intense and sharp focus, 8k resolution."),
    ("budget_guide", "A clever and confident Thai girl in a white bikini holding a fan of Thai Baht cash. Neon background in a central Bangkok district. Her skin is flawless and matte. Smart luxury theme, sharp details, cinematic lighting."),
    ("pattaya_guide", "Wide aerial-style shot of Pattaya bay at night with a vibrant neon coastline. In the foreground, a stunning Thai girl in a white bikini looking out at the sea. Her skin is smooth under the moonlight. Masterpiece of tropical nightlife.")
]

def queue_jobs():
    for name, prompt in JOBS:
        print(f"Preparing to queue: {name}...")
        for i in range(1, 4): # Generate 3 variants per category
            # Clone base workflow
            current_workflow = BASE_WORKFLOW.copy()
            
            # Inject dynamic data
            current_workflow["108"]["inputs"]["text"] = prompt
            current_workflow["123"]["inputs"]["filename_prefix"] = f"ThaiNights_{name}_{i:02d}"
            current_workflow["106"]["inputs"]["seed"] = int(time.time() * 1000) + (i * 123)
            
            # Send to ComfyUI API
            p = {"prompt": current_workflow}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
            
            try:
                urllib.request.urlopen(req)
                print(f"  [OK] Queued version {i:02d}")
                time.sleep(0.5) # Brief pause to avoid overwhelming the listener
            except Exception as e:
                print(f"  [Error] Failed to queue {name}: {e}")
                break

if __name__ == "__main__":
    queue_jobs()
    print("\n--- All jobs have been successfully sent to the ComfyUI queue! ---")
    print("Your RTX 5060 Ti should be working now. Check your ComfyUI window.")
