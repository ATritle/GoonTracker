import re

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

                text = page.locator("body").inner_text()

            finally:

                browser.close()

        match = re.search(
            r"LAST REPORT\s+([A-Za-z]+)\s+\((PVP|PVE)\)",
            text,
            re.MULTILINE
        )

        if match:

            map_name = match.group(1)

            return map_name.upper()

        raise Exception(
            "Unable to determine current map"
        )
