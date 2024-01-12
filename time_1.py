import crowmwhether
from crontab import CronTab
 
class CrontabControl:
    def __init__(self):
        self.cron = CronTab()
        self.job = None
        self.all_job = None
 
    # ファイルにジョブを書き込むメソッド
    def write_job(self, command, schedule, file_name):
        self.job = self.cron.new(command=command)
        self.job.setall(schedule)
        self.cron.write(file_name)
 
    # ファイル中のジョブを全て読み込むメソッド
    def read_jobs(self, file_name):
        self.all_job = CronTab(tabfile=file_name)
 
    # ジョブを監視するメソッド
    def monitor_start(self, file):
        # スケジュールを読み込む
        self.read_jobs(file)
        for result in self.all_job.run_scheduler():
            # スケジュールになるとこの中の処理が実行される
            print("予定していたスケジュールを実行しました")
 
def main():
    command = 'python3 ./cronweather.py'
    schedule = '55 13 * * *'
    file = 'output.tab'
 
    # インスタンス作成
    c = CrontabControl()
    # ファイルに書き込む
    c.write_job(command, schedule, file)
    # タスクスケジュールの監視を開始
    c.monitor_start(file)
 
if __name__ == "__main__":
    main()

# from slacker import Slacker
# from crontab import CronTab

# slack = Slacker("SLACK_BOT_TOKEN")

 
# class CrontabControl:
#     def __init__(self):
#         self.cron = CronTab()
#         self.job = None
#         self.all_job = None
 
#     # ファイルにジョブを書き込むメソッド
#     def write_job(self, command, schedule, file_name):
#         self.job = self.cron.new(command=command)
#         self.job.setall(schedule)
#         self.cron.write(file_name)
 
#     # ファイル中のジョブを全て読み込むメソッド
#     def read_jobs(self, file_name):
#         self.all_job = CronTab(tabfile=file_name)
 
#     # ジョブを監視するメソッド
#     def monitor_start(self, file):
#         # スケジュールを読み込む
#         self.read_jobs(file)
#         for result in self.all_job.run_scheduler():
#             # スケジュールになるとこの中の処理が実行される
#             slack.chat.post_message('timeline', 'crontab使えてるよ', as_user=True)
#             print("予定していたスケジュールを実行しました")
 
# def main():
#     command = 'python3 time_1.py'
#     schedule = '45 13 * * *'
#     file = 'output.tab'
 
#     # インスタンス作成
#     c = CrontabControl()
#     # ファイルに書き込む
#     c.write_job(command, schedule, file)
#     # タスクスケジュールの監視を開始
#     c.monitor_start(file)

# if __name__ == "__main__":
#     main()

# #WEB_HOOK_URLに、さっき発行したURLを設定
# WEB_HOOK_URL = "https://hooks.slack.com/services/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"

# def job():
#     requests.post(WEB_HOOK_URL, data=json.dumps({
#         #メッセージ
#         "text" : "検索しましょう<https://www.google.com/|ggrks>",
#         #名前
#         "username": "赤さん",
#         #アイコン
#         "icon_emoji":":baby:"
#     }))

# def __init__(self):
#         self.cron = CronTab()
#         self.job = None
#         self.all_job = None

#     # write jobs to file
# def write_job(self, command, schedule, file_name):
#         self.job = self.cron.new(command=command)
#         self.job.setall(schedule)
#         self.cron.write(file_name)

#     # read all jobs from file
# def read_jobs(self, file_name):
#         self.all_job = CronTab(tabfile=file_name)

#     # monitoring job
# def monitor_start(self, file):
#         self.read_jobs(file)
#         for result in self.all_job.run_scheduler():
#             continue


# def main():
#     command = "time_1.py"

#     # 3 p.m. every Sunday (PST) -> 8 a.m. every Monday (JST)
#     schedule = "15 * * * *"

#     output_file = "output.tab"

#     c = CrontabControl()
#     c.write_job(command, schedule, output_file)
#     c.monitor_start(output_file)


# if __name__ == "__main__":
#     main()

# schedule.every(3).seconds.do(job)
