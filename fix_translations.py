import json
import urllib.request
import os
import random
import datetime
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
WORKSPACE = "/home/alice/.openclaw/workspace/thainights_pages"

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res['response'].strip()

def translate_and_fix():
    content_dir = os.path.join(WORKSPACE, "src/content/blog/zh-tw")
    # Files added in the large batch
    files_to_fix = [
        "billboard-nana-plaza.md",
        "rainbow-4-nana-plaza.md",
        "sapphire-club-soi-15.md",
        "pin-up-agogo-pattaya.md",
        "the-lord-palace-bangkok.md",
        "emmanuelle-soapy-massage.md",
        "prink-bj-bar-sukhumvit.md",
        "the-pimp-gentlemens-club.md",
        "sherbet-ekamai-bangkok.md",
        "eden-club-bangkok.md"
    ]
    
    for filename in files_to_fix:
        path = os.path.join(content_dir, filename)
        if not os.path.exists(path): continue
        
        print(f"Fixing {filename}...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's already translated (simple check for Chinese characters)
        if re.search(r'[\u4e00-\u9fff]', content):
            print(f"  Skipping {filename}, already contains Chinese.")
            continue
            
        # Translate to Traditional Chinese
        trans_prompt = f"Translate the following blog post content into Traditional Chinese. Maintain the explicit and sensual 'Sensual Spiral' style. Output ONLY the translated content, no markdown title.\n\n{content}"
        translated_body = call_ollama(trans_prompt)
        
        # Preserve original frontmatter
        header_match = re.search(r'^---.*?---', content, re.DOTALL)
        if header_match:
            header = header_match.group(0)
            # Translate title in header
            title_match = re.search(r'title: "(.*?)"', header)
            if title_match:
                orig_title = title_match.group(1)
                title_trans = call_ollama(f"Translate this title to Traditional Chinese: {orig_title}")
                header = header.replace(orig_title, title_trans.strip('"'))
            
            # Combine
            new_content = header + "\n\n" + translated_body
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Successfully fixed {filename}.")

if __name__ == "__main__":
    translate_and_fix()
