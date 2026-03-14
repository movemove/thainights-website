import json
import urllib.request
import urllib.parse
import time
import os
import random

SERVER_ADDRESS = "192.168.1.162:8188"
T2I_FILE = "/home/alice/.openclaw/media/inbound/Moody_Text2Img_workflow---e3eeed6a-663d-4129-8cf1-f8566b861e68.json"
I2V_FILE = "/home/alice/.openclaw/media/inbound/i2v---80644865-3986-4f82-8942-018caa0df845.json"

def send_prompt(workflow):
    p = {"prompt": workflow}
    # Standard json.dumps is enough. Do NOT replace True/False/None strings!
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def upload_image(filename, subfolder, type):
    print(f"🔄 Transferring {filename} to input folder...")
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    view_url = f"http://{SERVER_ADDRESS}/view?{params}"
    upload_url = f"http://{SERVER_ADDRESS}/upload/image"
    try:
        with urllib.request.urlopen(view_url) as response:
            img_data = response.read()
        boundary = '----WebKitFormBoundary' + str(int(time.time()))
        data = [f'--{boundary}', f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(filename)}"', 'Content-Type: image/png', '', img_data, f'--{boundary}--']
        body = b'\r\n'.join([x.encode() if isinstance(x, str) else x for x in data])
        req = urllib.request.Request(upload_url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())['name']
    except Exception as e:
        print(f"❌ Transfer failed: {e}")
        return os.path.basename(filename)

# Variety Pools
SKINS = ["极致冷白皮", "健康小麦色皮肤", "阳光吻过的蜜糖色肌肤", "如瓷器般的白皙肤质"]
BODIES = ["Z-CUP超乳，细腰，沙漏型身材", "丰满诱人的丰乳肥臀曲线", "高挑且有着极致胸部比例的身材", "肉感十足且凹凸有致的火辣身材"]
OUTFITS = ["白色横条三角比基尼泳衣", "红色蕾丝半透明内衣", "紧身豹纹连体裙", "浅蓝色丝绸睡袍"]

def run_v8_pipeline():
    print("🚀 Stage 1: Generating 4K Master Photo with Variety...")
    with open(T2I_FILE, 'r') as f:
        wf_t2i = json.load(f)
    
    skin = random.choice(SKINS)
    body = random.choice(BODIES)
    outfit = random.choice(OUTFITS)
    
    # Update Prompt (Node 45) - Enhanced with variety and no wetness
    t2i_text = f"韩风冷色调网红美白滤镜, 19岁泰国美少女，{skin}，{body}，穿着{outfit}，走在深夜曼谷的Soi cowboy 街道上，霓虹燈光影，大師級攝影，細膩毛孔清晰可見，肌膚絲滑無水漬。"
    wf_t2i["45"]["inputs"]["text"] = t2i_text
    
    print(f"  - Characteristics: {skin}, {body}")
    
    # Fix Seeds
    seed = random.randint(1, 10**14)
    if "454" in wf_t2i: wf_t2i["454"]["inputs"]["seed"] = seed
    if "467" in wf_t2i: wf_t2i["467"]["inputs"]["seed"] = seed + 1
    
    # Remove Comparer nodes to avoid validation errors with temporary files
    wf_t2i.pop("64", None)
    wf_t2i.pop("468", None)
    wf_t2i.pop("200", None)
    wf_t2i.pop("455", None)
    wf_t2i.pop("464", None)

    resp_img = send_prompt(wf_t2i)
    img_id = resp_img['prompt_id']
    print(f"  - Image Job: {img_id}. Waiting for 4K output...")

    image_fn, sub = None, ""
    while not image_fn:
        h = get_history(img_id)
        if img_id in h:
            out = h[img_id].get('outputs', {})
            # Kevin's workflow saves the final 4K at node 480
            if "480" in out:
                image_fn = out["480"]['images'][0]['filename']
                sub = out["480"]['images'][0].get('subfolder', '')
                print(f"  ✅ 4K Image Ready: {image_fn}")
                break
        time.sleep(10)

    # Transfer
    input_fn = upload_image(image_fn, sub, "output")

    print(f"🚀 Stage 2: Producing Wan 2.2 Video from {input_fn} (Normal Speed)...")
    with open(I2V_FILE, 'r') as f:
        wf_i2v = json.load(f)
    
    # Inject Image & Prompt - Removed 'slowly', added 'natural real-time speed'
    wf_i2v["97"]["inputs"]["image"] = input_fn
    wf_i2v["492:93"]["inputs"]["text"] = "A cinematic video of the woman from the image at natural real-time speed. She energetically pushes herself up from the bed, lifting her upper body. Full double D-cup breasts and pink nipples revealed. The motion is smooth, vibrant and realistic. 4k resolution."
    
    # Randomize video seeds
    v_seed = random.randint(1, 10**14)
    if "129:86" in wf_i2v: wf_i2v["129:86"]["inputs"]["noise_seed"] = v_seed
    if "129:85" in wf_i2v: wf_i2v["129:85"]["inputs"]["noise_seed"] = v_seed

    resp_vid = send_prompt(wf_i2v)
    print(f"  ✅ Video Job Queued: {resp_vid['prompt_id']}")

if __name__ == "__main__":
    try:
        run_v8_pipeline()
    except Exception as e:
        print(f"FATAL: {e}")
