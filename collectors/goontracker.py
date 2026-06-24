from datetime import datetime

from collectors.base_web_collector import BaseWebCollector


class GoonTrackerCollector(BaseWebCollector):

    URL = "https://www.tarkov-goon-tracker.com/"

    def get_current_map(self):

        text = self.get_page_text(self.URL)

        section = text.split(
            "The Goons were last seen on:"
        )[1][:300]

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        if not lines:
            raise Exception(
                "Unable to determine current map"
            )

        current_map = lines[0]

        return {
            "map": current_map.upper(),
            "game_mode": None,
            "report_time": None
        }
