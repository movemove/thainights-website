import json
import urllib.request
import os
import random
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"

CATEGORIES = [
    "Nana Plaza", "Soi Cowboy", "Patpong", "Thermae Coffee", "Soi 6 Pattaya",
    "Walking Street Pattaya", "Soapy Massage", "Grab Long Jin", "Gentlemens Clubs",
    "Thong Lo KTV", "Eden Club", "Jodd Fairs"
]

STORY_PROMPT_TEMPLATE = """You are an expert adult content writer for thainights.net. 
Write a highly explicit, 800+ word "Midnight Memoir" story in Traditional Chinese about an intense encounter in {category}.
Style: "Sensual Spiral" - focus on tactile sensations, atmosphere, and detailed physiological responses.
Include specific sex details: oral, intercourse, glans, vagina, nipples, changing positions, and the sound of skin hitting skin.
The story should have a unique female character (name, outfit, personality).
Also provide a short title and a 160-char SEO description.
Output strictly as JSON: {{"title": "...", "description": "...", "content": "..."}}"""

def generate_story(category):
    print(f"Generating story for {category}...")
    payload = {
        "model": MODEL,
        "prompt": STORY_PROMPT_TEMPLATE.format(category=category),
        "stream": False,
        "format": "json"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return json.loads(res['response'])

def translate(text, target_lang):
    prompt = f"Translate the following erotic story into {target_lang}. Maintain the 'Sensual Spiral' style and all explicit details. Output only the translated JSON with the same keys (title, description, content).\n\n{text}"
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "format": "json"}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'))
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return json.loads(res['response'])

def save_story(data, slug):
    langs = {
        "zh-tw": data,
        "zh-cn": translate(json.dumps(data), "Simplified Chinese"),
        "en": translate(json.dumps(data), "English")
    }
    
    # Hero image selection based on category
    hero_map = {
        "nana": "nana-plaza.png", "cowboy": "soi-cowboy.png", "patpong": "patpong.png",
        "thermae": "thermae-coffee.png", "soi6": "soi6-pattaya.png", "walking": "pattaya-walking-street.png",
        "soapy": "soapy-massage-deep.png", "grab": "grab-long-jin.png", "clubs": "gentlemens-clubs.png",
        "ktv": "thonglo-ktv.png", "eden": "eden-bangkok.png", "jodd": "jodd-fairs-nightlife.png"
    }
    hero_file = "soi-cowboy.png" # default
    for k, v in hero_map.items():
        if k in slug: hero_file = v; break

    for code, content in langs.items():
        path = os.path.join(WORKSPACE, f"src/content/stories/{code}/{slug}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Format markdown
        md = f"""---
title: "{content['title']}"
description: "{content['description']}"
pubDate: "2026-03-16"
heroImage: "../../../assets/hero/{hero_file}"
---

{content['content']}
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
    print(f"Successfully saved {slug} in 3 languages.")

if __name__ == "__main__":
    # Generating 6 new stories in this turn to start fulfilling the request
    # Choosing categories that have fewer stories
    target_cats = ["Nana Plaza", "Soapy Massage", "Grab Long Jin", "Gentlemens Clubs", "Thong Lo KTV", "Eden Club"]
    for cat in target_cats:
        try:
            story = generate_story(cat)
            slug = cat.lower().replace(' ', '-').replace("'", "") + f"-{random.randint(100,999)}"
            save_story(story, slug)
        except Exception as e:
            print(f"Error processing {cat}: {e}")
