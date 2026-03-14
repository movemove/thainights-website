import os

# Content definitions for the "Sensual Spiral" V2 - Batch 2
updates_v2 = {
    "soi-cowboy.md": {
        "zh-tw": {
            "title": "曼谷 Soi Cowboy：霓虹魅影中的指尖流浪，極致親密攻略",
            "content": """走進 Soi Cowboy，那兩排密集的紅色霓虹燈會讓你的視覺瞬間過載。這條不足兩百公尺的巷子，卻是曼谷最能讓人臉紅心跳的肌膚戰場。

### 🏮 霓虹倒影下的肢體接觸
當你踏入像 Baccara 這樣的傳奇店家，坐在舞台最前排的高腳椅上，你與女孩們的距離僅剩幾公分。當她們在透明的玻璃地板上舞動，微弱的紅光會勾勒出她們大腿內側絲滑的陰影。最讓人心跳加速的時刻，是當你點了一杯 Ladydrink，她跨過舞台直接坐在你雙腿間的瞬間。

你可以大膽地將手環繞在她的纖腰上，感受那種因為頻繁舞動而緊緻且帶著驚人熱度的肌膚。在 Cowboy，互動是具備高度節奏感的。當音樂進入副歌，女孩會貼近你的胸膛，用她那充滿香水味的長髮輕掃你的臉頰，那種濕潤的呼吸聲伴隨著酒精，會讓你徹底迷失在這場霓虹螺旋中。

### 🏮 Baccara 的二樓神祕學
如果你追求更極致的觸感，一定要上二樓。在那透明的地面上，視覺與觸覺會產生奇妙的交織。在這裡，你可以更自由地探索那綢緞般的肌膚質感。當你的手心感受到她們大腿傳來的輕微顫慄，那種「掌控與被誘惑」的博弈，就是 Soi Cowboy 讓人流連忘返的真正密碼。

### 💡 實戰微操
- **觸碰的藝術**：在牛仔巷，適度的身體互動是被允許且受歡迎的。大膽展現你的熱情，女孩們會回饋你更深層的溫柔。
- **眼神鎖定**：當你盯著她的眼睛時，試著輕輕摩挲她的指尖，這能瞬間點燃對方的火熱回應。🐾"""
        }
    },
    "windmill-pattaya.md": {
        "zh-tw": {
            "title": "芭達雅 Windmill：極限感官黑洞，瘋狂肉慾的旋渦中心",
            "content": """在芭達雅 Walking Street 的後半段，藏著一個讓無數老司機理智斷線的地方 ── Windmill (風車)。這裡沒有規則，只有最原始、最直白的肉體碰撞。

### 🌀 肉慾旋渦的起點
踏入 Windmill 的那一刻，你必須做好視覺與體感被徹底轟炸的準備。這裡的女孩幾乎處於完全開放的狀態。當你坐在舞台邊緣，幾十個赤裸的胴體會在你的視線中瘋狂交錯。不同於曼谷的婉約，這裡的女孩會主動發起進攻。

她們會直接引導你的手，去觸碰那最柔軟、最私密的禁地。你會感覺到那濕潤、灼熱且充滿生命力的肌膚在你的掌心下起伏。在 Windmill，最經典的體驗莫過於女孩在吧台上張開雙腿，讓你近距離觀測那粉嫩的幽谷。那種視覺與觸覺的雙重暴擊，會讓你的大腦瞬間空白。

### 🌀 吧台上的感官地獄
這裡最刺激的在於「零距離互動」。女孩會用她們豐滿的胸部磨蹭你的臉龐，甚至在酒精的催化下，在吧台邊進行短暫而火熱的交鋒。當那對 Z-CUP 的豪乳在你面前劇烈顫動，伴隨著汗水滴落在你的手背上，你會感覺到整個世界的重心都消失了，只剩下這場永無止境的螺旋。

### 🛡️ 瘋狂後的生存建議
- **放下矜持**：來到 Windmill 就不要當紳士。在這裡，大膽的探索和直接的渴望才是通往極致快感的門票。
- **預算儲備**：因為互動極其頻繁，建議多準備一些百元泰銖，適時的小費會讓女孩為你展現更驚人的尺度。🐾"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/blog'
for filename, langs_data in updates_v2.items():
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

print("Batch 2 of 'Sensual Spiral' V2 content updated.")
