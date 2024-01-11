import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import AzureOpenAI
import azure_openai


client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15"
)

azure_openai_service_api_key=os.getenv("AZURE_OPENAI_KEY"), 

response = client.chat.completions.create(
    model="GPT35TURBO", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "こんにちは"}
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
# @app.event("app_mention")
# def message_hello(say):
#     # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
#     say(response.choices[0].message.content)


@app.message("helloworld")
def message_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("hoge")

@app.message("ho")
def hoge_hello(say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say("hogehoge")


# # ボットへのメンションを受け取るリスナー
# @app.event("message")
# def main(request, event, ack):
#     # タイムアウトしないように、応答だけ返す
#     ack()

#     # リトライ処理の場合にはヘッダーにx-slack-retry-numが含まれるので、
#     # その場合には何もせずに終了
#     if 'x-slack-retry-num' in request.headers:
#         print('x-slack-retry-num is found.')
#         return

#     ts = event["ts"]
#     channel = event["channel"]

#     # # スレッドでの会話の場合
#     # if 'thread_ts' in event:
#     #     chat_message = conversation.create_chat_message_with_history(event, channel)
#     # else:
#     #     # スレッドでの会話ではない場合
#     #     chat_message = conversation.create_chat_message(event)

#     # Azure OpenAIから回答を取得
#     answer = azure_openai.get_answer( azure_openai_service_api_key)

#     # 回答結果を返信
#     app.client.chat_postMessage(
#         channel=channel,
#         text=answer,
#         thread_ts=ts
#     )


# def get_answer(chat_message, azure_openai_service_api_key: str) -> str:
#     """
#     Azure OpenAI Serviceから回答を取得します。
#     :param chat_message: Azure OpenAI Serviceに渡す会話履歴
#     :param azure_openai_service_api_key: Azure OpenAI ServiceのAPI Key
#     :return: Azure OpenAI Serviceから取得した回答
#     """
#     openai.api_type = "azure"
#     openai.api_base = os.environ['AZURE_OPENAI_SERVICE_ENDPOINT']
#     openai.api_version = os.environ['AZURE_OPENAI_SERVICE_API_VERSION']
#     openai.api_key = azure_openai_service_api_key

#     response = openai.ChatCompletion.create(
#         engine=os.environ['AZURE_OPENAI_SERVICE_ENGINE'],
#         messages=chat_message,
#         temperature=0.7,
#         max_tokens=800,
#         top_p=0.95,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=None)

#     return response["choices"][3]["message"]["content"]

# def lambda_handler(event, context):
#     # SlackにAPI GatewayのURLを登録する際に使用する。
#     if "challenge" in event:
#         return {"challenge": event["challenge"]}
#     else:
#         # Slackからのリクエストを処理する
#         slack_handler = SlackRequestHandler(app=app)
#         return slack_handler.handle(event, context)

# @app.message("You are a helpful assistant")
# def message_hello(say):
#     # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
#     say(response.choices[0].message.content)




# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))