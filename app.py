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

send_message = [
            {"role": "system", "content": "You are a professional instructor. When you submit a keyword, I will give you two errata questions that will help you better understand that keyword.When you are sent the answers, grade them, out of 10 points."},
            {"role": "user", "content": "keyword: GPU"},
            {"role": "assistant", "content": "Great! Here are two errata questions related to the keyword GPU:In the provided answers for the keyword GPU is there any factual inaccuracy or information that could be further clarified? If yes, please point it out.Is there any additional information about GPUs that you think could enhance the completeness of the provided answers? If yes, please provide it.Please go ahead and provide your answers, and I'll grade them accordingly."},
            {"role": "user", "content": "answer: (1) yes (2) yes "},
            {"role": "assistant", "content": "Thank you for your responses. Let's go through the grading for each question:In the provided answers for the keyword GPU is there any factual inaccuracy or information that could be further clarified? If yes, please point it out.It seems there are no specific details pointed out for correction or clarification. However, it would be beneficial if you could specify the areas of concern to provide more precise feedback. Score: 2.5/3 Is there any additional information about GPUs that you think could enhance the completeness of the provided answers? If yes, please provide it. Again, without specific details on what additional information could be included, it's challenging to provide targeted feedback. If you have any particular aspects in mind, feel free to mention them for more accurate evaluation. Score: 2.5/3 Total Score: 5/6 Your responses suggest there might be room for improvement or clarification, but without specific details, it's challenging to provide precise feedback. If you have any specific points you'd like to address, please let me know!"},
        ]
error1 = "返信を送信する際のerrorが起きました"
#chatgptと会話する(返信生成用)の関数
def generate_gpt_reply(message):
    #apiへ送るメッセージに送られたmessageを追加する
    send_message.append({"role": "user", "content": message})
    try:
        response = client.chat.completions.create(
        model="GPT35TURBO", # model = "deployment_name".
        messages= send_message
    )
        
    except :
        return error1
    reply = response.choices[0].message.content
    #返信をapiに送るメッセージに追加する
    send_message.append({"role": "assistant", "content": reply})
    return reply

# load_dotenv()

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.event("app_mention")
def message_gpt(body,say):
    #channel,messageなどをbodyから取り出す
    channel_id = body["event"]["channel"]
    send_message = body["event"]["text"]
    thread_id = body["event"]["ts"]
    #関数を使ってreplyを生成
    reply = generate_gpt_reply(send_message)
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(text=reply,channel=channel_id, thread_ts=thread_id)

#stampを追加(考え中・わかった・わからないを判別するため)
@app.message(":man-tipping-hand:")
def react_to_emoji(body, say, client):
    channel_id = body["channel"]
    timestamp = body["ts"]

    # スタンプをつける（以下3か所全部同じ）
    client.reactions_add(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        channel=channel_id,
        timestamp=timestamp,
        name="man-raising-hand",
    )
    client.reactions_add(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        channel=channel_id,
        timestamp=timestamp,
        name="woman-gesturing-no",
    )
    client.reactions_add(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        channel=channel_id,
        timestamp=timestamp,
        name="thinking_face",
    )


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

# sattsun
    



# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
