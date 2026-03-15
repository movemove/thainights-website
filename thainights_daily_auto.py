import json
import urllib.request
import urllib.parse
import time
import os
import random
import subprocess
import datetime

# --- Configuration ---
SERVER_ADDRESS = "192.168.1.162:8188"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"
GOG_PW = "1072"

# Workflow Templates (Based on Kevin's provided JSONs)
T2I_TEMPLATE_FILE = "/home/alice/.openclaw/media/inbound/t2I---56e6241b-da54-429c-90fb-3d40e47d983e.json"
I2V_TEMPLATE_FILE = "/home/alice/.openclaw/media/inbound/i2v---80644865-3986-4f82-8942-018caa0df845.json"

CATEGORIES = [
    "Nana Plaza", "Soi Cowboy", "Patpong", "Thermae Coffee", "Soi 6 Pattaya",
    "Walking Street Pattaya", "Soapy Massage", "Grab Long Jin", "Gentlemen's Clubs",
    "Thong Lo KTV", "Eden Club", "Jodd Fairs"
]

OUTFITS = [
    "a tiny white string bikini", "a red velvet bodycon dress", "black sheer lace lingerie",
    "a Pikachu-themed bikini", "a modern gold Thai silk wrap dress", "a silver metallic mini skirt"
]

SKINS = ["极致冷白皮", "健康小麦色皮肤", "阳光吻过的蜜糖色肌肤"]

# --- Helper Functions ---

def call_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return json.loads(res['response'])

def send_comfy_prompt(workflow):
    p = {"prompt": workflow}
    data = json.dumps(p).replace('True', 'true').replace('False', 'false').encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_comfy_history(prompt_id):
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
            return json.loads(response.read())
    except: return {}

def download_comfy_file(filename, subfolder, type="output"):
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    url = f"http://{SERVER_ADDRESS}/view?{params}"
    dest = os.path.join(WORKSPACE, "public", "auto", filename)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(url) as response:
        with open(dest, 'wb') as f:
            f.write(response.read())
    return dest

def upload_to_comfy_input(local_path):
    filename = os.path.basename(local_path)
    url = f"http://{SERVER_ADDRESS}/upload/image"
    boundary = '----WebKitFormBoundaryAuto' + str(int(time.time()))
    with open(local_path, 'rb') as f:
        img_data = f.read()
    data = [f'--{boundary}', f'Content-Disposition: form-data; name="image"; filename="{filename}"', 'Content-Type: image/png', '', img_data, f'--{boundary}--']
    body = b'\r\n'.join([x.encode() if isinstance(x, str) else x for x in data])
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())['name']

# --- Main Logic ---

def run_daily_update():
    category = random.choice(CATEGORIES)
    print(f"🌟 Starting Daily Update for Category: {category}")

    # 1. Generate Story and Prompts via LLM
    llm_prompt = f"""You are a writer for thainights.net. Write an explicit, 500+ word story in Traditional Chinese about an encounter in {category}.
    Style: "Sensual Spiral" (descriptive, tactile, intense). Include sex details like oral, intercourse, glans, vagina, nipples.
    Also provide:
    1. A short title.
    2. A brief description for SEO.
    3. A Qwen-optimized image prompt (Natural language, high fashion, no wet skin, large breasts, slender waist).
    4. A Wan 2.2-optimized video prompt (Describing normal speed movement like lifting up, walking, or beckoning).
    Output as JSON: {{"title": "...", "desc": "...", "content": "...", "img_prompt": "...", "vid_prompt": "..."}}"""
    
    story_data = call_llm(llm_prompt)
    slug = category.lower().replace(' ', '-').replace("'", "")
    
    # 2. Generate Image (T2I)
    print("📸 Step 1: Generating 4K Image...")
    with open(T2I_TEMPLATE_FILE, 'r') as f:
        wf_t2i = json.load(f)
    
    wf_t2i["45"]["inputs"]["text"] = f"韩风冷色调网红美白滤镜, 19岁泰国美女, {random.choice(SKINS)}, Z-CUP超乳, 细腰, {random.choice(OUTFITS)}, {story_data['img_prompt']}"
    wf_t2i.pop("64", None); wf_t2i.pop("468", None) # Remove previewers
    
    seed = random.randint(1, 10**14)
    for sid in ["454", "467", "479"]:
        if sid in wf_t2i: wf_t2i[sid]["inputs"]["seed"] = seed + random.randint(1, 100)

    res_img = send_comfy_prompt(wf_t2i)
    img_id = res_img['prompt_id']
    
    image_fn, sub = None, ""
    while not image_fn:
        hist = get_comfy_history(img_id)
        if img_id in hist:
            out = hist[img_id].get('outputs', {})
            if "480" in out:
                image_fn = out["480"]['images'][0]['filename']
                sub = out["480"]['images'][0].get('subfolder', '')
        if not image_filename: time.sleep(15)
    
    local_img = download_comfy_file(image_fn, sub)
    input_img_fn = upload_to_comfy_input(local_img)

    # 3. Generate Video (I2V)
    print("🎬 Step 2: Generating Wan 2.2 Video...")
    with open(I2V_TEMPLATE_FILE, 'r') as f:
        wf_i2v = json.load(f)
    
    wf_i2v["97"]["inputs"]["image"] = input_img_fn
    wf_i2v["129:93"]["inputs"]["text"] = story_data['vid_prompt']
    wf_i2v["129:98"]["inputs"]["length"] = 121 # 5 seconds for stability
    
    res_vid = send_comfy_prompt(wf_i2v)
    vid_id = res_vid['prompt_id']
    
    video_fn = None
    while not video_fn:
        hist = get_comfy_history(vid_id)
        if vid_id in hist:
            out = hist[vid_id].get('outputs', {})
            # Wan nodes often output in node 108 or similar
            for nid in out:
                items = out[nid].get('gifs', []) + out[nid].get('images', [])
                for item in items:
                    if item['filename'].endswith('.mp4'):
                        video_fn = item['filename']
                        v_sub = item.get('subfolder', '')
                        break
        if not video_fn: time.sleep(30)
    
    local_vid = download_comfy_file(video_fn, v_sub)
    
    # 4. Create Markdown Files and Push
    print("🚀 Step 3: Updating Website...")
    # (Simplified: Writing zh-tw only for code demo, but real script would do all 3)
    md_content = f"""---
title: "{story_data['title']}"
description: "{story_data['desc']}"
pubDate: "{datetime.date.today().isoformat()}"
heroImage: "../../../assets/hero/{slug}.png"
---

{story_data['content']}

<video autoplay loop muted playsinline style="width: 100%; border-radius: 12px; margin: 2rem 0;"><source src="/videos/{slug}_daily.mp4" type="video/mp4"></video>
"""
    # Move files to final positions
    shutil.copy(local_img, os.path.join(WORKSPACE, "src/assets/hero", f"{slug}.png"))
    shutil.copy(local_vid, os.path.join(WORKSPACE, "public/videos", f"{slug}_daily.mp4"))
    
    with open(os.path.join(WORKSPACE, "src/content/stories/zh-tw", f"{slug}.md"), "w") as f:
        f.write(md_content)
    
    # Git Push
    subprocess.run(["git", "add", "."], cwd=WORKSPACE)
    subprocess.run(["git", "commit", "-m", f"Daily Auto Post: {story_data['title']}"], cwd=WORKSPACE)
    subprocess.run(["git", "push", "origin", "main"], cwd=WORKSPACE)
    print("✅ Daily update successfully published!")

if __name__ == "__main__":
    run_daily_update()
