import json
import urllib.request
import urllib.parse
import time
import os
import random

SERVER_ADDRESS = "192.168.1.162:8188"
T2I_FILE = "/home/alice/.openclaw/media/inbound/t2I---56e6241b-da54-429c-90fb-3d40e47d983e.json"
I2V_FILE = "/home/alice/.openclaw/media/inbound/i2v---80644865-3986-4f82-8942-018caa0df845.json"

def send_prompt(workflow):
    p = {"prompt": workflow}
    # Handle JSON booleans and ensure UTF-8
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def upload_image(filename, subfolder, type):
    print(f"🔄 Transferring {filename} from {type} to input folder...")
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    view_url = f"http://{SERVER_ADDRESS}/view?{params}"
    upload_url = f"http://{SERVER_ADDRESS}/upload/image"
    
    try:
        with urllib.request.urlopen(view_url) as response:
            img_data = response.read()
            
        boundary = '----WebKitFormBoundary' + str(int(time.time()))
        data = []
        data.append(f'--{boundary}'.encode())
        data.append(f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(filename)}"'.encode())
        data.append('Content-Type: image/png'.encode())
        data.append(b'')
        data.append(img_data)
        data.append(f'--{boundary}--'.encode())
        payload = b'\r\n'.join(data)
        
        req = urllib.request.Request(upload_url, data=payload)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            return res['name']
    except Exception as e:
        print(f"❌ Transfer failed: {e}")
        return os.path.basename(filename)

def run_ig_pipeline():
    # 1. Load Templates
    with open(T2I_FILE, 'r') as f:
        wf_t2i = json.load(f)
    with open(I2V_FILE, 'r') as f:
        wf_i2v = json.load(f)

    print("🚀 Step 1: Generating High-Res Image (Walking in Bangkok)...")
    # Set the walking prompt
    t2i_prompt = "韩风冷色调网红美白滤镜, 19岁泰国美女，韩式网红风格，精致妆容，极致冷白皮，overexposure，浅粉色唇釉带着光泽，通体雪白如瓷器凝脂，细腻毛孔与真实绒毛清晰可见，有着Z-CUP超乳，胸部巨大，白色横条三角比基尼泳衣，走在深夜曼谷的Soi cowboy 街道上，霓虹燈光影，景深"
    wf_t2i["45"]["inputs"]["text"] = t2i_prompt
    
    # Randomize seeds
    seed = random.randint(1, 10**14)
    for node_id in wf_t2i:
        if "seed" in wf_t2i[node_id]["inputs"]:
            if node_id in ["454", "467", "479"]: # Specifically for Kevin's SeedVR2 workflow
                wf_t2i[node_id]["inputs"]["seed"] = seed + random.randint(1, 1000)

    # Queue T2I
    resp_img = send_prompt(wf_t2i)
    img_prompt_id = resp_img['prompt_id']
    print(f"  - Image Queued: {img_prompt_id}. Polling for completion...")

    # Poll for T2I result
    image_filename = None
    subfolder = ""
    while not image_filename:
        history = get_history(img_prompt_id)
        if img_prompt_id in history:
            outputs = history[img_prompt_id].get('outputs', {})
            # Look for output from node 480 (Final SeedVR2 output)
            if "480" in outputs:
                img_info = outputs["480"]['images'][0]
                image_filename = img_info['filename']
                subfolder = img_info.get('subfolder', '')
                print(f"  ✅ Image Generated: {image_filename}")
                break
        time.sleep(10)

    # 2. Transfer image to input
    final_input_fn = upload_image(image_filename, subfolder, "output")

    print(f"🚀 Step 2: Generating Cinematic Video from {final_input_fn}...")
    # Update video workflow
    wf_i2v["97"]["inputs"]["image"] = final_input_fn
    
    # Set walking video prompt
    i2v_prompt = "A cinematic video of the woman in the image walking confidently through the neon-drenched Soi Cowboy alleyway in Bangkok. The camera pans slowly. Her long dark hair flows naturally with a subtle breeze, and the vibrant red neon lights flicker in the background. High texture detail on her smooth skin and the bikini."
    wf_i2v["129:93"]["inputs"]["text"] = i2v_prompt
    
    # Randomize video seeds
    v_seed = random.randint(1, 10**14)
    if "129:86" in wf_i2v: wf_i2v["129:86"]["inputs"]["noise_seed"] = v_seed
    if "129:85" in wf_i2v: wf_i2v["129:85"]["inputs"]["noise_seed"] = v_seed
    
    # Queue Video
    resp_vid = send_prompt(wf_i2v)
    print(f"  ✅ Video Queued: {resp_vid['prompt_id']}")
    print(f"  - Results will appear in ComfyUI output/video folder.")

if __name__ == "__main__":
    try:
        run_ig_pipeline()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
