import json
import urllib.request
import urllib.parse
import os
import random
import time

SERVER_ADDRESS = "192.168.1.162:8188"
IMAGE_FILENAME = "IG/ThaiNights_4K_00002_.png"

# Video Workflow Template (Wan 2.2)
WF_VIDEO = {
 "97": { "inputs": { "image": "" }, "class_type": "LoadImage" },
 "108": { "inputs": { "filename_prefix": "video/IG_Wan2.2_Final", "format": "auto", "codec": "auto", "video-preview": "", "video": ["129:94", 0] }, "class_type": "SaveVideo" },
 "129:98": { "inputs": { "width": 640, "height": 1152, "length": 169, "batch_size": 1, "positive": ["129:93", 0], "negative": ["129:89", 0], "vae": ["129:90", 0], "start_image": ["97", 0] }, "class_type": "WanImageToVideo" },
 "129:94": { "inputs": { "fps": 16, "images": ["129:87", 0] }, "class_type": "CreateVideo" },
 "129:104": { "inputs": { "shift": 5.0, "model": ["129:116", 0] }, "class_type": "ModelSamplingSD3" },
 "129:102": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "strength_model": 1.0, "model": ["129:96", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:124": { "inputs": { "value": 2 }, "class_type": "PrimitiveInt" },
 "129:85": { "inputs": { "add_noise": "disable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": ["129:125", 0], "end_at_step": ["129:119", 0], "return_with_leftover_noise": "disable", "model": ["129:103", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:86", 0] }, "class_type": "KSamplerAdvanced" },
 "129:118": { "inputs": { "value": 4 }, "class_type": "PrimitiveInt" },
 "129:86": { "inputs": { "add_noise": "enable", "noise_seed": 0, "steps": ["129:119", 0], "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "start_at_step": 0, "end_at_step": ["129:125", 0], "return_with_leftover_noise": "enable", "model": ["129:104", 0], "positive": ["129:98", 0], "negative": ["129:98", 1], "latent_image": ["129:98", 2] }, "class_type": "KSamplerAdvanced" },
 "129:89": { "inputs": { "text": "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:128": { "inputs": { "value": 20 }, "class_type": "PrimitiveInt" },
 "129:87": { "inputs": { "samples": ["129:85", 0], "vae": ["129:90", 0] }, "class_type": "VAEDecode" },
 "129:93": { "inputs": { "text": "A cinematic high-quality video of the woman in the image. She slowly and sensually moves in the nightclub. Perfectly smooth skin, realistic motion, 4k.", "clip": ["129:84", 0] }, "class_type": "CLIPTextEncode" },
 "129:131": { "inputs": { "value": True }, "class_type": "PrimitiveBoolean" },
 "129:90": { "inputs": { "vae_name": "wan_2.1_vae.safetensors" }, "class_type": "VAELoader" },
 "129:84": { "inputs": { "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default" }, "class_type": "CLIPLoader" },
 "129:96": { "inputs": { "unet_name": "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:95": { "inputs": { "unet_name": "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "weight_dtype": "default" }, "class_type": "UNETLoader" },
 "129:103": { "inputs": { "shift": 5.0, "model": ["129:117", 0] }, "class_type": "ModelSamplingSD3" },
 "129:127": { "inputs": { "value": 10 }, "class_type": "PrimitiveInt" },
 "129:101": { "inputs": { "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "strength_model": 1.0, "model": ["129:95", 0] }, "class_type": "LoraLoaderModelOnly" },
 "129:126": { "inputs": { "value": 3.5 }, "class_type": "PrimitiveFloat" },
 "129:116": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:95", 0], "on_true": ["129:101", 0] }, "class_type": "ComfySwitchNode" },
 "129:117": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:96", 0], "on_true": ["129:102", 0] }, "class_type": "ComfySwitchNode" },
 "129:119": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:128", 0], "on_true": ["129:118", 0] }, "class_type": "ComfySwitchNode" },
 "129:120": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:126", 0], "on_true": ["129:122", 0] }, "class_type": "ComfySwitchNode" },
 "129:125": { "inputs": { "switch": ["129:131", 0], "on_false": ["129:127", 0], "on_true": ["129:124", 0] }, "class_type": "ComfySwitchNode" },
 "129:122": { "inputs": { "value": 1.0 }, "class_type": "PrimitiveFloat" }
}

def upload_image(full_path):
    print(f"🔄 Transferring {full_path} to input folder...")
    filename = os.path.basename(full_path)
    subfolder = os.path.dirname(full_path)
    
    params = urllib.parse.urlencode({'filename': filename, 'subfolder': subfolder, 'type': 'output'})
    view_url = f"http://{SERVER_ADDRESS}/view?{params}"
    upload_url = f"http://{SERVER_ADDRESS}/upload/image"
    try:
        with urllib.request.urlopen(view_url) as response:
            img_data = response.read()
        boundary = '----WebKitFormBoundary' + str(int(time.time()))
        data = [f'--{boundary}', f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(filename)}"', 'Content-Type: image/png', '', img_data, f'--{boundary}--']
        # Join bytes
        body = b'\r\n'.join([x.encode() if isinstance(x, str) else x for x in data])
        req = urllib.request.Request(upload_url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())['name']
    except Exception as e:
        print(f"Error transferring: {e}")
        return os.path.basename(filename)

def run():
    # 1. Upload
    final_fn = upload_image(IMAGE_FILENAME)
    
    # 2. Queue Video
    WF_VIDEO["97"]["inputs"]["image"] = final_fn
    seed = random.randint(1, 10**14)
    WF_VIDEO["129:86"]["inputs"]["noise_seed"] = seed
    WF_VIDEO["129:85"]["inputs"]["noise_seed"] = seed
    
    p = {"prompt": WF_VIDEO}
    data = json.dumps(p).replace('True', 'true').replace('False', 'false').encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print(f"🚀 Video successfully queued! ID: {res['prompt_id']}")
    except Exception as e:
        print(f"Error queuing video: {e}")

if __name__ == "__main__":
    run()
