import json
import urllib.request
import os
import random
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"

# Define topics for reviews to reach 10 per category
TOPICS = [
    # Bangkok Bars
    ("BKK-Bars", "Billboard Nana Plaza", "The world's most famous rotating stage."),
    ("BKK-Bars", "Rainbow 4 Nana Plaza", "High energy, top tier dancers."),
    ("BKK-Bars", "Baccara Soi Cowboy", "The iconic glass floor experience."),
    ("BKK-Bars", "Suzy Wong Soi Cowboy", "Classic red Chinese theme and intimacy."),
    ("BKK-Bars", "King's Castle Patpong", "Where the legend of Patpong continues."),
    ("BKK-Bars", "Shark Nana Plaza", "Wild parties on the top floor."),
    ("BKK-Bars", "Crazy House Soi Cowboy", "Maximum visual impact and energy."),
    
    # Pattaya Nightlife
    ("Pattaya", "Sapphire Club Soi 15", "The premier agogo on Soi 15."),
    ("Pattaya", "Windmill Walking Street", "Pattaya's wildest and most extreme bar."),
    ("Pattaya", "Palace Walking Street", "Top tier visuals and professional dancers."),
    ("Pattaya", "Soi 6 Survival Guide", "Everything you need to know about the narrow alley."),
    ("Pattaya", "LK Metro vs Walking Street", "A comparison of the two main zones."),
    ("Pattaya", "Pin-up Agogo", "Modern, stylish and extremely popular."),
    
    # Massage & SPA
    ("Massage", "Emmanuelle Soapy Massage", "A classic bathhouse experience in Ratchada."),
    ("Massage", "Long Beach Massage", "Great value and professional service."),
    ("Massage", "The Lord Palace", "The peak of luxury bathhouses in Bangkok."),
    ("Massage", "Health Land Kaman", "Best spot for authentic therapy and prostate care."),
    ("Massage", "Prink BJ Bar", "The most famous BJ bar in Sukhumvit."),
    ("Massage", "Black Pagoda", "The dark and artistic gogo-massage fusion.")
]

REVIEW_PROMPT_TEMPLATE = """You are an expert nightlife critic for thainights.net. 
Write a vivid, sensual review in Traditional Chinese for {venue}.
Topic Category: {category}.
Style: "Sensual Spiral" - focused on atmosphere, tactile details, and the "meat bath" feeling.
Provide:
1. A catchy title.
2. A brief 160-char SEO description.
3. Detailed content (400+ words) covering the vibe, interaction with girls (touching, sitting on lap), and price expectations.
Include explicit details but keep it as a professional "review" for old-drivers.
Output strictly as JSON: {{"title": "...", "description": "...", "content": "..."}}"""

def generate_review(category, venue):
    print(f"Generating review for {venue}...")
    payload = {
        "model": MODEL,
        "prompt": REVIEW_PROMPT_TEMPLATE.format(category=category, venue=venue),
        "stream": False,
        "format": "json"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return json.loads(res['response'])

def translate(text, target_lang):
    prompt = f"Translate the following review into {target_lang}. Maintain the 'Sensual Spiral' style and all tactile details. Output only the translated JSON with the same keys.\n\n{text}"
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "format": "json"}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'))
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return json.loads(res['response'])

def save_review(data, slug):
    langs = {
        "zh-tw": data,
        "zh-cn": translate(json.dumps(data), "Simplified Chinese"),
        "en": translate(json.dumps(data), "English")
    }
    
    # Find best hero image
    hero_file = "soi-cowboy.png"
    if "nana" in slug or "billboard" in slug or "rainbow" in slug: hero_file = "nana-plaza.png"
    elif "pattaya" in slug or "windmill" in slug or "walking" in slug: hero_file = "pattaya-walking-street.png"
    elif "massage" in slug or "soapy" in slug: hero_file = "soapy-massage-deep.png"
    elif "bj" in slug or "prink" in slug: hero_file = "bangkok-bj-bars.png"

    for code, content in langs.items():
        path = os.path.join(WORKSPACE, f"src/content/blog/{code}/{slug}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
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
    print(f"Successfully saved review {slug} in 3 languages.")

if __name__ == "__main__":
    # Randomly picking 12 topics from the list to expand the blog sections
    selected_topics = random.sample(TOPICS, 12)
    for cat, venue, desc in selected_topics:
        try:
            review_data = generate_review(cat, venue)
            slug = venue.lower().replace(' ', '-').replace("'", "")
            save_review(review_data, slug)
        except Exception as e:
            print(f"Error processing {venue}: {e}")
