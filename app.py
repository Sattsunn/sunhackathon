import os
# from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import AzureOpenAI



client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15"
)

# response = client.chat.completions.create(
#     model="GPT35TURBO", # model = "deployment_name".
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
#         {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
#         {"role": "user", "content": "Do other Azure AI services support this too?"}
#     ]
# )
send_message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        ]
error1 = "返信を送信する際のerrorが起きました"
#chatgptと会話する(返信生成用)の関数
def generate_gpt_reply(message):
    send_message.append({"role": "user", "content": message})
    try:
        response = client.chat.completions.create(
        model="GPT35TURBO", # model = "deployment_name".
        messages= send_message
    )
    except :
        return error1
    reply = response.choices[0].message.content
    return reply

# load_dotenv()

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.event("app_mention")
def message_gpt(message,say):
    send_message = message['text']
    reply = generate_gpt_reply(send_message)
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(reply)


@app.message("hello")
def message_hello(message,say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(text=f"Hello, {message['user']}!,{message['contents']}")

@app.message("hoge")
def hoge_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("hogehoge")

@app.message("あいう")
def hoge_aiu(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("hogehoge")

@app.message("You are a helpful assistant")
def message_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("thank you!")




# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
