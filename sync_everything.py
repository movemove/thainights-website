import os
import subprocess
import re

# Slug mapping for articles
MAPPING = {
    "nana": "nana-plaza",
    "cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae": "thermae-coffee",
    "soi6": "soi6-pattaya",
    "soapy": "soapy-massage-deep",
    "massage": "massage-guide",
    "longjin": "grab-long-jin",
    "bjbar": "bangkok-bj-bars",
    "gentlemen": "gentlemens-clubs",
    "ktv": "thonglo-ktv",
    "eden": "eden-bangkok",
    "jodd": "jodd-fairs-nightlife",
    "walking": "pattaya-walking-street",
    "metro": "lk-metro-pattaya",
    "scam": "scam-prevention",
    "budget": "budget-guide",
    "pattaya_guide": "pattaya_guide"
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
    # Get all images using the query that worked before
    res = run_cmd(["gog", "drive", "ls", "-p", "--limit", "500", "--query", "mimeType = 'image/png' or mimeType = 'image/jpeg' or mimeType = 'video/mp4'"])
    lines = res.stdout.strip().split('\n')
    
    found_any = False
    
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2: continue
        
        file_id = parts[0]
        filename = parts[1]
        
        # Check for ThaiNights prefix
        if not filename.startswith("ThaiNights_"): continue
        
        print(f"Checking file: {filename}")
        found_any = True
        
        # Determine target category
        target_slug = None
        for key, slug in MAPPING.items():
            if key in filename.lower():
                target_slug = slug
                break
        
        if not target_slug:
            # Special categories
            if "high_heels" in filename.lower() or "elitelegs" in filename.lower() or "feet" in filename.lower():
                # These go to gallery
                dest_path = os.path.join(GALLERY_DIR, filename)
                if not os.path.exists(dest_path):
                    print(f"Downloading gallery item: {filename}")
                    run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
            continue

        # Is it a video?
        if filename.endswith(".mp4"):
            dest_path = os.path.join(VIDEO_DIR, f"{target_slug}.mp4")
            if not os.path.exists(dest_path):
                print(f"Downloading video: {filename} -> {target_slug}.mp4")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
                # Generate poster
                poster_path = os.path.join(VIDEO_DIR, f"{target_slug}_poster.jpg")
                subprocess.run(["ffmpeg", "-y", "-i", dest_path, "-ss", "00:00:01", "-vframes", "1", "-f", "image2", poster_path])
        
        # Is it an image?
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            # If it's a hero image (contains 01)
            if "_01" in filename or target_slug not in os.listdir(HERO_DIR):
                dest_path = os.path.join(HERO_DIR, f"{target_slug}.png")
                # Overwrite or fill missing
                print(f"Downloading hero image: {filename} -> {target_slug}.png")
                run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
            else:
                # Extra photos go to gallery
                dest_path = os.path.join(GALLERY_DIR, filename)
                if not os.path.exists(dest_path):
                    print(f"Downloading extra photo: {filename}")
                    run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
    
    if not found_any:
        print("No ThaiNights files found in listing.")

if __name__ == "__main__":
    sync_media()
    print("Sync process finished.")
