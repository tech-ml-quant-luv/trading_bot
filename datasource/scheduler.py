from apscheduler.schedulers.blocking import BlockingScheduler
from job_runner import run_pipeline

scheduler = BlockingScheduler(timezone="Asia/Kolkata")

scheduler.add_job(
    run_pipeline,
    trigger="cron",
    minute="*/5",
    second=5,
    max_instances=1,
    coalesce=True,
    timezone="Asia/Kolkata"
)


if __name__ == "__main__":
    print("Scheduler started...")
    scheduler.start()