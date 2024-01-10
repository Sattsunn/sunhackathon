from slack_bolt import App
import parameter_store

slack_bot_token = parameter_store.get_slack_bot_token()
slack_signing_secret = parameter_store.get_slack_signing_secret()

app = App(
    process_before_response=True,
    token=slack_bot_token,
    signing_secret=slack_signing_secret,
)


def create_chat_message_with_history(event, channel) -> list:
    """
    スレッドの履歴を取得し、Azure OpenAI Serviceへのメッセージを作成します。
    :param event: Slackのイベント
    :param channel: Slackのチャンネル
    :return: Azure OpenAI Serviceへのメッセージ
    """
    chat_message = []
    role = {"role": "system",
            "content": "You are an AI assistant that helps people find information."}

    thread_ts = event['thread_ts']
    messages = app.client.conversations_replies(channel=channel, ts=thread_ts)["messages"]

    # スレッドの履歴を投稿日時の昇順にソートします。
    sorted_messages = sorted(messages, key=lambda x: x["ts"])

    for message in sorted_messages:
        text = message['text']
        conversation = {}

        if 'client_msg_id' in message:
            conversation['role'] = 'user'
            conversation['content'] = text
        elif 'bot_id' in message:
            conversation['role'] = 'assistant'
            conversation['content'] = text

        chat_message.append(conversation)

    chat_message.insert(0, role)
    return chat_message


def create_chat_message(event) -> list:
    """
    スレッドでのやり取りではない場合のAzure OpenAI Serviceへのメッセージを作成します。
    :param event: Slackのイベント
    :return: Azure OpenAI Serviceへのメッセージ
    """
    question = event["text"]
    chat_message = [
        {"role": "system",
         "content": "You are an AI assistant that helps people find information."},
        {"role": "user", "content": question}
    ]
    return chat_message