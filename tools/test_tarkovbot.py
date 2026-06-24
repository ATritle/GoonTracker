from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://tarkovbot.eu/goonstracker",
        wait_until="networkidle"
    )

    text = page.locator("body").inner_text()

    print(text)

    browser.close()
