import os
import glob

# Content to translate
files = glob.glob('src/content/blog/zh-tw/*.md')

translations = {
    "zh-cn": {
        "Nana Plaza": "曼谷 Nana Plaza 攻略：全球最大成人游乐场深度评测",
        "Soi Cowboy": "Soi Cowboy 霓虹小巷：曼谷最受欢迎的 Go-Go Bar 聚集地",
        "Patpong": "Patpong 帕蓬夜市与红灯区：经典老牌区的魅力与陷阱",
        "Gentlemen's Clubs": "曼谷高端玩家首选：Gentlemen's Clubs (The Pimp / Sherbet)",
        "Walking Street": "芭提雅 Walking Street：全球老司机的终极朝圣地",
        "Massage": "曼谷按摩全攻略：从普通泰式按摩到「浴室」深度体验",
        # Snippets
        "曼谷": "曼谷",
        "泰國": "泰国",
        "攻略": "攻略",
        "評測": "评测",
        "地圖": "地图",
        "避坑": "避坑",
        "推薦": "推荐",
        "店家": "店家",
        "遊客": "游客",
        "老司機": "老司机",
        "討論區": "讨论区",
        "匿名留言": "匿名留言"
    },
    "en": {
        "Nana Plaza": "Nana Plaza Bangkok Guide: The World's Largest Adult Playground",
        "Soi Cowboy": "Soi Cowboy: Bangkok's Most Popular Neon Alley for Go-Go Bars",
        "Patpong": "Patpong Night Market & Red Light District: Charm and Traps of the Classic District",
        "Gentlemen's Clubs": "Bangkok Elite Choice: Gentlemen's Clubs (The Pimp / Sherbet)",
        "Walking Street": "Pattaya Walking Street: The Ultimate Pilgrimage for Global Players",
        "Massage": "Bangkok Massage Guide: From Traditional Thai to 'Soapy' Deep Experience",
        # Snippets
        "曼谷": "Bangkok",
        "泰國": "Thailand",
        "攻略": "Guide",
        "評測": "Review",
        "地圖": "Map",
        "避坑": "Avoid Scams",
        "推薦": "Recommended",
        "店家": "Venues",
        "遊客": "Tourists",
        "老司機": "Veterans",
        "討論區": "Discussions",
        "匿名留言": "Anonymous Comments"
    }
}

# Simplified content mapping for demonstration, real translation would be deeper
# but I will do a high-quality manual-style translation for the core articles.

articles = {
    "nana-plaza.md": {
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
        "zh-cn": {
            "title": "Soi Cowboy 霓虹小巷：曼谷最受欢迎的 Go-Go Bar 聚集地",
            "desc": "这条充满霓虹灯的小巷是曼谷夜生活的缩影。推荐 Baccara、Crazy House 等名店。",
            "content": """Soi Cowboy 是一条长约 150 公尺的小巷子，位于 Sukhumvit Soi 21 与 Soi 23 之间（捷运 Asok 站旁）。虽然巷子不长，但密集地分布了超过 40 家 Go-Go Bar，是曼谷观光客最爱打卡地点之一。

### 🏆 推荐店家

- **Baccara**: Soi Cowboy 的地标性店家。二楼有著名的透明玻璃地板，气氛非常嗨，通常一位难求。
- **Crazy House**: 装修现代，音乐与表演都非常有张力，是这条巷子里非常有竞争力的店家。
- **Tilac**: 空间非常宽敞，有大型舞台和多个小舞台，适合想要轻松喝酒看表演的朋友。

### ⚠️ 避坑小提醒

1. **路边拉客**: 巷子里常有拿着「Menu」拉客的人，建议直接走进你想去的店，不要理会路边的小蜜蜂。
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
    }
}

# Write files
for filename, trans in articles.items():
    for lang in ["zh-cn", "en"]:
        path = f"src/content/blog/{lang}/{filename}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            content = f"""---
title: '{trans[lang]['title']}'
description: '{trans[lang]['desc']}'
pubDate: 'Mar 11 2026'
heroImage: '../../assets/blog-placeholder-4.jpg'
---

{trans[lang]['content']}
"""
            f.write(content)

print("Generated basic translations for core articles.")
