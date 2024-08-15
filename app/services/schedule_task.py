from app.crud.auth import cleanup_expired_tokens
from app.db.session import get_db
import schedule
import datetime
import time


# for development mode

def run_scheduler():
    # Schedule the task to run every day at 02:51
    # schedule.every().day.at("02:51").do(scheduled_cleanup)
    schedule.every(1).minutes.do(lambda: cleanup_expired_tokens(db=next(get_db())))
    while True:
        schedule.run_pending()
        time.sleep(1)



# Production Mode


# def scheduled_cleanup():
#     # Check if today is the desired day of the week (e.g., Monday)
#     if datetime.datetime.now().weekday() == 0:  # 0 = Monday
#         cleanup_expired_tokens(db=next(get_db()))

# def run_scheduler():
#     # Schedule the task to run every day at 02:51
#     schedule.every().day.at("02:51").do(scheduled_cleanup)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)



