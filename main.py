from collections import Counter

from database import save_sighting
from database import get_latest_map

from collectors.goontracker import GoonTrackerCollector
from collectors.tarkovbot import TarkovBotCollector


def main():

    collectors = [
        ("GoonTracker", GoonTrackerCollector()),
        ("TarkovBot", TarkovBotCollector())
    ]

    print("\nGOON TRACKER\n")

    results = []

    for source_name, collector in collectors:

        try:

            current_map = collector.get_current_map()

            results.append(current_map)

            print(
                f"{source_name:<15} : {current_map}"
            )

            last_map = get_latest_map(
                source_name
            )

            if last_map != current_map:

                save_sighting(
                    source_name,
                    current_map
                )

                print(
                    f"{'':15}   Saved"
                )

            else:

                print(
                    f"{'':15}   No Change"
                )

        except Exception as ex:

            print(
                f"{source_name:<15} : ERROR -> {ex}"
            )

    if results:

        counts = Counter(results)

        consensus_map = counts.most_common(1)[0][0]

        confidence = (
            counts[consensus_map]
            / len(results)
        ) * 100

        print()
        print(f"Consensus      : {consensus_map}")
        print(f"Confidence     : {confidence:.0f}%")


if __name__ == "__main__":
    main()
