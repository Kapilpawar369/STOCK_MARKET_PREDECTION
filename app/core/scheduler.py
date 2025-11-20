from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.stock_refresh import run_stock_refresh
from app.jobs.daily_prediction import run_daily_prediction
from app.jobs.cleanup_tasks import run_cleanup

scheduler = BackgroundScheduler()

def start_scheduler():
    # Every day at 05:00
    scheduler.add_job(run_stock_refresh, "cron", hour=5, minute=0, id="stock_refresh")
    # Every day at 06:00
    scheduler.add_job(run_daily_prediction, "cron", hour=6, minute=0, id="daily_prediction")
    # Every day at 03:00
    scheduler.add_job(run_cleanup, "cron", hour=3, minute=0, id="cleanup")
    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
