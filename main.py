import threading
from config.scheduler import start_scheduler

def main():
    scheduler_thread = threading.Thread(
        target=start_scheduler,
        name="SchedulerThread",
        daemon=True
    )

    scheduler_thread.start()

    print("Main process running...")

    # Keep main alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Main stopped")

if __name__ == "__main__":
    main()
