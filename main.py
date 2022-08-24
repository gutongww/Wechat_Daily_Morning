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
his_birthday = os.environ['HIS_BIRTHDAY']
her_birthday = os.environ['HER_BIRTHDAY']

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
    temp = response['current']['temp_c']
    return weather, temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_his_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + his_birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_her_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + her_birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea,"color":"#737CA1"},"temperature":{"value":temperature,"color":"#728FCE"},"love_days":{"value":get_count(),"color":"#F67280"},"his_birthday_left":{"value":get_his_birthday(),"color":"#98AFC7"},"her_birthday_left":{"value":get_her_birthday(),"color":"#98AFC7"},"words":{"value":"要加油哦✌️！","color":"#F2BB66"}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
