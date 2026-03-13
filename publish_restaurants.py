import os

# New Restaurant Articles for the "Sensual Spiral" series
restaurant_articles = {
    "sky-bar-luxury.md": {
        "zh-tw": {
            "title": "雲端之吻：曼谷高空餐廳，晚風與香檳的感官纏繞",
            "desc": "在曼谷之巔，讓城市的霓虹成為你的桌布，感受極致的高空浪漫。",
            "content": """位於 60 層樓高空的 Sky Bar，空氣中帶著一絲微涼的晚風。當你坐在露台邊緣，整座曼谷的燈火如同被打碎的鑽石，在你的腳下閃爍。

### 🍹 晚風與酒精的化學反應
在這裡，感官被無限拉長。當侍者為你斟上冰鎮的香檳，杯壁的冷凝水珠滑過你的指尖。你對面的女孩穿著露背的絲綢長裙，背部曲線在月光下顯得如象牙般潔白細膩。當你們低聲交談，晚風會帶著她髮間的淡香輕拂你的臉龐。那種微醺的熱度與高空的涼意相互碰撞，就是最頂級的感官螺旋。

### 🍽️ 舌尖上的曼谷
這裡的料理不僅是食物，更是藝術。每一口帶有層次的酸、甜、辣，都在試圖挑逗你的味蕾邊界。這裡適合那些追求極致儀式感的玩家，在星空下進行一場靈魂與胃袋的雙重朝聖。🐾"""
        },
        "zh-cn": {
            "title": "云端之吻：曼谷高空餐厅，晚风与香槟的感官缠绕",
            "desc": "在曼谷之巅，让城市的霓虹成为你的桌布，感受极致的高空浪漫。",
            "content": """位于 60 层楼高空的 Sky Bar，空气中带着一丝微涼的晚风。当你坐在露台边缘，整个曼谷的灯火如同被打碎的钻石，在你的脚下闪烁。

### 🍹 晚风与酒精的化学反应
在这里，感官被无限拉长。当侍者为你斟上冰镇的香槟，杯壁的冷凝水珠滑过你的指尖。你对面的女孩穿着露背的丝绸长裙，背部曲线在月光下显得如象牙般洁白细腻。当你们低声交谈，晚风会带着她髮间的淡香轻拂你的脸庞。那种微醺的热度与高空的凉意相互碰撞，就是最顶级的感官螺旋。

### 🍽️ 舌尖上的曼谷
这里的料理不仅是食物，更是艺术。每一口带有层次的酸、甜、辣，都在试图挑逗你的味蕾边界。这里适合那些追求极致仪式感的玩家，在星空下进行一场灵魂与胃袋的双重朝圣。🐾"""
        },
        "en": {
            "title": "Kiss the Clouds: Bangkok Sky Dining – A Sensory Spin of Breeze and Bubbles",
            "desc": "At the peak of Bangkok, let the city neons be your tablecloth and feel the ultimate high-altitude romance.",
            "content": """Located 60 floors above the city, the air at the Sky Bar carries a cool midnight breeze. As you sit at the terrace edge, the lights of Bangkok sparkle below like shattered diamonds.

### 🍹 The Chemistry of Wind and Alcohol
Here, the senses are stretched to the limit. As the server pours chilled champagne, the condensation on the glass slides over your fingertips. The woman across from you, in a backless silk gown, has skin that glows like polished ivory under the moonlight. As you whisper, the breeze carries the scent of her hair against your face. That intoxicating mix of alcohol-induced warmth and high-altitude chill is the definitive sensual spiral.

### 🍽️ Bangkok on the Tongue
The cuisine here is more than food—it's art. Every layered burst of sour, sweet, and spicy tests the boundaries of your palate. This is for the adventurer seeking ritual and prestige, a dual pilgrimage of the soul and the stomach under the stars.🐾"""
        }
    },
    "riverside-dining.md": {
        "zh-tw": {
            "title": "河畔夜色：昭披耶河畔，辛辣與水波的感官對話",
            "desc": "水氣氤氳中，讓泰式香料的熱力喚醒你最深層的食慾。",
            "content": """昭披耶河的深夜，有一種沉靜卻誘人的張力。河畔餐廳的燈火映在起伏的水面上，像是無數條流動的金蛇。

### 🥘 辛辣的熱力螺旋
當一碗正宗的冬陰功湯（Tom Yum Goong）端上桌，那種帶著香茅與南薑的熱氣撲面而來。辛辣的香料在舌尖跳舞，讓你的體溫微微升高。坐在對面的女孩，因為這份熱力，臉頰泛起了一層淡淡的紅暈，眼神也變得迷離起來。在水波盪漾的背景下，這種「餐桌上的曖昧」比酒精更讓人沉醉。

### 💆 觸覺的延續
飯後，手牽手沿著河岸散步，濕潤的空氣包裹著肌膚。在這裡，每一道菜都是一次前戲，引導你進入泰國深夜更深層的螺旋中。🐾"""
        },
        "zh-cn": {
            "title": "河畔夜色：昭披耶河畔，辛辣与水波的感官对话",
            "desc": "水气氤氲中，让泰式香料的热力唤醒你最深层的食欲。",
            "content": """昭披耶河的深夜，有一种沉静却诱人的张力。河畔餐厅的灯火映在起伏的水面上，像是无数条流动的金蛇。

### 🥘 辛辣的热力螺旋
当一碗正宗的冬阴功汤（Tom Yum Goong）端上桌，那种带着香茅与南姜的热气扑面而来。辛辣的香料在舌尖跳舞，让你的体温微微升高。坐在对面的女孩，因为这份热力，脸颊泛起了一层淡淡的红晕，眼神也变得迷离起来。在水波荡漾的背景下，这种「餐桌上的暧昧」比酒精更让人沉醉。

### 💆 触觉的延续
饭后，手牵手沿着河岸散步，湿润的空气包裹着肌肤。在这里，每一道菜都是一次前戏，引导你进入泰国深夜更深层的螺旋中。🐾"""
        },
        "en": {
            "title": "Riverside Noir: Dining on the Chao Phraya – Spice and Waves",
            "desc": "Amidst the mist of the river, let the heat of Thai spices awaken your deepest cravings.",
            "content": """The midnight Chao Phraya River holds a quiet yet seductive tension. The lights of the riverside restaurants reflect on the moving water like a thousand golden serpents.

### 🥘 The Spiral of Spicy Heat
As a bowl of authentic Tom Yum Goong is served, the steam carrying lemongrass and galangal hits your face. Spicy herbs dance on your tongue, causing your body temperature to rise slightly. The girl across from you develops a soft flush on her cheeks from the heat, her eyes becoming hazy. Against the backdrop of the rippling river, this "tabletop flirtation" is more intoxicating than any wine.

### 💆 The Continuation of Touch
After dinner, walking hand-in-hand along the bank, the humid air wraps around your skin. Here, every dish is a prelude, leading you further into the deeper spirals of the Thai night.🐾"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/blog'
for filename, langs_data in restaurant_articles.items():
    for lang, data in langs_data.items():
        folder = os.path.join(base_path, lang)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'---\ntitle: "{data["title"]}"\ndescription: "{data["desc"]}"\npubDate: "2026-03-13"\n---\n\n{data["content"]}\n')

print("Restaurant articles published.")
