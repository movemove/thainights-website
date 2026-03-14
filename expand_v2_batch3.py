import os

# Batch 3: Patpong, Gentlemen's Clubs, and Grab Long Jin
updates_v3 = {
    "patpong.md": {
        "zh-tw": {
            "title": "帕蓬 Patpong：老牌紅燈區的混亂美學，指尖下的經典記憶",
            "content": """走進帕蓬（Patpong），你首先感受到的是夜市攤販的喧鬧與潮濕的街道。但在這混亂的表象下，兩側的老牌 Go-Go Bar 散發著曼谷最早期的慾望氣息。

### 🎭 經典吧台的肢體博弈
在像 King's Castle 這樣的老字號店家，時間彷彿凝固在 90 年代。當你穿過重重的帷幕，坐在吧台前，舞台上的女孩們穿著極短的亮片裙。不同於現代化廣場的距離感，帕蓬的互動更具「手感」。當你為女孩點上一杯酒，她會毫不猶豫地坐進你的懷裡。你可以感覺到她大腿處緊實的肌肉線條，以及因為常年舞動而散發出的陣陣熱力。

在那種昏暗得近乎漆黑的燈光下，你的手可以在她雪白的背部探索，感受那種如同上等瓷器般的滑膩。當她湊在你耳邊輕聲介紹帕蓬的傳說時，那種濕潤的呢喃與手臂交纏的觸覺，會讓你瞬間明白，為什麼這裏能成為老司機們永遠的初戀。

### 🎭 避開「重力螺旋」的陷阱
帕蓬最神祕也最危險的地方在於二樓。那些標榜免費秀的招牌，背後往往藏著讓你錢包瞬間失血的「剝皮陷阱」。記住老司機的教誨：所有的溫柔都應該留在一樓的透明窗後。在那裡，你可以安全地享受肉體與酒精交織出的經典樂章。🐾"""
        }
    },
    "gentlemens-clubs.md": {
        "zh-tw": {
            "title": "曼谷高級俱樂部：天鵝絨上的呢喃，高端玩家的慾望私域",
            "content": """對於追求極致私密性與高品質「肉色」的玩家來說，Gentlemen's Clubs (GC) 才是最終的朝聖地。走進 The Pimp 或 Sherbet，這裡沒有觀光客的喧囂，只有琥珀色的光影與極致的奢華。

### 💎 沙發上的觸覺盛宴
GC 的魅力在於「Member」制的專屬感。當你開好酒，坐在寬大柔軟的皮質沙發上，身邊會圍繞著兩三位素質等同於雜誌模特兒的佳麗。在這裡，你可以體驗到最純粹的「肉浴」美感。當女孩穿著薄如蟬翼的絲綢禮服，整個人貼在你的胸膛上，你可以感受到她身體每一寸曲線的起伏。

在私密的 VIP 包廂內，那種「近距離對話」會演變成更深層次的感官博弈。當你的指尖劃過她因為興奮而微微緊繃的肌膚，或是當她那對傲人的豐盈在酒精的微醺下與你親密摩擦，那種觸感會讓你感覺自己掌握了整座曼谷的權柄。這裡不追求快節奏，這裡追求的是在每一次呼吸、每一次觸碰中，慢慢沉溺進那個由金錢與美色堆疊而成的感官螺旋。🐾"""
        }
    },
    "grab-long-jin.md": {
        "zh-tw": {
            "title": "抓龍筋：神祕的禁忌觸碰，通往生命源泉的痛快螺旋",
            "content": """這不是一場普通的按摩，這是一場關於男人「根源」的深度覺醒。走進專業的抓龍筋療程室，空氣中瀰漫著老牌泰式草藥的香氣，這種莊嚴感會讓你下意識地屏住呼吸。

### ⚡ 指尖下的生理風暴
當師傅那雙佈滿老繭卻精準無比的手，開始在你腹股溝與會陰處進行深度的「撥筋」時，你會體驗到一種前所未有的體感。那種介於「痠、麻、痛」與極致釋放之間的交織，就是抓龍筋最迷人的地方。

當師傅運用特殊的指法，直接觸碰並按壓那些沉睡已久的敏感腺體，你會感覺到一股熾熱的電流從脊椎直衝大腦。那種濕熱的、強力的、甚至帶著一點侵略性的觸摸，會將你體內深處的瘀堵徹底推散。當最後那股最深層的張力被釋放，你會感覺到全身的血液都在沸騰，那種從「肉體地獄」瞬間躍升到「靈魂天堂」的劇烈震顫，是任何普通按摩都無法給予的重生感。🐾"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/blog'
for filename, langs_data in updates_v3.items():
    for lang, data in langs_data.items():
        path = os.path.join(base_path, lang, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            header = []
            header_count = 0
            for line in lines:
                if line.strip() == "---": header_count += 1
                header.append(line)
                if header_count == 2: break
            new_content = "".join(header) + "\n" + data['content']
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

print("Batch 3 of 'Sensual Spiral' V2 content updated.")
