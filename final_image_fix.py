import os
import re

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content"
ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero"

def final_fix():
    available = os.listdir(ASSETS_DIR)
    
    # 1. Map Yui to soi-cowboy.png
    # 2. Map Mei to soi-cowboy-mei.png
    # 3. Ensure all other articles have their heroImage uncommented and path corrected
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                # Special cases
                if "yui-spiral" in file:
                    new_content = re.sub(r"heroImage:.*", "heroImage: '../../../assets/hero/soi-cowboy.png'", new_content)
                elif "soi-cowboy-mei" in file:
                    new_content = re.sub(r"heroImage:.*", "heroImage: '../../../assets/hero/soi-cowboy-mei.png'", new_content)
                else:
                    # General uncommenting
                    new_content = re.sub(r"# heroImage: (['\"].*?['\"])", r"heroImage: \1", new_content)
                
                # Verify and fix broken links
                match = re.search(r"heroImage: (['\"])(.*?)\1", new_content)
                if match:
                    img_path = match.group(2)
                    img_name = os.path.basename(img_path)
                    
                    if img_name not in available:
                        # Try fallback to slug.png
                        slug = file.replace(".md", "")
                        if f"{slug}.png" in available:
                            new_content = re.sub(r"heroImage:.*", f"heroImage: '../../../assets/hero/{slug}.png'", new_content)
                        elif f"{slug}.jpg" in available:
                            new_content = re.sub(r"heroImage:.*", f"heroImage: '../../../assets/hero/{slug}.jpg'", new_content)
                        else:
                            # Still missing? Comment it out to prevent build failure
                            print(f"STILL MISSING: {img_name} for {path}")
                            new_content = re.sub(r"(heroImage:.*)", r"# \1", new_content)

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"FIXED: {path}")

if __name__ == "__main__":
    final_fix()
