import os
import re
import json
import urllib.request
import urllib.parse
import shutil

SERVER_ADDRESS = "192.168.1.162:8188"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"
HERO_DIR = os.path.join(WORKSPACE, "src/assets/hero")
CONTENT_DIR = os.path.join(WORKSPACE, "src/content/blog")

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

def get_history():
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history") as response:
            return json.loads(response.read())
    except: return {}

def download_image(filename, subfolder, type="output"):
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    url = f"http://{SERVER_ADDRESS}/view?{params}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except: return None

def sync_images():
    history = get_history()
    os.makedirs(HERO_DIR, exist_ok=True)
    
    found_slugs = []
    for pid in history:
        out = history[pid].get('outputs', {})
        for nid in out:
            if 'images' in out[nid]:
                for img in out[nid]['images']:
                    fn = img['filename']
                    if 'ThaiNights_Auto' in fn:
                        for slug in MAPPING:
                            if slug in fn:
                                print(f"Syncing image for {slug}...")
                                data = download_image(fn, img.get('subfolder',''))
                                if data:
                                    with open(os.path.join(HERO_DIR, f"{slug}.png"), "wb") as f:
                                        f.write(data)
                                    found_slugs.append(slug)
    return found_slugs

def fix_markdowns(slugs):
    for lang in ["zh-tw", "zh-cn", "en"]:
        lang_dir = os.path.join(CONTENT_DIR, lang)
        if not os.path.exists(lang_dir): continue
        for slug in slugs:
            path = os.path.join(lang_dir, f"{slug}.md")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                img_path = f"../../../assets/hero/{slug}.png"
                # Uncomment or update heroImage
                if "# heroImage:" in content:
                    content = content.replace(f"# heroImage: \"{img_path}\"", f"heroImage: \"{img_path}\"")
                elif "heroImage:" not in content:
                    content = content.replace("---", f"---\nheroImage: \"{img_path}\"", 1)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)

if __name__ == "__main__":
    slugs = sync_images()
    if slugs:
        fix_markdowns(slugs)
        print(f"Synced {len(set(slugs))} images and updated markdowns.")
    else:
        print("No new images found to sync.")
