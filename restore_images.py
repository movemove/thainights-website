import os
import re

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content"
ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero"

def restore_images():
    available_images = os.listdir(ASSETS_DIR)
    print(f"Available images: {len(available_images)}")
    
    count = 0
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Uncomment existing but commented out heroImage lines
                new_content = re.sub(r"# heroImage: (['\"].*?['\"])", r"heroImage: \1", content)
                
                # 2. Verify the path
                match = re.search(r"heroImage: (['\"])(.*?)\1", new_content)
                if match:
                    img_path = match.group(2)
                    img_name = os.path.basename(img_path)
                    if img_name not in available_images:
                        print(f"WARNING: {img_name} still missing for {path}")
                    else:
                        if new_content != content:
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            count += 1
                else:
                    # 3. If no heroImage at all, try to find a matching one by slug
                    slug = file.replace(".md", "")
                    target_img = None
                    if f"{slug}.png" in available_images:
                        target_img = f"{slug}.png"
                    elif f"{slug}.jpg" in available_images:
                        target_img = f"{slug}.jpg"
                    
                    if target_img:
                        img_rel = f"../../../assets/hero/{target_img}"
                        new_line = f"heroImage: '{img_rel}'"
                        # Insert after title:
                        new_content = re.sub(r'(title: ".*?")', r'\1\n' + new_line, new_content)
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                        print(f"ADDED heroImage to {path}")

    print(f"Restored/Updated {count} files.")

if __name__ == "__main__":
    restore_images()
