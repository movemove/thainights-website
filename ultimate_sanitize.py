import os
import re
import yaml

CONTENT_DIR = "/home/alice/.openclaw/workspace/thainights_pages/src/content"

def sanitize_frontmatter():
    count = 0
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parts = content.split('---', 2)
                if len(parts) < 3: continue
                
                raw_header = parts[1]
                body = parts[2]
                
                # Manual repair of common LLM artifacts in header
                lines = raw_header.split('\n')
                clean_lines = []
                for line in lines:
                    if not line.strip(): continue
                    if line.startswith("title:"):
                        # Get the part after the first colon
                        val = line.split(':', 1)[1].strip()
                        # Remove anything after the first logical end of string
                        # e.g., "Real Title" followed by "Explanation"
                        # We look for the content between the first and last quotes on THIS line
                        inner_match = re.search(r'["\'](.*?)["\']', val)
                        if inner_match:
                            clean_val = inner_match.group(1).replace('"', '').replace("'", "")
                        else:
                            clean_val = val.replace('"', '').replace("'", "")
                        clean_lines.append(f'title: "{clean_val}"')
                    elif line.startswith("description:"):
                        val = line.split(':', 1)[1].strip()
                        inner_match = re.search(r'["\'](.*?)["\']', val)
                        if inner_match:
                            clean_val = inner_match.group(1).replace('"', '').replace("'", "")
                        else:
                            clean_val = val.replace('"', '').replace("'", "")
                        clean_lines.append(f'description: "{clean_val}"')
                    elif any(line.strip().startswith(k) for k in ["pubDate:", "heroImage:", "# heroImage:", "updatedDate:"]):
                        clean_lines.append(line.strip())
                
                new_header = "\n".join(clean_lines)
                
                # Final validation
                try:
                    yaml.safe_load(new_header)
                except:
                    # If still broken, just force a basic title
                    slug = os.path.basename(path).replace(".md", "")
                    new_header = f'title: "{slug}"\ndescription: "Thailand nightlife guide"\npubDate: "2026-03-12"'
                new_content = f"--- \n{new_header}\n---{body}"
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
    print(f"Sanitized {count} files.")

if __name__ == "__main__":
    sanitize_frontmatter()
