import json
import urllib.request
import os
import random
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"

def call_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res['response'].strip()

def generate_article(category, topic):
    print(f"Creating content for {topic}...")
    
    # 1. Generate Title and Description
    meta_prompt = f"Create a catchy title and a 160-char SEO description in Traditional Chinese for a nightlife review of {topic} in {category}. Output as JSON: {{\"title\": \"...\", \"description\": \"...\"}}"
    meta = json.loads(call_ollama(meta_prompt))
    
    # 2. Generate Content (Separate call to avoid JSON size issues)
    content_prompt = f"""Write a highly explicit, 600+ word review in Traditional Chinese about {topic} in {category}.
    Style: "Sensual Spiral" - focused on atmosphere and tactile sensations (skin touch, soft bodies, etc.).
    Include details about price and venue vibe.
    Do not use markdown headers for the title, just start with the introduction."""
    content = call_ollama(content_prompt)
    
    # 3. Translate
    translations = {}
    for lang_name, lang_code in [("Simplified Chinese", "zh-cn"), ("English", "en")]:
        print(f"  Translating to {lang_name}...")
        trans_prompt = f"Translate the following text into {lang_name}. Maintain the explicit and sensual style.\n\nTitle: {meta['title']}\nDescription: {meta['description']}\n\nContent:\n{content}"
        raw_trans = call_ollama(trans_prompt)
        # Simple split to extract fields
        parts = raw_trans.split('\n\n', 2)
        if len(parts) >= 3:
            translations[lang_code] = {
                "title": parts[0].replace("Title: ", ""),
                "description": parts[1].replace("Description: ", ""),
                "content": parts[2].replace("Content: ", "")
            }
    
    translations["zh-tw"] = {**meta, "content": content}
    return translations

def save_article(langs, slug):
    hero_map = {
        "nana": "nana-plaza.png", "cowboy": "soi-cowboy.png", "patpong": "patpong.png",
        "thermae": "thermae-coffee.png", "soi6": "soi6-pattaya.png", "walking": "pattaya-walking-street.png",
        "soapy": "soapy-massage-deep.png", "grab": "grab-long-jin.png", "clubs": "gentlemens-clubs.png",
        "ktv": "thonglo-ktv.png", "eden": "eden-bangkok.png", "jodd": "jodd-fairs-nightlife.png"
    }
    hero_file = "soi-cowboy.png"
    for k, v in hero_map.items():
        if k in slug: hero_file = v; break

    for code, data in langs.items():
        path = os.path.join(WORKSPACE, f"src/content/blog/{code}/{slug}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        md = f"""---
title: "{data['title']}"
description: "{data['description']}"
pubDate: "2026-03-16"
heroImage: "../../../assets/hero/{hero_file}"
---

{data['content']}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
    print(f"Saved {slug} in all languages.")

if __name__ == "__main__":
    # Generate 4 articles per run to keep it manageable
    batch = [
        ("Bangkok Bars", "Rainbow 4 Nana Plaza"),
        ("Pattaya Nightlife", "Sapphire Club Soi 15"),
        ("Massage & SPA", "Emmanuelle Soapy Massage"),
        ("Premium & Niche", "The Lord Palace Bangkok")
    ]
    for cat, topic in batch:
        try:
            slug = topic.lower().replace(' ', '-').replace("'", "")
            langs = generate_article(cat, topic)
            save_article(langs, slug)
        except Exception as e:
            print(f"Error on {topic}: {e}")
