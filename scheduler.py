from apscheduler.schedulers.blocking import BlockingScheduler
from job_runner import run_pipeline

scheduler = BlockingScheduler(timezone="Asia/Kolkata")

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
    misfire_grace_time=30,
    timezone="Asia/Kolkata"
)


if __name__ == "__main__":
    print("Scheduler started...")
    scheduler.start()