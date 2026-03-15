import os
import re

# Precise Mapping for missing or broken images
FIX_MAPPING = {
    "obsession-nana": "ladyboy-bars-guide.png",
    "bj-alley-soi7": "bangkok-bj-bars.png",
    "currency-exchange": "budget-guide.png",
    "yui-spiral": "soi-cowboy.png",
    "thermae-mina": "thermae-coffee.png",
    "soi6-adventure": "soi6-pattaya.png",
    "soi-cowboy-mei": "soi-cowboy.png",
    "yui-spiral": "soi-cowboy.png"
}

CONTENT_DIRS = [
    "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog",
    "/home/alice/.openclaw/workspace/thainights_pages/src/content/stories"
]

HERO_ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero"
LANGS = ["zh-tw", "zh-cn", "en"]

def update_posts():
    available_images = os.listdir(HERO_ASSETS_DIR)
    
    for base_dir in CONTENT_DIRS:
        for lang in LANGS:
            lang_dir = os.path.join(base_dir, lang)
            if not os.path.exists(lang_dir): continue
            
            for filename in os.listdir(lang_dir):
                if not filename.endswith(".md"): continue
                
                slug = filename.replace(".md", "")
                path = os.path.join(lang_dir, filename)
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for existing heroImage
                match = re.search(r"heroImage: ['\"](.*)['\"]", content)
                has_valid_image = False
                
                if match:
                    img_rel_path = match.group(1)
                    img_name = os.path.basename(img_rel_path)
                    if img_name in available_images:
                        has_valid_image = True
                    else:
                        print(f"[BROKEN LINK] {path} references {img_name} which is missing.")
                
                if not has_valid_image:
                    # Determine best replacement
                    target_image = FIX_MAPPING.get(slug)
                    
                    # Fallback to slug.png if exists
                    if not target_image and f"{slug}.png" in available_images:
                        target_image = f"{slug}.png"
                    
                    # Fallback to slug.jpg if exists
                    if not target_image and f"{slug}.jpg" in available_images:
                        target_image = f"{slug}.jpg"

                    if target_image:
                        img_path = f"../../../assets/hero/{target_image}"
                        if "heroImage:" in content:
                            content = re.sub(r"heroImage:.*", f"heroImage: '{img_path}'", content)
                        else:
                            content = content.replace("---", f"---\nheroImage: '{img_path}'", 1)
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"[FIXED] Assigned {target_image} to {path}")
                    else:
                        print(f"[STILL MISSING] No suitable image found for {path}")

if __name__ == "__main__":
    update_posts()
