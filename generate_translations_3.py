import os

articles_part3 = {
    "pattaya-walking-street.md": {
        "zh-cn": {
            "title": "芭提雅 Walking Street：全球老司机的终极朝圣地",
            "desc": "如果曼谷是夜生活的天堂，那么芭提雅 Walking Street 就是天堂的中心。这里有最疯狂的派对与最密集的酒吧。",
            "content": """来到芭提雅，如果没去过 Walking Street (步行街)，等于没来过。这条在海滨大道尽头的街，白天看似平凡，晚上 7 点封路后，这里会变成全世界能量最高的娱乐区域。

### 🔥 必访 Go-Go Bar

- **Windmill**: 以「疯狂」著称，这里的表演尺度极大，是 Walking Street 的地标。
- **Palace**: 这里的舞蹈团队非常专业，灯光与音乐效果一流，是欣赏高颜值表演者的首选。
- **Baccara (Pattaya Branch)**: 与曼谷分店一样，以制服风格和玻璃地板闻名。

### 🚨 玩家生存守则

1.  **小心扒手**: 虽然这里警察很多，但在拥挤的街上还是要看好钱包。
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
        "zh-cn": {
            "title": "曼谷按摩全攻略：从普通泰式按摩到「浴室」深度体验",
            "desc": "泰国按摩种类繁多，从路边 300 泰铢的平价按摩，到充满仪式感的「肥皂按摩」，一篇教你如何选择。",
            "content": """泰国是按摩爱好者的天堂。但「纯」与「不纯」之间，往往只有一线之隔。了解泰国按摩的分类，能让你玩得更尽兴且不踩雷。

### 💆 分类导览

1.  **纯式按摩 (Traditional Thai)**:
    - **推荐**: Health Land, Let's Relax 等连锁店。
    - **体验**: 正统筋络放松，CP 值极高。
2.  **抓龙筋 (Health Prostate Massage)**:
    - **特色**: 针对男性生理功能的特殊按摩。
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

for filename, trans in articles_part3.items():
    for lang in ["zh-cn", "en"]:
        path = f"src/content/blog/{lang}/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            content = f"""---
title: '{trans[lang]['title']}'
description: '{trans[lang]['desc']}'
pubDate: 'Mar 11 2026'
heroImage: '../../../assets/blog-placeholder-about.jpg'
---

{trans[lang]['content']}
"""
            f.write(content)
