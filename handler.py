from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

import azure_openai
import parameter_store
import conversation

slack_bot_token = parameter_store.get_slack_bot_token()
slack_signing_secret = parameter_store.get_slack_signing_secret()
azure_openai_service_api_key = parameter_store.get_azure_openai_service_api_key()

app = App(
    process_before_response=True,
    token=slack_bot_token,
    signing_secret=slack_signing_secret,
)


# ボットへのメンションを受け取るリスナー
@app.event("message")
def main(request, event, ack):
    # タイムアウトしないように、応答だけ返す
    ack()

    # リトライ処理の場合にはヘッダーにx-slack-retry-numが含まれるので、
    # その場合には何もせずに終了
    if 'x-slack-retry-num' in request.headers:
        print('x-slack-retry-num is found.')
        return

    ts = event["ts"]
    channel = event["channel"]

    # スレッドでの会話の場合
    if 'thread_ts' in event:
        chat_message = conversation.create_chat_message_with_history(event, channel)
    else:
        # スレッドでの会話ではない場合
        chat_message = conversation.create_chat_message(event)

    # Azure OpenAIから回答を取得
    answer = azure_openai.get_answer(chat_message, azure_openai_service_api_key)

    # 回答結果を返信
    app.client.chat_postMessage(
        channel=channel,
        text=answer,
        thread_ts=ts
    )


def lambda_handler(event, context):
    # SlackにAPI GatewayのURLを登録する際に使用する。
    if "challenge" in event:
        return {"challenge": event["challenge"]}
    else:
        # Slackからのリクエストを処理する
        slack_handler = SlackRequestHandler(app=app)
        return slack_handler.handle(event, context)