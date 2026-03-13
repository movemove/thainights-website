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
VIDEO_DIR = "/home/alice/.openclaw/workspace/thainights_pages/public/videos"
CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog"

def run_cmd(cmd):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = "1072"
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def get_drive_files(query):
    print(f"Searching Drive with query: {query}")
    res = run_cmd(["gog", "drive", "ls", "--query", query, "--limit", "200"])
    lines = res.stdout.strip().split('\n')
    files = []
    if len(lines) > 1:
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                files.append({"id": parts[0], "name": parts[1]})
    return files

def process_media():
    # Ensure dirs exist
    os.makedirs(HERO_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

    # 1. Process Images
    images = get_drive_files("mimeType contains 'image/' and name contains 'ThaiNights'")
    processed_images = []
    for img in images:
        slug = None
        for key in SLUG_MAP:
            if key in img['name'].lower():
                slug = SLUG_MAP[key]
                break
        
        if slug:
            dest_path = os.path.join(HERO_DIR, f"{slug}.png")
            print(f"Downloading image: {img['name']} -> {slug}.png")
            run_cmd(["gog", "drive", "download", img['id'], "--out", dest_path])
            processed_images.append(slug)

    # 2. Process Videos
    videos = get_drive_files("name contains 'ThaiNights' and name contains '.mp4'")
    # Fallback search for videos
    if not videos:
        videos = get_drive_files("name contains 'Video'")

    processed_videos = []
    for vid in videos:
        slug = None
        for key in SLUG_MAP:
            if key in vid['name'].lower():
                slug = SLUG_MAP[key]
                break
        
        if slug:
            dest_path = os.path.join(VIDEO_DIR, f"{slug}.mp4")
            print(f"Downloading video: {vid['name']} -> {slug}.mp4")
            run_cmd(["gog", "drive", "download", vid['id'], "--out", dest_path])
            
            # Generate poster using ffmpeg
            poster_path = os.path.join(VIDEO_DIR, f"{slug}_poster.jpg")
            subprocess.run(["ffmpeg", "-y", "-i", dest_path, "-ss", "00:00:01", "-vframes", "1", poster_path])
            processed_videos.append(slug)

    return processed_images, processed_videos

def update_posts(image_slugs, video_slugs):
    langs = ["zh-tw", "zh-cn", "en"]
    for slug in set(image_slugs) | set(video_slugs):
        for lang in langs:
            md_path = os.path.join(CONTENT_DIR, lang, f"{slug}.md")
            if not os.path.exists(md_path): continue
            
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False
            # Update Hero Image
            if slug in image_slugs and "heroImage:" not in content:
                content = content.replace("pubDate:", f"heroImage: '../../../assets/hero/{slug}.png'\npubDate:")
                modified = True
            
            # Update Video (Insert a custom HTML tag for now or we can use a component)
            if slug in video_slugs and f"videos/{slug}.mp4" not in content:
                video_html = f'\n\n<video autoplay loop muted playsinline poster="/videos/{slug}_poster.jpg" style="width: 100%; border-radius: 12px; margin: 2rem 0;"><source src="/videos/{slug}.mp4" type="video/mp4"></video>\n\n'
                # Append before the last section or end
                content += video_html
                modified = True
            
            if modified:
                print(f"Updating {md_path}")
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(content)

if __name__ == "__main__":
    imgs, vids = process_media()
    if imgs or vids:
        update_posts(imgs, vids)
        print("Media update complete.")
    else:
        print("No new media to process.")
