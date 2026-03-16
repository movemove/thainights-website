import os
import re
import json
import urllib.request
import urllib.parse
import time

SERVER_ADDRESS = "192.168.1.162:8188"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"
HERO_DIR = os.path.join(WORKSPACE, "src/assets/hero")
CONTENT_DIR = os.path.join(WORKSPACE, "src/content/blog/zh-tw")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"

MAPPING = {
    "billboard-nana-plaza": "billboard-nana-plaza",
    "rainbow-4-nana-plaza": "rainbow-4-nana-plaza",
    "sapphire-club-soi-15": "sapphire-club-soi-15",
    "pin-up-agogo-pattaya": "pin-up-agogo-pattaya",
    "the-lord-palace-bangkok": "the-lord-palace-bangkok",
    "emmanuelle-soapy-massage": "emmanuelle-soapy-massage",
    "prink-bj-bar-sukhumvit": "prink-bj-bar-sukhumvit",
    "the-pimp-gentlemens-club": "the-pimp-gentlemens-club",
    "sherbet-ekamai-bangkok": "sherbet-ekamai-bangkok",
    "eden-club-bangkok": "eden-club-bangkok"
}

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res['response'].strip()

def download_image(filename, subfolder, type="output"):
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    url = f"http://{SERVER_ADDRESS}/view?{params}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except: return None

def get_history():
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history") as response:
            return json.loads(response.read())
    except: return {}

def full_sync_and_fix():
    # 1. Sync Images
    print("Syncing images...")
    history = get_history()
    os.makedirs(HERO_DIR, exist_ok=True)
    synced_slugs = []
    
    for pid in history:
        out = history[pid].get('outputs', {})
        for nid in out:
            if 'images' in out[nid]:
                for img in out[nid]['images']:
                    fn = img['filename']
                    if 'ThaiNights_Auto' in fn:
                        for slug in MAPPING:
                            if slug in fn:
                                data = download_image(fn, img.get('subfolder',''))
                                if data:
                                    with open(os.path.join(HERO_DIR, f"{slug}.png"), "wb") as f:
                                        f.write(data)
                                    synced_slugs.append(slug)

    # 2. Fix Translations and heroImage in MD files
    print("Fixing translations and heroImage references...")
    files = os.listdir(CONTENT_DIR)
    for file in files:
        if not file.endswith(".md"): continue
        path = os.path.join(CONTENT_DIR, file)
        slug = file.replace(".md", "")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix heroImage (Uncomment if file exists)
        img_path = f"../../../assets/hero/{slug}.png"
        if os.path.exists(os.path.join(HERO_DIR, f"{slug}.png")):
            content = content.replace(f"# heroImage: \"{img_path}\"", f"heroImage: \"{img_path}\"")
            if "heroImage:" not in content:
                content = content.replace("---", f"---\nheroImage: \"{img_path}\"", 1)
        
        # Detect if English
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]{3,}', content))
        
        if english_words > 50 and chinese_chars < 100:
            print(f"  Translating {file}...")
            parts = content.split('---', 2)
            if len(parts) >= 3:
                header, body = parts[1], parts[2]
                
                # Translate Title
                title_match = re.search(r'title: "(.*?)"', header)
                if title_match:
                    orig_title = title_match.group(1)
                    new_title = call_ollama(f"Translate this title to Traditional Chinese: {orig_title}").strip(' "')
                    header = header.replace(orig_title, new_title)
                
                # Translate Body
                trans_prompt = f"Translate the following erotic review into Traditional Chinese. Maintain the explicit 'Sensual Spiral' style. Output ONLY the translated text.\n\n{body}"
                new_body = call_ollama(trans_prompt)
                content = f"---{header}---{new_body}"
                
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    full_sync_and_fix()
