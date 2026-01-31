from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
her_birthday = "02-20"  # 2.20

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]

rapid_Key = os.environ["RAPID_KEY"]

def get_weather():
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": "Auckland"}

    headers = {
        "X-RapidAPI-Key": rapid_Key,
        "X-RapidAPI-Host": 'weatherapi-com.p.rapidapi.com'
    }

    response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    weather = response['current']['condition']['text']
    temp = math.floor(response['current']['temp_c'])
    return weather, temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_her_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + her_birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 平日随机文案
DAILY_RANDOM_WORDS = [
    "昭昭心许云深处，岁岁情归峥骨间",
    "娘娘就是要我的命，我眼都不会眨一下，自会取剑剖心",
    "臣在",
    "宁宁 我们什么时候能一起回草原看望春花",
    "你的正面与负面 我全部痴迷",
    "你是我暗室逢灯的际遇、绝渡逢舟的功德",
    "既然这个世界没有真正的感同，那我就身受",
    "珠水不必美 天地之宽 容得下你的不喜欢",
    "我们在相同的频道里",
    "很多人在四通八达的巷子走散，却能在下一个巷口的青砖屋前相遇。如果你愿意，我们以后就定居在那里。如果你不愿意，你想去哪里，我都陪你",
    "在你可寻找的范围内，我一直在",
]

def get_words():
  today_md = today.strftime("%m-%d")
  if today_md == "02-15":
    return "宝宝 今天玩得开心点哦 我就在家里乖乖等你回来 宝宝你今天回来之后还爱我么 不爱也没关系 不要把凌青或者猎娇带回家里就好啦"
  if today_md == "02-20":
    return "我身无长物 烂命真心 唯有贱命一条 价值千金 赠与Mio宝宝 做生日贺礼 --蒋伯驾"
  return random.choice(DAILY_RANDOM_WORDS)

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea,"color":"#737CA1"},"temperature":{"value":temperature,"color":"#728FCE"},"love_days":{"value":get_count(),"color":"#F67280"},"her_birthday_left":{"value":get_her_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":"#F2BB66"}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
