import json
import urllib.request
import time
import os
import random
import datetime
import re

# --- Configuration ---
SERVER_ADDRESS = "192.168.1.162:8188"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"

# --- Master Image Workflow Template (Kevin's Best Settings) ---
T2I_WORKFLOW = {
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
 "446": { "inputs": { "PowerLoraLoaderHeaderWidget": { "type": "PowerLoraLoaderHeaderWidget" }, "➕ Add Lora": "", "model": [ "46", 0 ], "clip": [ "39", 0 ] }, "class_type": "Power Lora Loader (rgthree)" },
 "450": { "inputs": { "image": [ "129", 0 ] }, "class_type": "GetImageSize" },
 "452": { "inputs": { "samples": [ "483", 0 ], "vae": [ "40", 0 ] }, "class_type": "VAEDecode" },
 "454": { "inputs": { "seed": 0 }, "class_type": "Seed (rgthree)" },
 "471": { "inputs": { "filename_prefix": "", "images": [ "170", 0 ] }, "class_type": "SaveImage" },
 "483": { "inputs": { "add_noise": "enable", "noise_seed": [ "454", 0 ], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 0, "end_at_step": 7, "return_with_leftover_noise": "enable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "443", 0 ] }, "class_type": "KSamplerAdvanced" },
 "484": { "inputs": { "add_noise": "disable", "noise_seed": [ "488", 0 ], "steps": 8, "cfg": 1, "sampler_name": "res_multistep", "scheduler": "beta", "start_at_step": 4, "end_at_step": 999, "return_with_leftover_noise": "disable", "model": [ "47", 0 ], "positive": [ "45", 0 ], "negative": [ "42", 0 ], "latent_image": [ "485", 0 ] }, "class_type": "KSamplerAdvanced" },
 "485": { "inputs": { "upscale_method": "bislerp", "scale_by": 1.7, "samples": [ "483", 0 ] }, "class_type": "LatentUpscaleBy" },
 "487": { "inputs": { "value": 0 }, "class_type": "PrimitiveInt" },
 "488": { "inputs": { "value": "a+b", "a": [ "487", 0 ], "b": [ "454", 0 ] }, "class_type": "SimpleMath+" }
}

IMAGE_FORMULA = "韩风冷色调网红美白滤镜, 19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大到人类极限，胸部下垂严重，(穿着白色丝绸挂脖比基尼:1.4)，(完全不透光:1.5)，(絕對不露出陰部:1.8)，"

# --- Core Content Generation ---

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        raw = res['response'].strip()
        # Extract JSON if it's wrapped in code blocks
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            return json_match.group(0)
        return raw

def generate_full_article_set(category, topic):
    print(f"🛠️  Generating content for: {topic}")
    
    # 1. Meta & Content (Traditional Chinese)
    prompt = f"""You are an adult content writer for thainights.net. 
    Write a "Sensual Spiral" review for {topic} in the category {category}.
    Focus: Tactile sensations, atmosphere, and "meat bath" vibes.
    Length: 600+ words.
    Include sex details if appropriate for the story (oral, intercourse, glans, vagina, nipples).
    Output as JSON: {{"title": "...", "description": "...", "content": "...", "img_prompt": "a short english description of the girl at the location"}}"""
    
    raw_json = call_ollama(prompt)
    data_tw = json.loads(raw_json)
    
    # 2. Translate to CN and EN
    print(f"  Translating...")
    trans_prompt = f"Translate the following JSON content into Simplified Chinese and English. Output as JSON with keys 'cn' and 'en':\n{raw_json}"
    trans_data = json.loads(call_ollama(trans_prompt))
    
    return {
        "zh-tw": data_tw,
        "zh-cn": trans_data['cn'],
        "en": trans_data['en']
    }

def trigger_comfy_image(slug, img_prompt):
    print(f"🎨 Triggering ComfyUI for {slug}...")
    full_prompt = f"{IMAGE_FORMULA} {img_prompt}, perfectly smooth skin, cinematic lighting, masterpiece."
    
    wf = json.loads(json.dumps(T2I_WORKFLOW))
    wf["45"]["inputs"]["text"] = full_prompt
    wf["471"]["inputs"]["filename_prefix"] = f"ThaiNights_Auto_{slug}"
    wf["9"]["inputs"]["filename_prefix"] = f"ThaiNights_Auto_{slug}"
    wf["454"]["inputs"]["seed"] = random.randint(1, 999999999)
    
    p = {"prompt": wf}
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=json.dumps(p).encode('utf-8'))
    try:
        urllib.request.urlopen(req)
        print(f"  [OK] Image job queued.")
    except Exception as e:
        print(f"  [Error] ComfyUI failed: {e}")

def save_and_publish(article_set, slug):
    for lang, data in article_set.items():
        path = os.path.join(WORKSPACE, f"src/content/blog/{lang}/{slug}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # We use the slug.png as a placeholder; Alice will sync it later.
        md = f"""---
title: "{data['title']}"
description: "{data['description']}"
pubDate: "{datetime.date.today().isoformat()}"
heroImage: "../../../assets/hero/{slug}.png"
---

{data['content']}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
    print(f"✅ Published {slug} across all languages.")

if __name__ == "__main__":
    # The Big Production Batch
    BATCH = [
        ("Bangkok Bars", "Billboard Nana Plaza"),
        ("Bangkok Bars", "Rainbow 4 Nana Plaza"),
        ("Pattaya Nightlife", "Sapphire Club Soi 15"),
        ("Pattaya Nightlife", "Pin-up Agogo Pattaya"),
        ("Massage & SPA", "The Lord Palace Bangkok"),
        ("Massage & SPA", "Emmanuelle Soapy Massage"),
        ("Massage & SPA", "Prink BJ Bar Sukhumvit"),
        ("Premium & Niche", "The Pimp Gentlemen's Club"),
        ("Premium & Niche", "Sherbet Ekamai Bangkok"),
        ("Premium & Niche", "Eden Club Bangkok")
    ]
    
    for cat, topic in BATCH:
        try:
            slug = topic.lower().replace(' ', '-').replace("'", "").replace('"', '')
            articles = generate_full_article_set(cat, topic)
            save_and_publish(articles, slug)
            # Trigger image generation matching the slug
            trigger_comfy_image(slug, articles['zh-tw']['img_prompt'])
            time.sleep(2)
        except Exception as e:
            print(f"❌ Failed to process {topic}: {e}")
    
    # Final Git Sync
    print("🌍 Pushing to GitHub...")
    os.chdir(WORKSPACE)
    os.system("git add . && git commit -m 'Auto-Content: Batch of 10 high-quality explicit reviews with automated image queuing' && git push origin main")
