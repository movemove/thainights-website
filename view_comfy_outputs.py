import json
import urllib.request

SERVER_ADDRESS = "192.168.1.162:8188"

def get_history():
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history") as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error fetching history: {e}")
        return None

def fetch_image(filename, subfolder, type):
    url_values = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": type})
    url = f"http://{SERVER_ADDRESS}/view?{url_values}"
    try:
        # We can't easily display it here, but we can verify accessibility
        with urllib.request.urlopen(url) as response:
            return True
    except:
        return False

if __name__ == "__main__":
    history = get_history()
    if history:
        print(f"Total history entries: {len(history)}")
        # Look at the most recent entry
        latest_id = list(history.keys())[-1]
        outputs = history[latest_id].get('outputs', {})
        for node_id in outputs:
            if 'images' in outputs[node_id]:
                for img in outputs[node_id]['images']:
                    print(f"Found Image: {img['filename']} (Node: {node_id})")
                    # In a real tool use, I could download this to /tmp
    else:
        print("Could not connect to ComfyUI or history is empty.")
