import os
import re
import json
import urllib.request
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemini-3-flash-preview:cloud"
CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog/zh-tw"

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res['response'].strip()

def fix_translations():
    # Only fix the ones I added in the last batch
    files = [
        "rainbow-4-nana-plaza.md",
        "sapphire-club-soi-15.md",
        "pin-up-agogo-pattaya.md",
        "the-lord-palace-bangkok.md",
        "emmanuelle-soapy-massage.md",
        "the-pimp-gentlemens-club.md",
        "sherbet-ekamai-bangkok.md",
        "eden-club-bangkok.md"
    ]
    
    for file in files:
        path = os.path.join(CONTENT_DIR, file)
        if not os.path.exists(path): continue
        
        print(f"Translating {file} to Traditional Chinese...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already Chinese (simple check)
        if len(re.findall(r'[\u4e00-\u9fff]', content)) > 100:
            print(f"  {file} already looks like Chinese. Skipping.")
            continue
            
        # Split frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3: continue
        header = parts[1]
        body = parts[2]
        
        # Translate Body
        prompt = f"Translate the following erotic review into Traditional Chinese. Maintain the 'Sensual Spiral' style and explicit details. Use terms like '肉浴' and '情色螺旋'. Output ONLY the translated text.\n\n{body}"
        new_body = call_ollama(prompt)
        
        # Translate Title in Header
        title_match = re.search(r'title: "(.*?)"', header)
        if title_match:
            orig_title = title_match.group(1)
            new_title = call_ollama(f"Translate this title to Traditional Chinese: {orig_title}").strip(' "')
            header = header.replace(orig_title, new_title)
            
        # Combine
        new_content = f"---{header}---{new_body}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Successfully translated {file}.")
        time.sleep(1)

if __name__ == "__main__":
    fix_translations()
