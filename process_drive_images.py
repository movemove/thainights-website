import os
import subprocess

# Map of prefix to slug
MAPPING = {
    "nana_plaza": "nana-plaza",
    "soi_cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae": "thermae-coffee",
    "soi6_pattaya": "soi6-pattaya",
    "soapy_massage": "soapy-massage-deep",
    "massage_guide": "massage-guide",
    "grab_long_jin": "grab-long-jin",
    "bj_bars": "bangkok-bj-bars",
    "gentlemens_clubs": "gentlemens-clubs",
    "thonglo_ktv": "thonglo-ktv",
    "eden_club": "eden-bangkok",
    "jodd_fairs": "jodd-fairs-nightlife",
    "walking_street": "pattaya-walking-street",
    "lk_metro": "lk-metro-pattaya",
    "scam_prevention": "scam-prevention",
    "budget_guide": "budget-guide",
    "pattaya_guide": "pattaya_guide"
}

def download_and_process():
    # 1. List files from Drive
    print("Fetching file list from Google Drive...")
    cmd = ["gog", "drive", "ls", "--query", "mimeType = 'image/png' or mimeType = 'image/jpeg'", "--limit", "100"]
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "1072"
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    lines = result.stdout.strip().split('\n')
    if len(lines) < 2:
        print("No images found.")
        return

    # Process all files that contain ThaiNights in filename
    files = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 2 and "ThaiNights" in parts[1]:
            files.append((parts[0], parts[1]))

    processed_slugs = set()
    
    # Create target directory
    os.makedirs("/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero", exist_ok=True)
    
    for file_id, filename in files:
        # Determine which slug this belongs to
        target_slug = None
        for key, slug in MAPPING.items():
            if key in filename.lower():
                target_slug = slug
                break
        
        if not target_slug or target_slug in processed_slugs:
            continue
            
        print(f"Processing {filename} for {target_slug}...")
        
        # 2. Download
        dest = f"/tmp/{filename}"
        subprocess.run(["gog", "drive", "download", file_id, "-o", dest], env=env)
        
        # 3. Convert to WebP and move to assets
        final_path = f"/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero/{target_slug}.webp"
        subprocess.run(["ffmpeg", "-y", "-i", dest, "-q:v", "80", final_path])
        
        processed_slugs.add(target_slug)
        
    return processed_slugs

def update_markdown(slugs):
    base_content_path = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog"
    for lang in ["zh-tw", "zh-cn", "en"]:
        for slug in slugs:
            md_path = os.path.join(base_content_path, lang, f"{slug}.md")
            if os.path.exists(md_path):
                print(f"Updating {md_path} with heroImage...")
                with open(md_path, 'r') as f:
                    lines = f.readlines()
                
                # Check if heroImage already exists
                has_hero = any(line.startswith("heroImage:") for line in lines)
                
                if not has_hero:
                    # Insert after title:
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if line.startswith("title:"):
                            new_lines.append(f"heroImage: '../../../assets/hero/{slug}.webp'\n")
                    
                    with open(md_path, 'w') as f:
                        f.writelines(new_lines)

if __name__ == "__main__":
    slugs = download_and_process()
    if slugs:
        update_markdown(slugs)
        print(f"Successfully updated {len(slugs)} articles with new images.")
