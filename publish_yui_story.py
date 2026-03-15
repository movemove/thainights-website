import os
import shutil

# Story Data for "The Yui Chronicles" - Inspired by Uncle03 style
yui_story = {
    "yui-spiral.md": {
        "zh-tw": {
            "title": "曼谷之巔的黑色洗禮 ── 與「Yui」的頂級螺旋",
            "description": "在那首 Stay with me 的旋律中，我與 Yui 在曼谷的深夜進行了一場靈魂與肉體的徹底交換。",
            "content": """耳邊響起松原みき那首經典的《Stay with me》，輕快的 City Pop 旋律在 Crazy House 的空氣中震盪，卻掩蓋不住那股讓人理智瓦解的淫靡氣息。

東京的夜晚是壓抑的黑色西裝，而曼谷的夜晚，是破碎的、瘋狂旋轉的紅色霓虹。我推了推眼鏡，目光在 Soi Cowboy 那些交錯的胴體間逡巡。阿乃已經點好了酒，正與媽媽桑調笑，體現著某種老掉牙的「資本主義優勢」。我原本以為今晚又會是一場佛系的「城市考察」，直到 **Yui** 出現。

她是一個典型的「大奶小隻馬」，雪白如凝脂的肌膚在紅光下閃爍著微弱的光澤。她沒有像其他女孩那樣機械地扭動，而是對著我露出了一個帶著小酒窩的微笑，眼睛笑得像月牙兒一樣，帶著一絲尚未被這座城市徹底污染的純真。

「我要你 paybar 我，這是命令。」當我靠近她耳邊輕聲說出這句話時，我看見她眼底閃過一絲不可思議的驚喜。我看見阿乃在旁邊嘿嘿直笑，但我知道，今晚的心靈豐盈比射精的那幾秒鐘更為重要。

**【場景：曼谷飯店房間】**

門鎖扣上的聲音，宣告了現實世界的徹底消失。

比起短鐘房的侷促，飯店寬敞的空間才適合這場感官的史詩。Yui 換上了那件日系小公主風格的睡衣，包得緊緊的，那種極端的反差感反而點燃了我內心最深處的惡魔。當她緩緩拉下肩帶，那一對巨大的、充滿膠原蛋白的豪乳如同熟透的果實般跳動而出，粉紅色的**乳頭**因為興奮與微涼的空調而堅挺著。

我將她推倒在微涼的床榻上。她那滑嫩如綢緞的肌膚在月光下泛著瑩潤的光。我俯下身，先是用唇瓣輕輕含住她的**乳頭**，感受著那種如同軟糖般的彈性。隨後，我的手滑向那片早已泥濘不堪的禁地。當我碩大的**龜頭**撐開那道粉嫩、緊緻的**小穴**縫隙，緩緩沒入那灼熱、濕潤的深處時，Yui 發出了一聲如同小貓般嬌羞的呻吟。

「噢...好深...」她用生澀的中文呢喃。

我開始變換姿勢。我讓她背對著我，雙手撐在窗台上。從後方看去，她滿背的細緻刺青與雪白的臀部構成了曼谷深夜最神祕的圖騰。我扶著她的胯骨，每一次猛烈的撞擊都發出清脆的「啪、啪」聲，**龜頭**在那不斷收縮的**小穴**內壁中進進出出，摩擦出的體溫彷彿要將靈魂融化。

最終，在最後幾十次的瘋狂衝刺中，我感覺到她的小穴發生了痙攣般的劇烈收縮，像是有無數隻小手在拼命向內拉扯。在那種極端的緊縛感中，我緊緊抱住她，將積蓄已久的灼熱全部灌注進那充滿誘惑的螺旋深處...

回台灣的飛機上，耳機裡依然播著那首 Stay with me。阿乃說九月的機票比較便宜，我笑了笑。也許，我愛上的不只是 Yui，而是這座與東京完全相反、能讓人徹底沈淪的城市。🐾"""
        },
        "zh-cn": {
            "title": "曼谷之巅的黑色洗礼 ── 与「Yui」的顶级螺旋",
            "description": "在那首 Stay with me 的旋律中，我与 Yui 在曼谷的深夜进行了一场灵魂与肉体的彻底交换。",
            "content": """耳边响起松原みき那首经典的《Stay with me》，轻快的 City Pop 旋律在 Crazy House 的空气中震荡，却掩盖不住那股让人理智瓦解的淫靡气息。

东京的夜晚是压抑的黑色西装，而曼谷的夜晚，是破碎的、疯狂旋转的红色霓虹。我推了推眼镜，目光在 Soi Cowboy 那些交错的胴体间逡巡。阿乃已经点好了酒，正与妈妈桑调笑，体现着某种老掉牙的「资本主义优势」。我原本以为今晚又会是一场佛系的「城市考察」，直到 **Yui** 出现。

她是一个典型的「大奶小只马」，雪白如凝脂的肌肤在红光下闪烁着微弱的光泽。她没有像其他女孩那样机械地扭动，而是对着我露出了一个带着小酒窝的微笑，眼睛笑得像月牙儿一样，带着一丝尚未被这座城市彻底污染的纯真。

「我要你 paybar 我，这是命令。」当我靠近她耳边轻声说出这句话时，我看见她眼底闪过一丝不可思议的惊喜。我看见阿乃在旁边嘿嘿直笑，但我知道，今晚的心灵丰盈比射精的那几秒钟更为重要。

**【场景：曼谷酒店房间】**

门锁扣上的声音，宣告了现实世界的彻底消失。

比起短钟房的局促，酒店宽敞的空间才适合这场感官的史诗。Yui 换上了那件日系小公主风格的睡衣，包得紧紧的，那种极端的反差感反而点燃了我内心最深处的恶魔。当她缓缓拉下肩带，那一对巨大的、充满胶原蛋白的豪乳如同熟透的果实般跳动而出，粉红色的**乳头**因为兴奋与微凉的空调而坚挺着。

我将她推倒在微凉的床榻上。她那滑嫩如绸缎的肌肤在月光下泛着莹润的光。我俯下身，先是用唇瓣轻轻含住她的**乳头**，感受着那种如同软糖般的弹性。随后，我的手滑向那片早已泥泞不堪的禁地。当我硕大的**龟头**撑开那道粉嫩、紧致的**小穴**缝隙，缓缓没入那灼热、湿润的深处时，Yui 发出了一声如同小猫般娇羞的呻吟。

「噢...好深...」她用生涩的中文呢喃。

我开始变换姿势。我让她背对着我，双手撑在窗台上。从后方看去，她满背的细致纹身与雪白的臀部构成了曼谷深夜最神秘的图腾。我扶着她的胯骨，每一次猛烈的撞击都发出清脆的「啪、啪」声，**龟头**在那不断收缩的**小穴**内壁中进进出出，摩擦出的体温仿佛要将灵魂融化。

最终，在最后几十次的疯狂冲刺中，我感觉到她的下身发生了痉挛般的剧烈收缩，像是无数只小手在拼命向内拉扯。在那种极端的紧缚感中，我紧紧抱住她，将积蓄已久的灼热全部灌注进那充满诱惑的螺旋深处...

回台湾的飞机上，耳机里依然播着那首 Stay with me。阿乃说九月的机票比较便宜，我笑了笑。也许，我爱上的不只是 Yui，而是这座与东京完全相反、能让人彻底沈沦的城市。🐾"""
        },
        "en": {
            "title": "The Black Baptism of Bangkok ── Ultimate Spiral with 'Yui'",
            "description": "To the melody of Stay with me, I engaged in a profound exchange of soul and flesh with Yui in the heart of Bangkok.",
            "content": """Miki Matsubara's "Stay with Me" plays in my ears, the upbeat City Pop rhythm pulsating through Crazy House, yet failing to drown out the air of logic-shattering decadence.

Tokyo nights are repressed black suits; Bangkok nights are shattered, madly spinning red neons. I pushed up my glasses, my gaze drifting across the intermingling bodies of Soi Cowboy. A-Nai had already ordered drinks, flirting with the Mama-san—a classic display of "capitalist advantage." I thought tonight would be another Zen "urban inspection," until **Yui** appeared.

She was the perfect "big-breasted petite," with skin as white and smooth as congealed fat, shimmering faintly under the red light. She didn't writhe mechanically like the other girls. Instead, she flashed me a dimpled smile, her eyes curving like crescent moons, carrying a trace of innocence not yet tainted by this city.

"I want you to pay-bar me. That’s an order." As I whispered this into her ear, I saw a flicker of unbelievable surprise in her eyes. I saw A-Nai laughing nearby, but I knew that tonight's spiritual fulfillment was far more important than those few seconds of ejaculation.

**[Scene: Bangkok Hotel Room]**

The click of the door lock signaled the total disappearance of the real world.

Compared to the cramped short-time rooms, a spacious hotel suite was the only fitting stage for this sensory epic. Yui changed into a Japanese-style "little princess" nightgown, wrapped tightly—that extreme contrast only ignited the demon deep within me. As she slowly pulled down the straps, those massive, collagen-rich breasts sprang free like ripened fruit, her pink **nipples** standing firm from excitement and the cool air conditioning.

I pushed her onto the cool bedsheets. Her silken skin glowed like polished jade under the moonlight. Leaning down, I first took her **nipple** softly into my lips, feeling the gummy-like elasticity. Then, my hand slid toward that already rain-slicked forbidden zone. As my large **glans** pried open the tight, tender slit of her **vagina**, slowly submerging into those scorching, moist depths, Yui let out a moan as coy as a kitten.

"Oh... so deep..." she murmured in broken Chinese.

I began to shift positions. I turned her over, hands braced against the window sill. Looking from behind, the intricate tattoos across her back contrasted with her snow-white buttocks, forming the most mysterious totem of the Bangkok night. Gripping her hips, each fierce impact let out a sharp "slap, slap." My **glans** moved in and out of the constantly contracting walls of her **vagina**, the friction generating a heat that threatened to melt my very soul.

Finally, in the dozens of frantic lunges at the end, I felt her vagina undergo a violent, spasming contraction, like countless tiny hands pulling inward with all their might. In that extreme bondage, I held her body tight, pouring my long-accumulated heat into the depths of that seductive spiral...

On the plane back to Taiwan, my headphones were still playing Stay with Me. A-Nai said September tickets are cheaper. I smiled. Perhaps, what I fell in love with wasn't just Yui, but this city—the polar opposite of Tokyo—that allows a man to truly submerge himself.🐾"""
        }
    }
}

base_path = '/home/alice/.openclaw/workspace/thainights_pages/src/content/stories'

for filename, langs_data in yui_story.items():
    for lang, data in langs_data.items():
        folder = os.path.join(base_path, lang)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        
        # Determine hero image
        hero = "../../../assets/hero/soi-cowboy.png"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'---\ntitle: "{data["title"]}"\ndescription: "{data["description"]}"\npubDate: "2026-03-16"\nheroImage: "{hero}"\n---\n\n{data["content"]}\n')

print("New story 'Yui Spiral' published across all languages.")
