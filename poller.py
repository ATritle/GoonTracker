import time

from database import initialize
from main import main


def run():

    initialize()

    print("GOON TRACKER POLLER STARTED\n")

    while True:

        try:

            main()

        except Exception as ex:

            print(
                f"\nPoller Error: {ex}\n"
            )

        print(
            "\nWaiting 60 seconds...\n"
        )

        time.sleep(60)


if __name__ == "__main__":
    run()
