import os
import re
import json
import urllib.request
import urllib.parse

SERVER_ADDRESS = "192.168.1.162:8188"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"
HERO_DIR = os.path.join(WORKSPACE, "src/assets/hero")
CONTENT_DIR = os.path.join(WORKSPACE, "src/content")

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

def fix_all_images():
    history = get_history()
    available_images = os.listdir(HERO_DIR)
    
    # Map from history filenames to target slugs
    history_map = {}
    for pid in history:
        out = history[pid].get('outputs', {})
        for nid in out:
            if 'images' in out[nid]:
                for img in out[nid]['images']:
                    fn = img['filename']
                    if 'ThaiNights' in fn:
                        # Extract slug if possible
                        parts = fn.split('_')
                        if len(parts) >= 3:
                            slug = parts[2]
                            if slug not in history_map:
                                history_map[slug] = (fn, img.get('subfolder', ''))

    # Sweep all markdown files
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                slug = file.replace(".md", "")
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if heroImage is present and valid
                match = re.search(r"heroImage: ['\"](.*?)['\"]", content)
                has_valid = False
                if match:
                    img_name = os.path.basename(match.group(1))
                    if img_name in available_images:
                        has_valid = True
                    else:
                        print(f"Broken link in {path}: {img_name}")
                
                if not has_valid:
                    # Try to find in assets
                    if f"{slug}.png" in available_images:
                        target_img = f"{slug}.png"
                    elif f"{slug}.jpg" in available_images:
                        target_img = f"{slug}.jpg"
                    else:
                        # Try to find in history map
                        found_in_hist = None
                        for key in history_map:
                            if key in slug:
                                found_in_hist = history_map[key]
                                break
                        
                        if found_in_hist:
                            fn, sub = found_in_hist
                            print(f"Downloading {fn} for {slug}...")
                            data = download_image(fn, sub)
                            if data:
                                with open(os.path.join(HERO_DIR, f"{slug}.png"), "wb") as f:
                                    f.write(data)
                                target_img = f"{slug}.png"
                                available_images.append(target_img)
                            else: target_img = None
                        else: target_img = None
                    
                    if target_img:
                        img_ref = f"../../../assets/hero/{target_img}"
                        if "heroImage:" in content:
                            content = re.sub(r"heroImage:.*", f"heroImage: '{img_ref}'", content)
                        else:
                            content = content.replace("---", f"---\nheroImage: '{img_ref}'", 1)
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"FIXED {path} with {target_img}")

if __name__ == "__main__":
    fix_all_images()
