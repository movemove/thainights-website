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

def fix_all_translations():
    files = os.listdir(CONTENT_DIR)
    for file in files:
        if not file.endswith(".md"): continue
        path = os.path.join(CONTENT_DIR, file)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Heuristic: If there are many English words and few Chinese characters, it needs translation
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]{3,}', content))
        
        if english_words > 50 and chinese_chars < 100:
            print(f"Translating {file}...")
            
            # Split frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3: continue
            
            header = parts[1]
            body = parts[2]
            
            # Translate Title in Header
            title_match = re.search(r'title: "(.*?)"', header)
            if title_match:
                orig_title = title_match.group(1)
                new_title = call_ollama(f"Translate this title to Traditional Chinese: {orig_title}").strip(' "')
                header = header.replace(orig_title, new_title)
            
            # Translate Body
            trans_prompt = f"Translate the following erotic review into Traditional Chinese. Maintain the explicit and sensual 'Sensual Spiral' style. Use terms like '肉浴' and '情色螺旋'. Output ONLY the translated text.\n\n{body}"
            new_body = call_ollama(trans_prompt)
            
            # Combine
            new_content = f"---{header}---{new_body}"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Done fixing {file}.")
            time.sleep(1) # Breath for API

if __name__ == "__main__":
    fix_all_translations()
