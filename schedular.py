from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from database import tasks_db
from bot import send_telegram_message


def check_deadlines():
    now_str = datetime.now().strftime("%H:%M")
    
    for chat_id, tasks in tasks_db.items():
        for task in tasks:
            if not task["is_completed"] and not task["notified"]:
                if task["deadline"] <= now_str:
                    msg = f"<b>Напоминание!</b>\n\n<b>{task['title']}</b> (Дедлайн: {task['deadline']})"

                    success = send_telegram_message(task["chat_id"], msg)

                    if success:
                        task["notified"] = True
                        print(f"[Scheduler] Уведомление отправлено для задачи #{task['id']}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_deadlines, 'interval', minutes=1)
    scheduler.start()