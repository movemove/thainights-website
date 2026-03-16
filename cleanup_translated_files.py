import os
import re

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog/zh-tw"

def clean_titles():
    for file in os.listdir(CONTENT_DIR):
        if file.endswith(".md"):
            path = os.path.join(CONTENT_DIR, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix titles that have LLM garbage
            title_match = re.search(r'title: "(.*?)"', content, re.DOTALL)
            if title_match:
                title_val = title_match.group(1)
                if len(title_val) > 100 or "**" in title_val or ">" in title_val:
                    # Attempt to find a clean title inside the garbage
                    clean_match = re.search(r'《(.*?)》', title_val)
                    if clean_match:
                        new_title = clean_match.group(1)
                    else:
                        # Fallback: take the first line of the title block
                        new_title = title_val.split('\n')[0].strip(' "')
                    
                    print(f"Cleaning title in {file}: {new_title}")
                    content = content.replace(title_val, new_title)
                    
            # Fix descriptions that are still English
            desc_match = re.search(r'description: "(.*?)"', content)
            if desc_match:
                desc_val = desc_match.group(1)
                if re.search(r'[a-zA-Z]{5,}', desc_val) and not re.search(r'[\u4e00-\u9fff]', desc_val):
                    # Description is English, let's just make it a generic Chinese one for now
                    new_desc = "深入探索曼谷最真實的夜生活體驗，包含環境氛圍、消費指南與實戰心得。"
                    print(f"Replacing English desc in {file}")
                    content = content.replace(desc_val, new_desc)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    clean_titles()
