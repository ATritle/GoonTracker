from collectors.base_web_collector import BaseWebCollector


class GoonTrackerCollector(BaseWebCollector):

    URL = "https://www.tarkov-goon-tracker.com/"

    def get_current_map(self):

        text = self.get_page_text(self.URL)

        section = text.split(
            "The Goons were last seen on:"
        )[1][:300]

        maps = [
            "Lighthouse",
            "Customs",
            "Woods",
            "Shoreline"
        ]

        for map_name in maps:
            if map_name in section:
                return map_name.upper()

        raise Exception(
            "Unable to determine current map"
        )
