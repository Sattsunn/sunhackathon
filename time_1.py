import schedule
import requests
import json

from time import sleep


#WEB_HOOK_URLに、さっき発行したURLを設定
WEB_HOOK_URL = "https://hooks.slack.com/services/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"

def job():
    requests.post(WEB_HOOK_URL, data=json.dumps({
        #メッセージ
        "text" : "検索しましょう<https://www.google.com/|ggrks>",
        #名前
        "username": "赤さん",
        #アイコン
        "icon_emoji":":baby:"
    }))

schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
    sleep(1)
