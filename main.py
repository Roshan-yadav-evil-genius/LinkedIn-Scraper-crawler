from playwright.sync_api import sync_playwright


def open_manual_browser():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./chrome_user_data",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36",
        )

        page = context.new_page()
        page.goto("https://www.google.com")

        page.screenshot()

        print("✅ Manual browser is open. You can browse freely.")
        print("   Close the browser window (top-right ❌) when done.")

        try:
            page.wait_for_event("close", timeout=0)
        except KeyboardInterrupt:
            print("🛑 Script interrupted.")
        finally:
            context.close()


if __name__ == "__main__":
    open_manual_browser()
