import os
import re

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content"
ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero"

def fix_missing_images():
    available_images = os.listdir(ASSETS_DIR)
    print(f"Available images: {len(available_images)}")
    
    count = 0
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find heroImage: '...'
                match = re.search(r"heroImage: ['\"](.*?)['\"]", content)
                if match:
                    img_path = match.group(1)
                    img_name = os.path.basename(img_path)
                    
                    if img_name not in available_images:
                        # Image is missing! Comment it out to prevent build failure
                        print(f"MISSING: {img_name} in {path}. Removing reference.")
                        content = re.sub(r"(heroImage:.*)", r"# \1", content)
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
    print(f"Fixed {count} files with missing images.")

if __name__ == "__main__":
    fix_missing_images()
