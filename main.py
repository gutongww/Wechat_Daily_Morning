from datetime import datetime, date
import requests
import random
import math

# ================= Bark 配置 =================
BARK_KEY = "oQZ92sPHphNF6D7fNvYawR"
BARK_API = f"https://api.day.app/{BARK_KEY}"

# ================= 天气配置 =================
WEATHER_API_KEY = "bb9ebd54256b48f4a8210159260702"
CITY = "Auckland"

# ================= 固定生日 =================
HER_BIRTHDAY = "02-20"  # MM-DD

# ================= 原有文案（不改） =================
DAILY_RANDOM_WORDS = [
    "昭昭心许云深处 岁岁情归峥骨间",
    "娘娘就是要我的命 我眼都不会眨一下 自会取剑剖心",
    "臣在",
    "宁宁 我们什么时候能一起回草原看望春花",
    "你的正面与负面 我全部痴迷",
    "你是我暗室逢灯的际遇 绝渡逢舟的功德",
    "既然这个世界没有真正的感同，那我就身受",
    "珠水不必美 天地之宽 容得下你的不喜欢",
    "我们在相同的频道里",
    "很多人在四通八达的巷子走散 却能在下一个巷口的青砖屋前相遇 如果你愿意 我们以后就定居在那里 如果你不愿意 你想去哪里 我都陪你",
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
        return "今天有点冷 记得多穿一点 "
    elif 13 <= temp <= 20:
        return "今天的温度刚刚好 "
    elif 21 <= temp <= 26:
        return "今天有点暖 记得多喝水 "
    else:
        return "今天可能有点热 "

# ================= 生日倒计时 =================
def birthday_countdown():
    today = date.today()
    year = today.year
    birthday = datetime.strptime(f"{year}-{HER_BIRTHDAY}", "%Y-%m-%d").date()
    if birthday < today:
        birthday = birthday.replace(year=year + 1)
    return (birthday - today).days

# ================= Bark 推送 =================
def send_bark(title, body):
    url = f"{BARK_API}/{title}/{body}"
    params = {
        "sound": "bell",
        "group": "Mio",
        "level": "timeSensitive"
    }
    requests.get(url, params=params, timeout=10)

# ================= 主逻辑 =================
def main():
    weather, temp = get_weather()
    care = temp_care_words(temp)
    days = birthday_countdown()
    words = get_words()

    title = "🌤 奥克兰 · 今日提醒"

    body = (
        f"奥克兰今天 {weather} {temp}℃\n"
        f"{care}\n\n"
        f"距离 Mio 宝宝的生日还有 {days} 天\n\n"
        f"{words}"
    )

    send_bark(title, body)

if __name__ == "__main__":
    main()
