import re
from datetime import datetime

from playwright.sync_api import sync_playwright

from collectors.base import BaseCollector


class TarkovBotCollector(BaseCollector):

    URL = "https://tarkovbot.eu/goonstracker"

    def get_current_map(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            try:

                page = browser.new_page()

                page.goto(
                    self.URL,
                    wait_until="networkidle"
                )

                text = page.locator(
                    "body"
                ).inner_text()

            finally:

                browser.close()

        match = re.search(
            r"LAST REPORT\s+([A-Za-z]+)\s+\((PVP|PVE)\)",
            text,
            re.MULTILINE
        )

        if not match:
            raise Exception(
                "Unable to determine current map"
            )

        map_name = match.group(1)
        game_mode = match.group(2)

        timestamp_match = re.search(
            r"(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})",
            text
        )

        report_time = None

        if timestamp_match:

            report_time = datetime.strptime(
                timestamp_match.group(1),
                "%d.%m.%Y %H:%M:%S"
            )

        return {
            "map": map_name.upper(),
            "game_mode": game_mode,
            "report_time": report_time
        }