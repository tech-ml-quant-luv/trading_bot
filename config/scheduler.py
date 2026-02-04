# scheduler_service.py

from apscheduler.schedulers.background import BackgroundScheduler
from config.job_runner import run_pipeline

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    scheduler.add_job(
        run_pipeline,
        trigger="cron",
        day_of_week="mon-fri",
        hour="9-15",
        minute="*/5",
        second=9,
        id="ohlcv_feature_pipeline",
        max_instances=1,
        coalesce=True,
        misfire_grace_time=30
    )

    print("Scheduler started...")
    scheduler.start()

    # IMPORTANT: keep thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.shutdown()
