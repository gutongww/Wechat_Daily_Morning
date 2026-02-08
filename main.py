from datetime import datetime, date
import requests
import random
import math

# ================= Bark 配置 =================
BARK_KEYS = [
    "oQZ92sPHphNF6D7fNvYawR",
    "uBSGy5uo7yrbb6JknU4B5F"  
]

BARK_APIS = [f"https://api.day.app/{key}" for key in BARK_KEYS]

# ================= 天气配置 =================
WEATHER_API_KEY = "bb9ebd54256b48f4a8210159260702"
CITY = "Auckland"

# ================= 固定生日 =================
HER_BIRTHDAY = "02-20"  # MM-DD

# ================= 原有文案（不改） =================
DAILY_RANDOM_WORDS = [
    "昭昭心许云深处 岁岁情归峥骨间",
    "娘娘就是要我的命 我眼都不会眨一下 自会取剑剖心",
    "宁宁 我们什么时候能一起回草原看望春花",
    "你的正面与负面 我全部痴迷",
    "老派约会啊 那我们要一路沿着珠江边走 毫无顾忌地饮酒 话题要漫无目的 像鱼在海里游泳"
    "在最后一个路口 我们会仰望绵延千里的骑楼街 去底下的一家咖啡店买两杯馥芮白 在等待窗口站五分钟 我们会无聊 所以我会碰碰你的肩 你会摸摸我的头 而这样细微的触动 让五分钟的等待有了无限意义"
    "你是我暗室逢灯的际遇 绝渡逢舟的功德",
    "既然这个世界没有真正的感同，那我就身受",
    "珠水不必美 天地之宽 容得下你的不喜欢",
    "试着接受我吧 人生在正确与错误之外 还有爱啊",
    "我们在相同的频道里",
    "在你可寻找的范围内 我一直在",
]

def get_words():
    today_md = datetime.now().strftime("%m-%d")
    if today_md == "02-15": 
        return "宝宝 今天玩得开心点哦 我就在家里乖乖等你回来 宝宝你今天回来之后还爱我么 不爱也没关系 不要把凌青或者猎娇带回家里就好啦"
    if today_md == "02-20":
        return "生日快乐 Mio 宝宝 愿你被温柔包围 好运常在 万事胜意"
    return random.choice(DAILY_RANDOM_WORDS)

# ================= 奥克兰天气 =================
def get_weather():
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": CITY,
        "lang": "zh"
    }
    res = requests.get(url, params=params, timeout=10).json()
    weather = res["current"]["condition"]["text"]
    temp = math.floor(res["current"]["temp_c"])
    return weather, temp

# ================= 温度关心语 =================
def temp_care_words(temp):
    if temp <= 12:
        return "今天有点冷 要多穿一点 小心着凉"
    elif 13 <= temp <= 20:
        return "今天的温度刚刚好 "
    elif 21 <= temp <= 24:
        return "今天有点热 记得多喝水 "
    else:
        return "今天可能很热 出门要做好防晒哦 "

# ================= 生日倒计时 =================
def birthday_countdown():
    today = date.today()
    year = today.year
    birthday = datetime.strptime(f"{year}-{HER_BIRTHDAY}", "%Y-%m-%d").date()
    if birthday < today:
        birthday = birthday.replace(year=year + 1)
    return (birthday - today).days

# ================= Bark 推送（双人） =================
def send_bark(title, body):
    params = {
        "sound": "bell",
        "group": "Mio",
        "level": "timeSensitive"
    }
    for api in BARK_APIS:
        url = f"{api}/{title}/{body}"
        requests.get(url, params=params, timeout=10)

# ================= 主逻辑 =================
def main():
    weather, temp = get_weather()
    care = temp_care_words(temp)
    days = birthday_countdown()
    words = get_words()

    title = "🌤 奥克兰 · 今日提醒"

    birthday_line = "Mio宝宝的生日就是今天！\n\n" if days == 0 else f"距离 Mio 宝宝的生日还有 {days} 天\n\n"
    body = (
        f"奥克兰今天 {weather} {temp}℃\n"
        f"{care}\n\n"
        f"{birthday_line}"
        f"{words}"
    )

    send_bark(title, body)

if __name__ == "__main__":
    main()
