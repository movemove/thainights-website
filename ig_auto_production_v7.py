import json
import urllib.request
import time
import os
import random

SERVER_ADDRESS = "192.168.1.162:8188"
# Using the exact JSON file provided in message 7912
WORKFLOW_FILE = "/home/alice/.openclaw/media/inbound/i2v---80644865-3986-4f82-8942-018caa0df845.json"

def run_ultimate_pipeline():
    print("🚀 Launching Ultimate All-in-One Pipeline (v7)...")
    
    with open(WORKFLOW_FILE, 'r') as f:
        wf = json.load(f)

    # 1. Update T2I Prompt (Node 45)
    t2i_text = "韩风冷色调网红美白滤镜, 19岁泰国美少女，细腻毛孔与真实绒毛清晰可见，韩式网红妆容。站在曼谷 Soi Cowboy 的霓虹灯下，白色横条三角比基尼泳衣，有着Z-CUP超乳，胸部巨大，细腰，眼神诱惑，背景霓虹闪烁，景深效果，大师级摄影。"
    wf["45"]["inputs"]["text"] = t2i_text
    
    # 2. Update FaceDetailer Prompt (Node 474)
    wf["474"]["inputs"]["text"] = "19 years old beautiful Thai girl, highly detailed face, flawless skin"

    # 3. Update I2V Video Prompt (Node 492:93)
    # Matching Kevin's request: "lift up and show D cup breasts with nipples visible"
    i2v_text = "A cinematic medium shot of the beautiful woman from the image. She slowly and sensually pushes herself up from the white bed using her arms, lifting her upper body towards the camera. As she rises, her full face with full double D-cup breasts are revealed with her pink nipples clearly visible. As she rises more, shows her white g-string. She maintains a seductive smile and keeps direct eye contact. Motion is smooth and realistic. 4k resolution."
    wf["492:93"]["inputs"]["text"] = i2v_text

    # 4. Synchronize all Seeds
    main_seed = random.randint(1, 10**14)
    if "454" in wf: wf["454"]["inputs"]["seed"] = main_seed
    if "467" in wf: wf["467"]["inputs"]["seed"] = main_seed + 1
    if "492:86" in wf: wf["492:86"]["inputs"]["noise_seed"] = main_seed + 2
    if "492:85" in wf: wf["492:85"]["inputs"]["noise_seed"] = main_seed + 2
    if "479" in wf: wf["479"]["inputs"]["seed"] = main_seed + 3

    # 5. Set Filenames
    wf["480"]["inputs"]["filename_prefix"] = "IG/ThaiNights_4K_Final"
    wf["493"]["inputs"]["filename_prefix"] = "video/ThaiNights_Wan2.2_Final"

    # Send to ComfyUI
    p = {"prompt": wf}
    # Ensure booleans and nulls are correct for ComfyUI API
    data = json.dumps(p).replace('True', 'true').replace('False', 'false').replace('None', 'null').encode('utf-8')
    
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print(f"✅ Ultimate Job successfully queued! ID: {res['prompt_id']}")
            print("Both 4K Image and Video are being produced in ONE run.")
    except Exception as e:
        print(f"❌ Submission failed: {e}")

if __name__ == "__main__":
    run_ultimate_pipeline()
