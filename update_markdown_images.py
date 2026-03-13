import os
import re

MAPPING = {
    "nana-plaza": "nana-plaza",
    "soi-cowboy": "soi-cowboy",
    "patpong": "patpong",
    "thermae-coffee": "thermae-coffee",
    "soi6-pattaya": "soi6-pattaya",
    "soapy-massage-deep": "soapy-massage-deep",
    "massage-guide": "massage-guide",
    "grab-long-jin": "grab-long-jin",
    "bangkok-bj-bars": "bangkok-bj-bars",
    "gentlemens-clubs": "gentlemens-clubs",
    "thonglo-ktv": "thonglo-ktv",
    "eden-bangkok": "eden-bangkok",
    "jodd-fairs-nightlife": "jodd-fairs-nightlife",
    "pattaya-walking-street": "pattaya-walking-street",
    "lk-metro-pattaya": "lk-metro-pattaya",
    "scam-prevention": "scam-prevention",
    "budget-guide": "budget-guide",
    "pattaya_guide": "pattaya_guide"
}

HERO_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/assets/hero"
CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog"
LANGS = ["zh-tw", "zh-cn", "en"]

def update_all_markdowns():
    available_heroes = [f.replace(".png", "") for f in os.listdir(HERO_DIR) if f.endswith(".png")]
    print(f"Available hero images: {available_heroes}")
    
    for lang in LANGS:
        lang_dir = os.path.join(CONTENT_DIR, lang)
        if not os.path.exists(lang_dir): continue
        
        for filename in os.listdir(lang_dir):
            if not filename.endswith(".md"): continue
            
            slug = filename.replace(".md", "")
            md_path = os.path.join(lang_dir, filename)
            
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if hero image exists for this slug
            if slug in available_heroes:
                image_path = f"../../../assets/hero/{slug}.png"
                
                # Update or Insert heroImage in frontmatter
                if "heroImage:" in content:
                    content = re.sub(r'heroImage:.*', f"heroImage: '{image_path}'", content)
                else:
                    # Insert after title: "..."
                    content = re.sub(r'(title: ".*")', r"\1\nheroImage: '" + image_path + "'", content)
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {md_path}")

if __name__ == "__main__":
    update_all_markdowns()
