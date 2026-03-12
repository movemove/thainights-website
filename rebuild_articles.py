import os

articles = {
    "nana-plaza.md": {
        "zh-tw": {
            "title": "曼谷 Nana Plaza 攻略：全球最大成人遊樂場深度評測",
            "desc": "位於 Sukhumvit Soi 4 的三層樓傳奇建築，新手必看指南。",
            "content": """Nana Plaza 被譽為「世界上最大的成人遊樂場」。位於 Sukhumvit Soi 4，這座三層樓的建築物就像是一個微型都市，每一層都有其獨特的風格與魅力。

### 🏆 推薦店家

- **Straps (2F)**: 這裡的氣氛極佳，Ladyboy 們的素質也非常高，適合想要初次嘗試不同體驗的朋友。
- **Rainbow 4 (1F)**: 經典的 Go-Go Bar，音樂大聲，能量滿滿，表演也非常敬業。
- **Billboard (3F)**: 這裏有著名的旋轉舞台，空間寬敞，適合在那邊喝杯飲料慢慢欣賞。

### ⚠️ 避坑小提醒

1. 進店後先看酒單確認價格，通常啤酒在 150-200 泰銖左右。
2. 請妹妹喝飲料 (Ladydrink) 之前，先確認價格，避免結帳時產生不必要的糾紛。"""
        },
        "zh-cn": {
            "title": "曼谷 Nana Plaza 攻略：全球最大成人游乐场深度评测",
            "desc": "位于 Sukhumvit Soi 4 的三层楼传奇建筑，新手必看指南。",
            "content": """Nana Plaza 被誉为「世界上最大的成人游乐场」。位于 Sukhumvit Soi 4，这座三层楼的建筑物就像是一个微型都市，每一层都有其独特的风格与魅力。

### 🏆 推荐店家

- **Straps (2F)**: 这里的气氛极佳，Ladyboy 们的素质也非常高，适合想要初次尝试不同体验的朋友。
- **Rainbow 4 (1F)**: 经典的 Go-Go Bar，音乐大声，能量满满，表演也非常敬业。
- **Billboard (3F)**: 这里有著名的旋转舞台，空间宽敞，适合在那里喝杯饮料慢慢欣赏。

### ⚠️ 避坑小提醒

1. 进店后先看酒单确认价格，通常啤酒在 150-200 泰铢左右。
2. 请妹妹喝饮料 (Ladydrink) 之前，先确认价格，避免结帐时产生不必要的纠纷。"""
        },
        "en": {
            "title": "Nana Plaza Bangkok Guide: The World's Largest Adult Playground",
            "desc": "A three-story legendary complex on Sukhumvit Soi 4. A must-visit for newcomers.",
            "content": """Nana Plaza is often called "The World's Largest Adult Playground." Located on Sukhumvit Soi 4, this three-story complex is like a micro-city, where each floor has its own unique style and charm.

### 🏆 Recommended Venues

- **Straps (2F)**: Excellent atmosphere with high-quality Ladyboy performers. Perfect for those looking for a unique first-time experience.
- **Rainbow 4 (1F)**: A classic Go-Go Bar. Loud music, high energy, and very professional performances.
- **Billboard (3F)**: Famous for its rotating stage and spacious layout. A great place to enjoy a drink and watch the show.

### ⚠️ Essential Tips

1. Always check the drink menu for prices first. Typically, a beer costs around 150-200 THB.
2. Confirm the price of a "Ladydrink" before buying one to avoid any billing disputes later."""
        }
    },
    "soi-cowboy.md": {
        "zh-tw": {
            "title": "Soi Cowboy 霓虹小巷：曼谷最受歡迎的 Go-Go Bar 聚集地",
            "desc": "這條充滿霓虹燈的小巷是曼谷夜生活的縮影。推薦 Baccara、Crazy House 等名店。",
            "content": """Soi Cowboy 是一條長約 150 公尺的小巷子，位於 Sukhumvit Soi 21 與 Soi 23 之間（捷運 Asok 站旁）。雖然巷子不長，但密集地分佈了超過 40 家 Go-Go Bar，是曼谷觀光客最愛打卡地點之一。

### 🏆 推薦店家

- **Baccara**: Soi Cowboy 的地標性店家。二樓有著名的透明玻璃地板，氣氛非常嗨，通常一位難求。
- **Crazy House**: 裝潢現代，音樂與表演都非常有張力，是這條巷子里非常有競爭力的店家。
- **Tilac**: 空間非常寬敞，有大型舞台和多個小舞台，適合想要輕鬆喝酒看表演的朋友。

### ⚠️ 避坑小提醒

1. **路邊拉客**: 巷子里常有拿著「Menu」拉客的人，建議直接走進你想去的店，不要理會路邊的小蜜蜂。
2. **門口拍照**: 大多數店家門口嚴禁拍照，請尊重當地規定，避免發生衝突。
3. **結帳檢查**: 雖然 Soi Cowboy 相對安全，但結帳時還是建議瞄一眼帳單金額是否正確。"""
        },
        "zh-cn": {
            "title": "Soi Cowboy 霓虹小巷：曼谷最受欢迎的 Go-Go Bar 聚集地",
            "desc": "这条充满霓虹灯的小巷是曼谷夜生活的缩影。推荐 Baccara、Crazy House 等名店。",
            "content": """Soi Cowboy 是一条长约 150 公尺的小巷子，位于 Sukhumvit Soi 21 与 Soi 23 之间（捷运 Asok 站旁）。虽然巷子不长，但密集地分布了超过 40 家 Go-Go Bar，是曼谷观光客最爱打卡地点之一。

### 🏆 推荐店家

- **Baccara**: Soi Cowboy 的地标性店家。二楼有著名的透明玻璃地板，气氛非常嗨，通常一位难求。
- **Crazy House**: 装修现代，音乐与表演都非常有张力，是这条巷子里非常有竞争力的店家。
- **Tilac**: 空间非常宽敞，有大型舞台和多个小舞台，适合想要轻松喝酒看表演的朋友。

### ⚠️ 避坑小提醒

1. **路边拉客**: 巷子里常有拿着「Menu」拉客的人，建议直接走进你想去的店，不要理会路边的子。
2. **门口拍照**: 大多数店家门口严禁拍照，请尊重当地规定，避免发生冲突。
3. **结帐检查**: 虽然 Soi Cowboy 相对安全，但结帐时还是建议瞄一眼账单金额是否正确。"""
        },
        "en": {
            "title": "Soi Cowboy Guide: Bangkok's Most Iconic Neon Red-Light District",
            "desc": "This neon-drenched alleyway is the epitome of Bangkok nightlife. Featuring legendary spots like Baccara and Crazy House.",
            "content": """Soi Cowboy is a 150-meter long alley located between Sukhumvit Soi 21 and Soi 23 (next to BTS Asok). Despite its short length, it houses over 40 Go-Go Bars and is one of the most photographed nightlife spots in Bangkok.

### 🏆 Top Recommendations

- **Baccara**: The most famous venue in the alley. Known for its glass floor on the second level and a consistently high-energy atmosphere. Usually very crowded.
- **Crazy House**: Modern decor with high-impact music and performances. One of the most competitive and exciting venues in the area.
- **Tilac**: Very spacious with multiple stages. Ideal for those who want a bit more breathing room while enjoying the shows.

### ⚠️ Pro-Tips to Avoid Scams

1. **Street Hawkers**: You'll see people on the street with "menus" trying to lure you in. It's best to ignore them and head straight into a reputable bar of your choice.
2. **Photography**: Most bars strictly prohibit photography near their entrances. Please respect this to avoid unwanted confrontations.
3. **Bill Check**: While Soi Cowboy is generally safe, it's always good practice to double-check your bill before paying."""
        }
    },
    "patpong.md": {
        "zh-tw": {
            "title": "Patpong 帕蓬夜市與紅燈區：經典老牌區的魅力與陷阱",
            "desc": "曼谷歷史最悠久的紅燈區，這裡有最著名的 Ping Pong Show，但也充滿了觀光客陷阱。",
            "content": """帕蓬 (Patpong) 是曼谷最早發展起來的紅燈區，位於 Silom 區。這裡最獨特的地方在於紅燈區與「帕蓬夜市」緊密結合，你可以一邊逛地攤買盜版 T-shirt，一邊被兩旁的 Go-Go Bar 拉客。

### 🎭 區域名店

- **King's Castle 1 & 2**: 這裡的表演非常經典，氣氛比較偏向傳統的 Go-Go Bar，相對安全。
- **Pink Panther**: 設有大螢幕轉播球賽，還有現場泰拳表演，吸引了不少喜歡輕鬆氛圍的遊客。

### ⚠️ 終極警告：避開二樓店家！

這是帕蓬區最重要的法則：**絕對不要跟著路邊拉客的小蜜蜂上二樓！**

二樓的店通常標榜「免費秀」或「飲料 100 泰銖」，但當你進去後，結帳時帳單可能會變成幾千甚至上萬泰銖。如果你想看秀，請留在**一樓**的透明落地窗店家，或是去正規的表演場所。

### 💡 建議行程

建議下午先去 Silom 周邊吃美食，晚上 8 點左右來逛逛夜市，隨後選一家一樓的 Go-Go Bar 喝杯飲料感受氣氛即可。"""
        },
        "zh-cn": {
            "title": "Patpong 帕蓬夜市与红灯区：经典老牌区的魅力与陷阱",
            "desc": "曼谷历史最悠久的红灯区，这里有最著名的 Ping Pong Show，但也充满了游客陷阱。",
            "content": """帕蓬 (Patpong) 是曼谷最早发展起来的红灯区，位于 Silom 区。这里最独特的地方在于红灯区与「帕蓬夜市」紧密结合，你可以一边逛地摊买盗版 T-shirt，一边被两旁的 Go-Go Bar 拉客。

### 🎭 区域名店

- **King's Castle 1 & 2**: 这里的表演非常经典，气氛比较偏向传统的 Go-Go Bar，相对安全。
- **Pink Panther**: 设有大屏幕转播球赛，还有现场泰拳表演，吸引了不少喜欢轻松氛围的游客。

### ⚠️ 终极警告：避开二楼店家！

这是帕蓬区最重要的法则：**绝对不要跟着路边拉客的小蜜蜂上二楼！**

二楼的店通常标榜「免费秀」或「饮料 100 泰铢」，但当你进去后，结帐时账单可能会变成几千甚至上万泰铢。如果你想看秀，请留在**一楼**的透明落地窗店家，或是去正规的表演场所。

### 💡 建议行程

建议下午先去 Silom 周边吃美食，晚上 8 点左右来逛逛夜市，随后选一家一楼的 Go-Go Bar 喝杯饮料感受气氛即可。"""
        },
        "en": {
            "title": "Patpong Night Market & Red Light District: Charm and Traps",
            "desc": "Bangkok's oldest red-light district, home to the famous Ping Pong Shows and many tourist traps.",
            "content": """Patpong is the original red-light district of Bangkok, located in the Silom area. Its unique feature is the seamless integration of the "Patpong Night Market" with the Go-Go Bars lining both sides of the street.

### 🎭 Top Venues

- **King's Castle 1 & 2**: Known for classic performances with a traditional Go-Go Bar atmosphere. Generally considered safe and reputable.
- **Pink Panther**: Features large screens for sports and live Muay Thai matches, attracting a crowd looking for a more relaxed vibe.

### ⚠️ The Golden Rule: Avoid the Second Floor!

This is the most critical advice for Patpong: **Never follow street touts to a second-floor bar!**

These venues often lure tourists with promises of "free shows" or "100 THB drinks," but once inside, you may be presented with a bill for thousands or even tens of thousands of THB. If you want to enjoy a show safely, stay at the **ground-floor** venues with transparent windows or visit legitimate theaters.

### 💡 Recommended Itinerary

Have dinner in the Silom area in the late afternoon, head to the night market around 8 PM, and then pick a ground-floor Go-Go Bar to soak in the atmosphere with a drink."""
        }
    },
    "gentlemens-clubs.md": {
        "zh-tw": {
            "title": "曼谷高端玩家首選：Gentlemen's Clubs (The Pimp / Sherbet)",
            "desc": "如果你預算充足，想要體驗更高層次的泰國夜生活，這些私人俱樂部是你的最佳選擇。",
            "content": """與 Nana Plaza 或 Soi Cowboy 的混亂不同，曼谷的 Gentlemen's Clubs (GC) 提供的是更高端、更具私密性的娛樂體驗。這裡通常需要開酒（Member），環境優雅，表演素質也更高。

### 💎 頂級推薦

- **The Pimp**: 曼谷最著名的 GC。場地巨大，有各種風格的包廂與泳池派對。這裡的模特兒素質極高，適合多人聚會或預算寬裕的玩家。
- **Sherbet / Monte Carlo**: 位於 Ekkamai 區，這裡的氣氛更像是一個高級酒吧，有現場樂隊表演，是當地富裕階層常去的地方。

### 💰 消費模式

這些地方通常採用「買酒開卡」的制度。
1.  **開酒費**: 通常需要購買數瓶烈酒作為入會。
2.  **Model 費用**: 陪同人員會依照「節數」(Starts) 計費。
3.  **小費**: 建議準備一些百元鈔票發放。"""
        },
        "zh-cn": {
            "title": "曼谷高端玩家首选：Gentlemen's Clubs (The Pimp / Sherbet)",
            "desc": "如果你预算充足，想要体验更高层次的泰国夜生活，这些私人俱乐部是你的最佳选择。",
            "content": """与 Nana Plaza 或 Soi Cowboy 的混乱不同，曼谷的 Gentlemen's Clubs (GC) 提供的是更高端、更具私密性的娱乐体验。这里通常需要开酒（Member），环境优雅，表演素质也更高。

### 💎 顶级推荐

- **The Pimp**: 曼谷最著名的 GC。场地巨大，有各种风格的包厢与泳池派对。这里的模特儿素质极高，适合多人聚会或预算宽裕的玩家。
- **Sherbet / Monte Carlo**: 位于 Ekkamai 区，这里的气氛更像是一个高级酒吧，有现场乐队表演，是当地富裕阶层常去的地方。

### 💰 消费模式

这些地方通常采用「买酒开卡」的制度。
1.  **开酒费**: 通常需要购买数瓶烈酒作为入会。
2.  **Model 费用**: 陪同人员会依照「节数」(Starts) 计费。
3.  **小费**: 建议准备一些百元钞票发放。"""
        },
        "en": {
            "title": "Bangkok's Elite Choice: Gentlemen's Clubs (The Pimp / Sherbet)",
            "desc": "For those with a healthy budget seeking a more sophisticated and private nightlife experience.",
            "content": """Unlike the chaotic vibes of Nana Plaza or Soi Cowboy, Bangkok’s Gentlemen’s Clubs (GC) offer a premium, private entertainment experience. Membership usually involves buying bottles, with elegant surroundings and higher-caliber performers.

### 💎 Top Recommendations

- **The Pimp**: The most legendary GC in Bangkok. A massive venue featuring themed private rooms and pool parties. Known for exceptionally high-quality models, it's perfect for groups or high-rollers.
- **Sherbet / Monte Carlo**: Located in the Ekkamai area, the atmosphere here is more akin to an upscale lounge with live bands, popular among Bangkok’s elite.

### 💰 Pricing Model

These venues typically operate on a "Member Card" system:
1.  **Membership**: Requires the purchase of multiple bottles of premium spirits.
2.  **Model Fees**: Companions are billed by "Starts" (time intervals).
3.  **Tips**: It's recommended to have 100 THB bills ready for tipping."""
        }
    },
    "pattaya-walking-street.md": {
        "zh-tw": {
            "title": "芭達雅 Walking Street：全球老司機的終極朝聖地",
            "desc": "如果曼谷是夜生活的天堂，那麼芭達雅 Walking Street 就是天堂的中心。這裏有最瘋狂的派對與最密集的酒吧。",
            "content": """來到芭達雅，如果沒去過 Walking Street (步行街)，等於沒來過。這條在海濱大道盡頭的街，白天看似平凡，晚上 7 點封路後，這裡會變成全世界能量最高的娛樂區域。

### 🔥 必訪 Go-Go Bar

- **Windmill**: 以「瘋狂」著稱，這裡的表演尺度極大，是 Walking Street 的地標。
- **Palace**: 這裡的舞蹈團隊非常專業，燈光與音樂效果一流，是欣賞高顏值表演者的首選。
- **Baccara (Pattaya Branch)**: 與曼谷分店一樣，以制服風格和玻璃地板聞名。

### 🚨 玩家生存守則

1.  **小心扒手**: 雖然這裡警察很多，但在擁擠的街上還是要看好錢包。
2.  **鐘點戰**: 芭達雅的消費邏輯與曼谷略有不同，Bar Fine 價格會隨時間變動。
3.  **大冒險**: 支線的 Soi 6 或 Soi Buakhao 也有很多平價且有趣的選擇。

### 💡 小建議

建議可以在黃昏時分先在海灘邊喝杯啤酒，等到 9 點之後再正式進入 Walking Street，那是氣氛最高昂的時刻！🐾"""
        },
        "zh-cn": {
            "title": "芭提雅 Walking Street：全球老司机的终极朝圣地",
            "desc": "如果曼谷是夜生活的天堂，那么芭提雅 Walking Street 就是天堂的中心。这里有最疯狂的派对与最密集的酒吧。",
            "content": """来到芭提雅，如果没去过 Walking Street (步行街)，等于没来过。这条在海滨大道尽头的街，白天看似平凡，晚上 7 点封路后，这里会变成全世界能量最高的娱乐区域。

### 🔥 必访 Go-Go Bar

- **Windmill**: 以「疯狂」著称，这里的表演尺度极大，是 Walking Street 的地标。
- **Palace**: 这里的舞蹈团队非常专业，灯光与音乐效果一流，是欣赏高颜值表演者的首选。
- **Baccara (Pattaya Branch)**: 与曼谷分店一样，以制服风格和玻璃地板闻名。

### 🚨 玩家生存守則

1.  **小心扒手**: 虽然这里警察很多，但在拥挤的街上还是要把看好钱包。
2.  **钟点战**: 芭提雅的消费逻辑与曼谷略不同，Bar Fine 价格会随时间变動。
3.  **大冒险**: 支线的 Soi 6 或 Soi Buakhao 也有很多平价且有趣的選擇。

### 💡 小建议

建议可以在黄昏时分先在海滩边喝杯啤酒，等到 9 点之后再正式进入 Walking Street，那是气氛最高昂的时刻！🐾"""
        },
        "en": {
            "title": "Pattaya Walking Street: The Ultimate Pilgrimage for Global Players",
            "desc": "If Bangkok is the heaven of nightlife, Walking Street is its center. Home to the craziest parties and densest bars.",
            "content": """Coming to Pattaya without visiting Walking Street is like never coming at all. This street at the end of Beach Road looks ordinary by day, but after 7 PM, it becomes one of the highest-energy entertainment zones in the world.

### 🔥 Must-Visit Go-Go Bars

- **Windmill**: Famous for its "wild" vibe and extreme performances. An iconic landmark of the street.
- **Palace**: Features professional dance troupes with top-tier lighting and sound. The top choice for high-visual performances.
- **Baccara (Pattaya)**: Like its Bangkok counterpart, famous for its uniform themes and transparent second-floor walkway.

### 🚨 Player Survival Guide

1. **Watch for Pickpockets**: Despite the heavy police presence, keep a close eye on your wallet in crowded areas.
2. **Timing Matters**: Pattaya's Bar Fine logic differs slightly from Bangkok; prices may vary depending on the time.
3. **Explore Side Streets**: Nearby Soi 6 or Soi Buakhao offer more affordable and fun alternatives.

### 💡 Pro Tip

Grab a beer on the beach at sunset, and wait until after 9 PM to enter Walking Street when the atmosphere reaches its peak!🐾"""
        }
    },
    "massage-guide.md": {
        "zh-tw": {
            "title": "曼谷按摩全攻略：從普通泰式按摩到「浴室」深度體驗",
            "desc": "泰國按摩種類繁多，從路邊 300 泰銖的平價按摩，到充滿儀式感的「肥皂按摩」，一篇教你如何選擇。",
            "content": """泰國是按摩愛好者的天堂。但「純」與「不純」之間，往往只有一線之隔。了解泰國按摩的分類，能讓你玩得更盡興且不踩雷。

### 💆 分類導覽

1.  **純式按摩 (Traditional Thai)**:
    - **推薦**: Health Land, Let's Relax 等連鎖店。
    - **體驗**: 正統筋絡放鬆，CP 值極高。
2.  **抓龍筋 (Health Prostate Massage)**:
    - **特色**: 針對男性生理功能的特殊按摩。
    - **推薦**: 選擇有認證的老牌店家，確保衛生與專業度。
3.  **肥皂按摩 (Soapy Massage / 浴室)**:
    - **特色**: 泰國夜生活最奢華的體驗之一。
    - **名店**: Maria, Emmanuelle, Long Beach。這裡的環境像五星級飯店，提供全方位的洗浴服務。

### ⚠️ 注意事項

- **小費文化**: 按摩結束後，建議給予師傅 50-100 泰銖的小費。
- **透明度**: 高級浴室通常有透明玻璃房（魚缸）供挑選，價格公開透明，不會有隱藏消費。

---

不論你是想要放鬆筋骨，還是想要極致享受，曼谷的按摩文化絕對能滿足你的所有需求！"""
        },
        "zh-cn": {
            "title": "曼谷按摩全攻略：从普通泰式按摩到「浴室」深度体验",
            "desc": "泰国按摩种类繁多，从路边 300 泰铢的平价按摩，到充满仪式感的「肥皂按摩」，一篇教你如何选择。",
            "content": """泰国是按摩爱好者的天堂。但「纯」与「不纯」之间，往往只有一线之隔。了解泰国按摩的分类，能让你玩得更尽兴且不踩雷。

### 💆 分类导览

1.  **纯式按摩 (Traditional Thai)**:
    - **推荐**: Health Land, Let's Relax 等连锁店。
    - **体验**: 正统筋络放松，CP 值极高。
2.  **抓龙筋 (Health Prostate Massage)**:
    - **特色**: 针对男性生理功能的特殊按摩.
    - **推荐**: 选择有认证的老牌店家，确保卫生与专业度。
3.  **肥皂按摩 (Soapy Massage / 浴室)**:
    - **特色**: 泰国夜生活最奢华的体验之一。
    - **名店**: Maria, Emmanuelle, Long Beach。这里的环境像五星级饭店，提供全方位的洗浴服务。

### ⚠️ 注意事项

- **小费文化**: 按摩结束后，建议给予师傅 50-100 泰铢的小费。
- **透明度**: 高級浴室通常有透明玻璃房（鱼缸）供挑选，价格公开透明，不会有隐藏消费。

---

不论你是想要放松筋骨，还是想要极致享受，曼谷的按摩文化绝对能满足你的所有需求！"""
        },
        "en": {
            "title": "Bangkok Massage Guide: From Traditional Thai to 'Soapy' Experiences",
            "desc": "Thailand is a paradise for massage lovers. Learn the difference between 'pure' and 'not so pure' venues here.",
            "content": """Thailand is a mecca for massage. However, there's often a fine line between therapeutic and "extra" services. Understanding the categories will help you enjoy the best experience.

### 💆 Category Overview

1. **Traditional Thai Massage**:
   - **Recommended**: Chains like Health Land or Let's Relax.
   - **Experience**: Authentic muscle relaxation with great value.
2. **Prostate Massage (Grab Long Jin)**:
   - **Specialty**: A traditional technique focused on male physiological health.
   - **Recommended**: Stick to established venues with certified practitioners for hygiene and professionalism.
3. **Soapy Massage (Bathhouse)**:
   - **Specialty**: One of the most luxurious nightlife experiences.
   - **Venues**: Maria, Emmanuelle, Long Beach. These look like 5-star hotels and offer comprehensive bathing services.

### ⚠️ Things to Note

- **Tip Culture**: It's customary to give a 50-100 THB tip after the session.
- **Transparency**: High-end soapy massage parlors feature transparent viewing rooms (the "fishbowl") with clear pricing.

---

Whether you want to relax your muscles or indulge in ultimate luxury, Bangkok's massage scene has it all!"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/blog'

for filename, trans in articles.items():
    for lang in ["zh-tw", "zh-cn", "en"]:
        folder = os.path.join(base_path, lang)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        
        # Hero images mapping
        hero = "../../../assets/blog-placeholder-about.jpg"
        if "nana-plaza" in filename: hero = "../../../assets/blog-placeholder-3.jpg"
        if "soi-cowboy" in filename: hero = "../../../assets/blog-placeholder-4.jpg"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: '{trans[lang]['title']}'
description: '{trans[lang]['desc']}'
pubDate: 'Mar 11 2026'
heroImage: '{hero}'
---

{trans[lang]['content']}
""")

print("Successfully reconstructed all 18 articles across 3 languages.")
