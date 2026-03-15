import json
import urllib.request
import urllib.parse
import os
import shutil
import re

SERVER_ADDRESS = '192.168.1.162:8188'
WORKSPACE = '/home/alice/.openclaw/workspace/thainights_pages'
HERO_DIR = os.path.join(WORKSPACE, 'src/assets/hero')
CONTENT_DIR = os.path.join(WORKSPACE, 'src/content/blog')

# Map of prefix/keywords to blog slugs
MAPPING = {
    "nana": "nana-plaza",
    "cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae": "thermae-coffee",
    "soi6": "soi6-pattaya",
    "soapy": "soapy-massage-deep",
    "massage": "massage-guide",
    "longjin": "grab-long-jin",
    "bj": "bangkok-bj-bars",
    "gentlemen": "gentlemens-clubs",
    "ktv": "thonglo-ktv",
    "eden": "eden-bangkok",
    "jodd": "jodd-fairs-nightlife",
    "walking": "pattaya-walking-street",
    "metro": "bangkok-metro-guide",
    "sim": "thai-sim-guide",
    "scam": "scam-prevention",
    "budget": "budget-guide",
    "windmill": "windmill-pattaya",
    "hourglass": "guest-friendly-hotels",
    "hotel": "guest-friendly-hotels",
    "ladyboy": "ladyboy-bars-guide",
    "yui": "yui-spiral"
}

def get_history():
    try:
        with urllib.request.urlopen(f'http://{SERVER_ADDRESS}/history') as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error fetching history: {e}")
        return None

def download_image(filename, subfolder, type):
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': type})
    url = f'http://{SERVER_ADDRESS}/view?{params}'
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except:
        return None

def sync_latest_high_res():
    history = get_history()
    if not history: return
    
    # Store the best image for each slug
    # We prioritize "Evolution", "Moody", "4K", "Variety" over generic names
    slug_to_best_file = {}
    
    # Process history in order (oldest to newest) to let latest ones win
    for pid in sorted(history.keys(), key=lambda x: int(history[x]['prompt'][0]) if isinstance(history[x]['prompt'][0], int) else 0):
        outputs = history[pid].get('outputs', {})
        for node_id in outputs:
            if 'images' in outputs[node_id]:
                for img in outputs[node_id]['images']:
                    filename = img['filename']
                    if 'ThaiNights' not in filename: continue
                    
                    # Find matching slug
                    match_slug = None
                    for key, slug in MAPPING.items():
                        if key in filename.lower():
                            match_slug = slug
                            break
                    
                    if match_slug:
                        # Priority score based on keywords in filename
                        score = 0
                        if 'ultimate' in filename.lower() or '4k' in filename.lower(): score = 4
                        elif 'moody' in filename.lower(): score = 3
                        elif 'evolution' in filename.lower(): score = 2
                        elif 'varied' in filename.lower() or 'variety' in filename.lower(): score = 1
                        
                        current_best = slug_to_best_file.get(match_slug, {"score": -1})
                        # If this one has higher priority score, or same score but newer (since we iterate forward)
                        if score >= current_best['score']:
                            slug_to_best_file[match_slug] = {
                                "filename": filename,
                                "subfolder": img.get('subfolder', ''),
                                "type": img.get('type', 'output'),
                                "score": score
                            }

    os.makedirs(HERO_DIR, exist_ok=True)
    updated_slugs = []

    for slug, info in slug_to_best_file.items():
        print(f"Syncing best image for {slug}: {info['filename']} (Score: {info['score']})")
        img_data = download_image(info['filename'], info['subfolder'], info['type'])
        if img_data:
            dest_path = os.path.join(HERO_DIR, f"{slug}.png")
            with open(dest_path, 'wb') as f:
                f.write(img_data)
            updated_slugs.append(slug)

    # Update Markdowns
    for lang in ['zh-tw', 'zh-cn', 'en']:
        lang_dir = os.path.join(CONTENT_DIR, lang)
        if not os.path.exists(lang_dir): continue
        for filename in os.listdir(lang_dir):
            if not filename.endswith('.md'): continue
            slug = filename.replace('.md', '')
            if slug in updated_slugs:
                path = os.path.join(lang_dir, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                img_ref = f"../../../assets/hero/{slug}.png"
                if 'heroImage:' in content:
                    content = re.sub(r"heroImage:.*", f"heroImage: '{img_ref}'", content)
                else:
                    content = content.replace("---", f"---\nheroImage: '{img_ref}'", 1)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {path}")

if __name__ == "__main__":
    sync_latest_high_res()
