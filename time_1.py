import schedule
import requests
import json

from time import sleep



def job():
    requests.post("https://sunhackathon.onrender.com/slack/events", data=json.dumps({
        #メッセージ
        "text" : "検索しましょう<https://www.google.com/|ggrks>",
        #名前
        "username": "赤さん",
        #アイコン
        "icon_emoji":":baby:"
    }))

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    sleep(1)