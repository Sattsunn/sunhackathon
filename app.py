import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15"
)

response = client.chat.completions.create(
    model="GPT35TURBO", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)


load_dotenv()

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# 'hello' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.event("app_mention")
def message_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(response.choices[0].message.content)


@app.message("hello")
def message_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("helloa!")

@app.message("You are a helpful assistant")
def message_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(response.choices[0].message.content)




# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))