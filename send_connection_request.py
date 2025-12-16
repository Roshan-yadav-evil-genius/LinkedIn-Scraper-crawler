import asyncio
import sys
import tomllib  # Python 3.11+
from playwright.async_api import async_playwright, BrowserContext
from enum import Enum

class ConnectionStatus(Enum):
    NOT_CONNECTED = "not_connected"
    CONNECTED = "connected"
    PENDING = "pending"

class FollowingStatus(Enum):
    NOT_FOLLOWING = "not_following"
    FOLLOWING = "following"

def load_config():
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("❌ Error: 'config.toml' not found.")
        sys.exit(1)


async def load_linkedin_profile(context: BrowserContext):
    page1 = await context.new_page()
    await page1.goto("https://www.linkedin.com/in/roshanyadavevilgenius/",wait_until="load")
    
    if await is_login_required(page1):
        print("Login required")
        return

    await check_connection_status(page1)
    await check_following_status(page1)

async def check_connection_status(page):
    connection_status = ConnectionStatus.NOT_CONNECTED
    
    
async def check_following_status(page):
    following_status = FollowingStatus.NOT_FOLLOWING
    
    


async def is_login_required(page):
    login_required = False

    signInPageXpath="""//body[
        //input[@type='password']
        or
        //button[.//span[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign in')]]
        or
        //a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign in')]
        or
        //*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'welcome back')]
        or
        //*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign in using another account')]
        or
        //*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'continue with google')]
    ]"""
    # no need for selector just get elemnt by selector no need to wait
    signInPageElement = await page.locator(signInPageXpath)

    if signInPageElement:
        login_required = True

    for auth_routes_indicator in ["/login", "/checkpoint", "/authwall"]:
        if auth_routes_indicator in page.url:
            login_required = True
            break


    return login_required




async def open_manual_browser():
    config = load_config()
    browser_config = config.get("browser", {})
    # context_config = config.get("context", {})
    context_config = {}

    async with async_playwright() as p:
        print("🚀 Launching browser...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=context_config.get("user_data_dir", "./chrome_user_data1"),
            headless=browser_config.get("headless", False),
            args=browser_config.get("args", []),
            user_agent=context_config.get("user_agent"),
        )

        print("🔄 Running parser...")
        await load_linkedin_profile(context)

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
