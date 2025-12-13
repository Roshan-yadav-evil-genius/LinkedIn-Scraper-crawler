from playwright.sync_api import sync_playwright
import sys
import tomllib  # Python 3.11+


def load_config():
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("❌ Error: 'config.toml' not found.")
        sys.exit(1)


def open_manual_browser():
    config = load_config()
    browser_config = config.get("browser", {})
    context_config = config.get("context", {})
    print(browser_config)
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=context_config.get("user_data_dir", "./chrome_user_data"),
            headless=browser_config.get("headless", False),
            args=browser_config.get("args", []),
            user_agent=context_config.get("user_agent"),
        )

        page = context.pages[0] if context.pages else context.new_page()
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
