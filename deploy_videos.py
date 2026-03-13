import os
import subprocess
import re

# Mapping of file keywords to blog slugs
SLUG_MAP = {
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

# Special mapping for Feet videos to specific articles
FEET_MAP = {
    "massage_sole": "massage-guide",
    "soapy_toes": "soapy-massage-deep",
    "relaxing_feet": "thermae-coffee",
    "beach_barefoot": "pattaya-walking-street"
}

VIDEO_DIR = "/home/alice/.openclaw/workspace/thainights_pages/public/videos"
CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog"

def run_cmd(cmd):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "1072"
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def sync_videos():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    print("Fetching video list from Google Drive...")
    res = run_cmd(["gog", "drive", "ls", "-p", "--limit", "1000", "--query", "mimeType = 'video/mp4'"])
    lines = res.stdout.strip().split('\n')
    
    video_assignments = {} # {slug: [video_paths]}

    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) < 2: continue
        file_id, filename = parts[0], parts[1]
        
        if not filename.startswith("ThaiNights_"): continue
        
        target_slug = None
        # Handle regular video jobs
        for key, slug in SLUG_MAP.items():
            if f"Video_{key}" in filename or f"Fast_{key}" in filename:
                target_slug = slug
                break
        
        # Handle Feet videos
        if not target_slug:
            for key, slug in FEET_MAP.items():
                if key in filename.lower():
                    target_slug = slug
                    break
        
        if target_slug:
            dest_name = filename.replace(".mp4", "").replace("ThaiNights_", "").lower() + ".mp4"
            dest_path = os.path.join(VIDEO_DIR, dest_name)
            
            print(f"Downloading: {filename} -> {dest_name}")
            run_cmd(["gog", "drive", "download", file_id, "--out", dest_path])
            
            # Generate poster
            poster_name = dest_name.replace(".mp4", "_poster.jpg")
            poster_path = os.path.join(VIDEO_DIR, poster_name)
            subprocess.run(["ffmpeg", "-y", "-i", dest_path, "-ss", "00:00:01", "-vframes", "1", "-f", "image2", poster_path])
            
            if target_slug not in video_assignments:
                video_assignments[target_slug] = []
            video_assignments[target_slug].append(dest_name)
            
    return video_assignments

def update_markdown(assignments):
    langs = ["zh-tw", "zh-cn", "en"]
    for slug, vids in assignments.items():
        for lang in langs:
            md_path = os.path.join(CONTENT_DIR, lang, f"{slug}.md")
            if not os.path.exists(md_path): continue
            
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            for vid in vids:
                if vid in content: continue
                poster = vid.replace(".mp4", "_poster.jpg")
                video_html = f'\n\n<video autoplay loop muted playsinline poster="/videos/{poster}" style="width: 100%; border-radius: 12px; margin: 2rem 0;"><source src="/videos/{vid}" type="video/mp4"></video>\n\n'
                
                # Try to insert before discussions or at end
                if "### 💬" in new_content:
                    parts = new_content.split("### 💬", 1)
                    new_content = parts[0] + video_html + "### 💬" + parts[1]
                else:
                    new_content += video_html
            
            if new_content != content:
                print(f"Updating {md_path}")
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    assignments = sync_videos()
    if assignments:
        update_markdown(assignments)
        print("Video deployment finished.")
    else:
        print("No new videos found to deploy.")
