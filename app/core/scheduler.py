from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import sentry_sdk

from app.jobs.stock_refresh import run_stock_refresh
from app.jobs.daily_prediction import run_daily_prediction
from app.jobs.cleanup_tasks import run_cleanup

# ✅ Use explicit timezone to avoid server drift bugs
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def start_scheduler():
    if scheduler.running:
        return  # ✅ Prevent duplicate start on reload

    scheduler.add_job(
        run_stock_refresh,
        CronTrigger(hour=5, minute=0),
        id="stock_refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        run_daily_prediction,
        CronTrigger(hour=6, minute=0),
        id="daily_prediction",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        run_cleanup,
        CronTrigger(hour=3, minute=0),
        id="cleanup",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
