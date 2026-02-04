import threading
import time
from config.scheduler import start_scheduler
from data.live_data_streaming import start_live_data_stream

def main():

    #Start the scheduler thread
    thread_1 = threading.Thread(
        target = start_scheduler,
        name="SchedulerThread",
        daemon=True
    )

    #Start the Live data feed thread
    thread_2 = threading.Thread(
        target=start_live_data_stream,
        name="LiveDataStreamingThread",
        daemon=True
    )
    thread_1.start()
    print("_Scheduler Started_")
    thread_2.start()
    print("_Live data streaming started_")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMain Stopped")


if __name__ == "__main__":
    main()