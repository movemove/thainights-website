import os

articles_part2 = {
    "patpong.md": {
        "zh-cn": {
            "title": "Patpong 帕蓬夜市与红灯区：经典老牌区的魅力与陷阱",
            "desc": "曼谷历史最悠久的红灯区，这里有最著名的 Ping Pong Show，但也充满了游客陷阱。",
            "content": """帕蓬 (Patpong) 是曼谷最早发展起来的红灯区，位于 Silom 区。这里最独特的地方在于红灯区与「帕蓬夜市」紧密结合，你可以一边逛地摊买盗版 T-shirt，一邊被兩旁的 Go-Go Bar 拉客。

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
    }
}

for filename, trans in articles_part2.items():
    for lang in ["zh-cn", "en"]:
        path = f"src/content/blog/{lang}/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            content = f"""---
title: '{trans[lang]['title']}'
description: '{trans[lang]['desc']}'
pubDate: 'Mar 11 2026'
heroImage: '../../assets/blog-placeholder-about.jpg'
---

{trans[lang]['content']}
"""
            f.write(content)
