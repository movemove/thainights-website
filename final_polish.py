import os
import re

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content/blog/zh-tw"

def final_polish():
    for file in os.listdir(CONTENT_DIR):
        if not file.endswith(".md"): continue
        path = os.path.join(CONTENT_DIR, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the title block
        title_match = re.search(r'title: "(.*?)"', content, re.DOTALL)
        if title_match:
            title_val = title_match.group(1)
            if len(title_val) > 150 or "**" in title_val or "Option" in title_val:
                # Find the first quoted Chinese title or pick a reasonable line
                clean_titles = re.findall(r'\*\*《(.*?)》\*\*', title_val)
                if not clean_titles:
                    clean_titles = re.findall(r'\*\*「(.*?)」\*\*', title_val)
                if not clean_titles:
                    # Look for anything between ** and ** that has Chinese
                    clean_titles = [t for t in re.findall(r'\*\*(.*?)\*\*', title_val) if re.search(r'[\u4e00-\u9fff]', t)]
                
                if clean_titles:
                    new_title = clean_titles[0]
                else:
                    # Last resort: take the first non-empty line after "Option 1"
                    lines = title_val.split('\n')
                    new_title = ""
                    for line in lines:
                        if re.search(r'[\u4e00-\u9fff]', line) and "translate" not in line.lower():
                            new_title = line.strip(' ">*')
                            break
                    if not new_title: new_title = title_val.split('\n')[0].strip()

                print(f"Polishing {file}: {new_title}")
                content = content.replace(title_val, new_title)
                
        # Fix description to be clean too
        content = re.sub(r'description: ".*?"', 'description: "泰國夜生活深度實測評測，為您揭開曼谷與芭達雅的神祕面紗。"', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    final_polish()
