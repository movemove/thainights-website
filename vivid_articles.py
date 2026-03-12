import os

# Define the new 10 articles with vivid, sensory descriptions
new_articles = {
    "thermae-coffee.md": {
        "zh-tw": {
            "title": "蛇美咖啡 Thermae：曼谷地下的慾望流動，傳奇交友聖殿",
            "desc": "踏入這座傳奇的地下咖啡廳，感受空氣中瀰漫的香水與原始慾望。",
            "content": """位於 Sukhumvit 15 巷口地下的蛇美咖啡（Thermae），是無數老司機心目中的麥加。推開那扇沉重的門，微弱的燈光夾雜著冰冷的空調，迎面而來的是上百雙審視與期待的目光。

### 🌀 慾望的環形賽道
這裡沒有 Go-Go Bar 的喧囂音樂，只有低沉的交談聲。女孩們靠牆而立，形成一圈流動的慾望長廊。你不需要點什麼花式調酒，只需一杯啤酒，就能在這場「眼神交鋒」中尋找那個讓你瞬間口乾舌燥的存在。

### 🎭 實戰攻略
- **黃金時間**：晚上 10 點到凌晨 1 點是戰況最激烈的時刻。
- **眼神交流**：在這裡，對視三秒就是一場無聲的契約。如果她對你微笑，那就是邀請你進入她的溫柔鄉。

這裡的交易直接而純粹，省去了酒吧的繁文縟節，只剩下肉體與金錢最原始的博弈。🐾"""
        },
        "zh-cn": {
            "title": "蛇美咖啡 Thermae：曼谷地下的欲望流动，传奇交友圣殿",
            "desc": "踏入这座传奇的地下咖啡厅，感受空气中弥漫的香水与原始欲望。",
            "content": """位于 Sukhumvit 15 巷口地下的蛇美咖啡（Thermae），是无数老司机心目中的麦加。推开那扇沉重的门，微弱的灯光夹杂着冰冷的空调，迎面而来的是上百双审视与期待的目光。

### 🌀 欲望的环形赛道
这里没有 Go-Go Bar 的喧嚣音乐，只有低沉的交谈声。女孩们靠墙而立，形成一圈流动的欲望长廊。你不需要点什么花式调酒，只需一杯啤酒，就能在这场「眼神交锋」中寻找那个让你瞬间口干舌燥的存在。

### 🎭 实战攻略
- **黄金时间**：晚上 10 点到凌晨 1 点是战况最激烈的时刻。
- **眼神交流**：在这里，对视三秒就是一场无声的契约。如果她对你微笑，那就是邀请你进入她的温柔乡。

这里的交易直接而纯粹，省去了酒吧的繁文缛节，只剩下肉体与金钱最原始的博弈。🐾"""
        },
        "en": {
            "title": "Thermae Coffee: Bangkok's Underground Temple of Desire",
            "desc": "Step into this legendary basement cafe where perfume and primal urges fill the air.",
            "content": """Located in the basement of Sukhumvit Soi 15, Thermae is the Mecca for veterans. As you push open the heavy doors, the dim light and cold air hit you, along with hundreds of pairs of eyes filled with anticipation.

### 🌀 The Circular Runway of Lust
There's no blaring music like a Go-Go Bar, only the low hum of negotiation. Girls line the walls, creating a continuous gallery of beauty. You don't need fancy cocktails; a single beer is your ticket to this intense "eye contact" arena where you'll find the one who makes your heart race.

### 🎭 Pro Strategy
- **Peak Hours**: 10 PM to 1 AM is when the selection is at its height.
- **The Look**: Here, a three-second gaze is a contract. If she smiles back, it's an invitation into her private world.

Transactions here are raw and direct, stripped of bar formalities, leaving only the primal exchange of flesh and silver.🐾"""
        }
    },
    "soi6-pattaya.md": {
        "zh-tw": {
            "title": "芭達雅 Soi 6：白日夢想家，整條街都是你的後宮",
            "desc": "當陽光灑在 Soi 6，那不僅是街道，而是荷爾蒙爆炸的起點。",
            "content": """芭達雅的 Soi 6 是所有老司機的後花園。下午兩點，整座城市還在午睡，這裡早已熱氣騰騰。窄小的巷子兩側站滿了穿著極短熱褲與貼身背心的女孩，她們的挑逗比泰國的烈日還要炙熱。

### 🔥 夾道歡迎的熱情
走進這條巷子，你就是國王。女孩們會從酒吧門口探出頭，嬌聲呼喚，甚至動手將你「抓」進店內。這裡不講究浪漫，只講究快感。在狹窄昏暗的二樓「休息室」，你可以聽見牆壁另一側傳來的沉重喘息。

### ⚠️ 生存守則
- **短鐘快戰**：這裡的節奏極快，ST (Short Time) 是主流。
- **白天更嗨**：下午 4 點到 6 點是「搶鮮」的好時機。

如果你喜歡那種「被獵食」的快感，Soi 6 絕對能讓你流連忘返。🐾"""
        },
        "zh-cn": {
            "title": "芭提雅 Soi 6：白日梦想家，整条街都是你的后宫",
            "desc": "当阳光洒在 Soi 6，那不仅是街道，而是荷尔蒙爆炸的起点。",
            "content": """芭提雅的 Soi 6 是所有老司机的后花园。下午两点，整座城市还在午睡，这里早已热气腾腾。窄小的巷子两侧站满了穿着极短热裤与贴身背心的女孩，她们的挑逗比泰国的烈日还要炙热。

### 🔥 夹道欢迎的热情
走进这条巷子，你就是国王。女孩们会从酒吧门口探出头，娇声呼唤，甚至动手将你「抓」进店内。这里不讲究浪漫，只讲究快感。在狭窄昏暗的二楼「休息室」，你可以看见墙壁另一侧传来的沉重喘息。

### ⚠️ 生存守则
- **短钟快战**：这里的节奏极快，ST (Short Time) 是主流。
- **白天更嗨**：下午 4 点到 6 点是「抢鲜」的好时机。

如果你喜欢那种「被猎食」的快感，Soi 6 绝对能让你流连忘返。🐾"""
        },
        "en": {
            "title": "Pattaya Soi 6: The Daytime Harem for Dreamers",
            "desc": "When the sun hits Soi 6, it's not just a street—it's ground zero for a hormonal explosion.",
            "content": """Pattaya’s Soi 6 is every veteran’s playground. At 2 PM, while the rest of the city naps, this place is already steaming. The narrow alley is lined with girls in micro-shorts and skin-tight tops, their teases hotter than the Thai sun.

### 🔥 A Gauntlet of Passion
Walk down this street, and you are king. Girls will lean out of bars, calling your name, sometimes literally "grabbing" you inside. Romance doesn't live here; only pleasure does. In the dimly lit "rooms" upstairs, you can hear the rhythmic heavy breathing from the other side of the thin walls.

### ⚠️ Survival Rules
- **Short Time Action**: The pace here is lightning-fast; ST is the standard.
- **Daylight Delight**: 4 PM to 6 PM is the best time for "fresh" selections.

If you enjoy the thrill of being "preyed upon," Soi 6 will keep you coming back for more.🐾"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/blog'

for filename, trans in new_articles.items():
    for lang in ["zh-tw", "zh-cn", "en"]:
        folder = os.path.join(base_path, lang)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        hero = "../../../assets/blog-placeholder-about.jpg"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'---\ntitle: "{trans[lang]["title"]}"\ndescription: "{trans[lang]["desc"]}"\npubDate: "Mar 12 2026"\nheroImage: "{hero}"\n---\n\n{trans[lang]["content"]}\n')

print("Generated first batch of vivid articles.")
