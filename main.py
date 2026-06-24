from datetime import datetime

from database import save_sighting
from database import get_latest_sighting

from collectors.goontracker import GoonTrackerCollector
from collectors.tarkovbot import TarkovBotCollector


def main():

    collectors = [
        ("GoonTracker", GoonTrackerCollector()),
        ("TarkovBot", TarkovBotCollector())
    ]

    print("\nGOON TRACKER\n")

    reports = []

    for source_name, collector in collectors:

        try:

            report = collector.get_current_map()

            reports.append(
                {
                    "source": source_name,
                    **report
                }
            )

            print(
                f"{source_name:<15} : {report['map']}"
            )

            latest = get_latest_sighting(
                source_name
            )

            changed = (
                latest is None
                or latest["map"] != report["map"]
            )

            if changed:

                save_sighting(
                    source_name,
                    report["map"],
                    report["game_mode"],
                    str(report["report_time"])
                    if report["report_time"]
                    else None
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

    if reports:

        print()
        print("=" * 50)
        print("CURRENT REPORTS")
        print("=" * 50)

        for report in reports:

            report_time = (
                report["report_time"]
                if report["report_time"]
                else "Unknown"
            )

            print(
                f"{report['source']:<15} : "
                f"{report['map']:<12} "
                f"{report_time}"
            )

        print()

        unique_maps = {
            report["map"]
            for report in reports
        }

        if len(unique_maps) == 1:

            agreed_map = next(iter(unique_maps))

            print(
                "STATUS         : AGREEMENT"
            )

            print(
                f"LOCATION       : {agreed_map}"
            )

        else:

            print(
                "STATUS         : DISAGREEMENT"
            )

            print(
                f"TRACKERS       : {len(unique_maps)} different locations reported"
            )

        reports_with_time = [
            report
            for report in reports
            if report["report_time"] is not None
        ]

        if reports_with_time:

            latest_report = max(
                reports_with_time,
                key=lambda report: report["report_time"]
            )

            print()
            print("LATEST TIMESTAMPED REPORT")

            print(
                f"LOCATION       : {latest_report['map']}"
            )

            print(
                f"SOURCE         : {latest_report['source']}"
            )

            print(
                f"REPORTED       : {latest_report['report_time']}"
            )


if __name__ == "__main__":
    main()
