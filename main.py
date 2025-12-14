import asyncio
import sys
import tomllib  # Python 3.11+
from playwright.async_api import async_playwright
from parser import parse_linkedin_profile


def load_config():
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("❌ Error: 'config.toml' not found.")
        sys.exit(1)


async def open_manual_browser():
    config = load_config()
    browser_config = config.get("browser", {})
    context_config = config.get("context", {})

    async with async_playwright() as p:
        print("🚀 Launching browser...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=context_config.get("user_data_dir", "./chrome_user_data"),
            headless=browser_config.get("headless", False),
            args=browser_config.get("args", []),
            user_agent=context_config.get("user_agent"),
        )

        print("🔄 Running parser...")
        await parse_linkedin_profile(context)

        print("✅ Manual browser is open. You can browse freely.")
        print("   Close the last active browser window to exit the script.")

        try:
            # Wait for the most recently opened page to close, or keep open recursively?
            # Ideally we just wait indefinitely until user closes the browser (all pages) or kills script.
            # But the original code waited for a "page" to close.
            # We'll stick to waiting for a page close event for now to keep it simple,
            # ideally the one opened by parser or the first one.

            pages = context.pages
            if pages:
                page = pages[-1]  # The one opened by parser likely
                await page.wait_for_event("close", timeout=0)
            else:
                # Should not happen if parser opens a page, but fallback
                print("⚠️ No pages open. Waiting for 10 seconds before exit...")
                await asyncio.sleep(10)

        except KeyboardInterrupt:
            print("🛑 Script interrupted.")
        finally:
            print("🔒 Closing context...")
            await context.close()


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.run(open_manual_browser())
    except KeyboardInterrupt:
        pass
