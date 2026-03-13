import os
import subprocess
import json
import random

# Mapping of file keywords to blog slugs
SLUG_MAP = {
    "nana": "nana-plaza",
    "cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae": "thermae-coffee",
    "soi6": "soi6-pattaya",
    "soapy": "soapy-massage-deep",
    "massage": "massage-guide",
    "longjin": "grab-long-jin",
    "grab": "grab-long-jin",
    "bj": "bangkok-bj-bars",
    "gentlemen": "gentlemens-clubs",
    "ktv": "thonglo-ktv",
    "eden": "eden-bangkok",
    "jodd": "jodd-fairs-nightlife",
    "walking": "pattaya-walking-street",
    "ws": "pattaya-walking-street",
    "metro": "lk-metro-pattaya",
    "scam": "scam-prevention",
    "budget": "budget-guide",
    "windmill": "windmill-pattaya"
}

ASSETS_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets"
HERO_DIR = os.path.join(ASSETS_DIR, "hero")
GALLERY_DIR = os.path.join(ASSETS_DIR, "gallery")
VIDEO_DIR = "/home/alice/.openclaw/workspace/thainights_pages/public/videos"

os.makedirs(HERO_DIR, exist_ok=True)
os.makedirs(GALLERY_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def run_cmd(cmd):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "1072"
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def sync_media():
    print("Listing files on Drive...")
    res = run_cmd(["gog", "drive", "ls", "-p", "--limit", "1000", "--query", "mimeType = 'image/png' or mimeType = 'image/jpeg' or mimeType = 'video/mp4'"])
    lines = res.stdout.strip().split('\n')
    
    found_any = False
    downloaded_hero_slugs = set()

    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2: continue
        
        file_id = parts[0]
        filename = parts[1]
        
        if not filename.startswith("ThaiNights_"): continue
        found_any = True
        
        # Determine target category
        target_slug = None
        for key, slug in SLUG_MAP.items():
            if key in filename.lower():
                target_slug = slug
                break
        
        # Handle Gallery items
        if "high_heels" in filename.lower() or "elitelegs" in filename.lower() or "feetdetail" in filename.lower():
            dest_path = os.path.join(GALLERY_DIR, filename)
            if not os.path.exists(dest_path):
                print(f"Downloading gallery item: {filename}")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
            continue

        if not target_slug:
            continue

        # Handle Videos
        if filename.endswith(".mp4"):
            dest_path = os.path.join(VIDEO_DIR, f"{target_slug}.mp4")
            if not os.path.exists(dest_path):
                print(f"Downloading video: {filename} -> {target_slug}.mp4")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
                poster_path = os.path.join(VIDEO_DIR, f"{target_slug}_poster.jpg")
                subprocess.run(["ffmpeg", "-y", "-i", dest_path, "-ss", "00:00:01", "-vframes", "1", "-f", "image2", poster_path])
        
        # Handle Hero Images
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            # If it's a primary hero (01) or we haven't got one yet
            is_primary = "_01" in filename or "_01" not in filename # fallback
            
            if target_slug not in downloaded_hero_slugs:
                dest_path = os.path.join(HERO_DIR, f"{target_slug}.png")
                print(f"Downloading hero image: {filename} -> {target_slug}.png")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
                downloaded_hero_slugs.add(target_slug)
            else:
                # Extra photos go to gallery
                dest_path = os.path.join(GALLERY_DIR, filename)
                if not os.path.exists(dest_path):
                    print(f"Downloading extra photo to gallery: {filename}")
                    run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
    
    if not found_any:
        print("No ThaiNights files found in listing.")

if __name__ == "__main__":
    sync_media()
    print("Sync process finished.")
