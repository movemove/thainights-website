import os
import subprocess
import re

# Precise Mapping based on your Google Drive filenames
DRIVE_MAPPING = {
    "nana_plaza": "nana-plaza",
    "soi_cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae": "thermae-coffee",
    "soi6_pattaya": "soi6-pattaya",
    "soapy_massage": "soapy-massage-deep",
    "massage_guide": "massage-guide",
    "grab_long_jin": "grab-long-jin",
    "bangkok-bj-bars": "bangkok-bj-bars",
    "gentlemens_clubs": "gentlemens-clubs",
    "thonglo_ktv": "thonglo-ktv",
    "eden_club": "eden-bangkok",
    "jodd_fairs": "jodd-fairs-nightlife",
    "walking_street": "pattaya-walking-street",
    "lk_metro": "lk-metro-pattaya",
    "scam_prevention": "scam-prevention",
    "budget_guide": "budget-guide",
    "pattaya_ws": "pattaya-walking-street"
}

ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets"
HERO_DIR = os.path.join(ASSETS_DIR, "hero")
CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog"

def run_cmd(cmd):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "1072"
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def force_sync():
    os.makedirs(HERO_DIR, exist_ok=True)
    print("Force scanning Drive for all images...")
    res = run_cmd(["gog", "drive", "ls", "-p", "--limit", "500", "--query", "mimeType = 'image/png' or mimeType = 'image/jpeg'"])
    lines = res.stdout.strip().split('\n')
    
    downloaded_count = 0
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2: continue
        file_id, filename = parts[0], parts[1]
        
        if not filename.startswith("ThaiNights_"): continue
        
        # Match filename to slug
        target_slug = None
        for key, slug in DRIVE_MAPPING.items():
            if key in filename.lower():
                target_slug = slug
                break
        
        if target_slug:
            dest = os.path.join(HERO_DIR, f"{target_slug}.png")
            # Force download if it's a priority variety image
            is_priority = "FaceVar" in filename or "Curvy" in filename or "Hourglass" in filename
            
            if not os.path.exists(dest) or is_priority:
                print(f"Applying {filename} as hero for {target_slug}")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest])
                downloaded_count += 1

    # Update Markdowns
    available = [f.replace(".png", "") for f in os.listdir(HERO_DIR) if f.endswith(".png")]
    for lang in ["zh-tw", "zh-cn", "en"]:
        for slug in available:
            md_path = os.path.join(CONTENT_DIR, lang, f"{slug}.md")
            if os.path.exists(md_path):
                print(f"Ensuring {md_path} links to {slug}.png")
                with open(md_path, 'r') as f: content = f.read()
                img_path = f"../../../assets/hero/{slug}.png"
                if "heroImage:" in content:
                    content = re.sub(r"heroImage:.*", f"heroImage: '{img_path}'", content)
                else:
                    # Insert at the top of frontmatter
                    content = content.replace("---", f"---\nheroImage: '{img_path}'", 1)
                with open(md_path, 'w') as f: f.write(content)

if __name__ == "__main__":
    force_sync()
