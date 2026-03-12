import json
import urllib.request
import urllib.parse

def queue_prompt(prompt_text, filename_prefix, server_address="192.168.1.162:8001"):
    # Basic workflow structure for Pony V6
    # Note: Node IDs might vary, but for a simple API call we define a fresh one
    workflow = {
        "3": {
            "inputs": {
                "seed": 123456789, # Will be randomized by ComfyUI if handled via API normally or we can vary it
                "steps": 30,
                "cfg": 7,
                "sampler_name": "dpmpp_2m_sde_gpu",
                "scheduler": "karras",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "ponyDiffusionV6XL_v6StartWithThis.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 1216,
                "height": 832,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": prompt_text,
                "clip": ["11", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "score_4, score_5, score_6, source_pony, (worst quality, low quality:1.4), text, watermark, logo, bad hands, deformed anatomy, blurry, out of focus, distorted face",
                "clip": ["11", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": filename_prefix,
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        },
        "11": {
            "inputs": {
                "stop_at_clip_layer": -2,
                "clip": ["4", 1]
            },
            "class_type": "CLIPSetLastLayer"
        }
    }

    p = {"prompt": workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    try:
        urllib.request.urlopen(req)
        print(f"Successfully queued: {filename_prefix}")
    except Exception as e:
        print(f"Failed to queue {filename_prefix}: {e}")

# The list of 18 categories and their prompts
jobs = [
    ("nana_plaza", "score_9, score_8_up, score_7_up, rating_explicit, (photorealistic:1.2), cinematic wide shot of Nana Plaza Bangkok at night, grand three-story open-air entertainment complex, glowing hot pink and purple neon signs, 1woman, stunning Thai girl in white bikini on balcony, busy street atmosphere, masterpiece"),
    ("soi_cowboy", "score_9, score_8_up, score_7_up, rating_explicit, cinematic street photography of Soi Cowboy Bangkok, thousands of red and pink neon signs, 1woman, sexy Thai girl in white string bikini standing in rain, reflections on asphalt, urban masterpiece"),
    ("patpong", "score_9, score_8_up, score_7_up, rating_explicit, moody photography of Patpong Night Market, glowing Go-Go bar entrances, 1woman, beautiful Thai girl in white bikini sitting at an outdoor bar stool, 1990s vintage film style, rich colors"),
    ("thermae", "score_9, score_8_up, score_7_up, rating_explicit, underground basement bar Thermae Bangkok, dim atmospheric lighting, 1woman, mysterious Thai girl in white silk bikini, seductive gaze, smoke in air, sense of desire, cinematic lighting"),
    ("soi6_pattaya", "score_9, score_8_up, score_7_up, rating_explicit, sunny afternoon in Pattaya Soi 6, narrow alley with colorful bars, 1woman, hot Thai girl in tiny white micro bikini standing in front of bar, tropical heat, vibrant colors"),
    ("soapy_massage", "score_9, score_8_up, score_7_up, rating_explicit, luxury Thai soapy massage hall, huge aquarium stage, 1woman, gorgeous Thai girl in sheer white bikini covered in soap bubbles, warm steam, blue neon highlights, dramatic lighting"),
    ("massage_guide", "score_9, score_8_up, score_7_up, rating_suggestive, traditional Thai massage spa interior, 1woman, gentle Thai masseuse in white silk outfit, warm candle lighting, serene atmosphere, high quality textures"),
    ("grab_long_jin", "score_9, score_8_up, score_7_up, rating_suggestive, mysterious Thai therapy room, 1woman, skilled Thai practitioner in white, sacred atmosphere, dim lighting, spiritual and physical focus, cinematic"),
    ("bj_bars", "score_9, score_8_up, score_7_up, rating_explicit, neon-lit Bangkok BJ bar, high stools, 1woman, seductive Thai girl in white bikini behind a curtain, moody lighting, intense eye contact, cinematic"),
    ("gentlemens_clubs", "score_9, score_8_up, score_7_up, rating_suggestive, ultra-luxurious Bangkok Gentlemen club, 1woman, stunning Thai model in white silk bikini with gold accents, lounging on red velvet sofa, amber lighting, high-end lifestyle"),
    ("thonglo_ktv", "score_9, score_8_up, score_7_up, rating_suggestive, high-end KTV private room in Thong Lo, 1woman, beautiful Thai girl in white cocktail dress-style bikini, holding golden microphone, luxury spirits on table, karaoke lights"),
    ("eden_club", "score_9, score_8_up, score_7_up, rating_explicit, private sensory party at Eden Club Bangkok, 1woman, exotic Thai girl in white lace bikini, mysterious forbidden fruit theme, deep red lighting, seductive atmosphere"),
    ("jodd_fairs", "score_9, score_8_up, score_7_up, rating_suggestive, Jodd Fairs night market outdoor bar, 1woman, casual Thai girl in white bikini top and shorts, drinking cocktail, busy market background, vibrant night life"),
    ("walking_street", "score_9, score_8_up, score_7_up, rating_explicit, Pattaya Walking Street iconic entrance, sea of neon lights, 1woman, energetic Thai girl in white micro bikini dancing, tropical night breeze, chaotic and colorful"),
    ("lk_metro", "score_9, score_8_up, score_7_up, rating_explicit, LK Metro Pattaya L-shaped street, 1woman, gorgeous Thai girl in white bikini leaning against a bar wall, neon glow, intimate atmosphere, masterpiece"),
    ("scam_prevention", "score_9, score_8_up, score_7_up, rating_suggestive, cinematic dark mood, 1woman, Thai girl in white bikini holding a drink, shadow play, mysterious back alley, high contrast, warning sign vibe"),
    ("budget_guide", "score_9, score_8_up, score_7_up, rating_suggestive, 1woman, Thai girl in white bikini holding a fan of Thai Baht cash, neon background, clever spending theme, cinematic lighting"),
    ("pattaya_guide", "score_9, score_8_up, score_7_up, rating_suggestive, wide aerial shot of Pattaya bay at night, vibrant neon coastline, 1woman, Thai girl in white bikini in foreground, beach night breeze, masterpiece")
]

# Execute
for name, prompt in jobs:
    # Queue 3 versions for each
    for i in range(1, 4):
        queue_prompt(prompt, f"ThaiNights_{name}_{i:02d}")
