from slacker import Slacker
 
def main():
 # APIトークンを設定する
    slack = Slacker("SLACK_BOT_TOKEN")
    # Slackにメッセージを送信する
    slack.chat.post_message('timeline', 'crontabdekita', as_user=True)
 
if __name__ == "__main__":
    main()