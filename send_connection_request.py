import asyncio
import sys
import tomllib  # Python 3.11+
from playwright.async_api import async_playwright, BrowserContext, Locator
from enum import Enum
from typing import List, Dict
from dataclasses import dataclass
from rich import print


class ConnectionStatus(Enum):
    NOT_CONNECTED = "not_connected"
    CONNECTED = "connected"
    PENDING = "pending"


class FollowingStatus(Enum):
    NOT_FOLLOWING = "not_following"
    FOLLOWING = "following"


@dataclass
class AvailabelButtons:
    element: Locator
    visible: bool


list_availabel_action_buttons: Dict[str, AvailabelButtons] = {}


def load_config():
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("❌ Error: 'config.toml' not found.")
        sys.exit(1)


async def load_linkedin_profile(context: BrowserContext):
    global list_availabel_action_buttons
    page1 = await context.new_page()
    try:
        await page1.goto(
            "https://www.linkedin.com/in/roshanyadavevilgenius/", wait_until="load"
        )
    except Exception as e:
        print(e)

    # if await is_login_required(page1):
    #     print("Login required")
    #     return

    list_availabel_action_buttons = await list_availabel_buttons(page1)

    # await click_action_button("save to pdf",availabel_action_buttons,page1)

    connection_status = await check_connection_status(
        page1, list_availabel_action_buttons
    )
    following_status = await check_following_status(
        page1, list_availabel_action_buttons
    )

    print(f"Connection Status: {connection_status}")
    print(f"Following Status: {following_status}")

    if connection_status == ConnectionStatus.NOT_CONNECTED:
        await send_connection_request(page1)


async def click_action_button(button_name, availabel_action_buttons, page):
    if button_name in availabel_action_buttons:
        if availabel_action_buttons[button_name].visible:
            await availabel_action_buttons[button_name].element.click()
        else:
            if "more" in availabel_action_buttons:
                if not await availabel_action_buttons[button_name].element.is_visible():
                    await availabel_action_buttons["more"].element.click()
                await availabel_action_buttons[button_name].element.click()
                # await availabel_action_buttons["more"].element.click()


async def list_availabel_buttons(page):
    availabel_buttons: Dict[str, AvailabelButtons] = {}
    visible_buttons_xpath = (
        "(//section[contains(@class,'artdeco-card')])[1]"
        "//ul[.//li[contains(normalize-space(.),'connections')]]"
        "/following-sibling::*[1]"
        "//button"
    )
    more_buttons_xpath = (
        "(//section[contains(@class,'artdeco-card')])[1]"
        "//ul[.//li[contains(normalize-space(.),'connections')]]"
        "/following-sibling::*[1]"
        "//div[@role='button']"
    )
    buttons = await page.locator(visible_buttons_xpath).all()
    for button in buttons:
        if await button.is_visible():
            span = button.locator("span").first
            inner_text = (
                await span.inner_text()
                if await span.count() > 0
                else await button.inner_text()
            )
            normalized_text = " ".join(inner_text.split()).lower()
            availabel_buttons[normalized_text] = AvailabelButtons(button, True)

    if "more" in availabel_buttons:
        await availabel_buttons["more"].element.click()
        await page.wait_for_timeout(2000)
        # wait for buttons to be visible

    buttons = await page.locator(more_buttons_xpath).all()
    for button in buttons:
        if await button.is_visible():
            span = button.locator("span").first
            inner_text = (
                await span.inner_text()
                if await span.count() > 0
                else await button.inner_text()
            )
            normalized_text = " ".join(inner_text.split()).lower()
            availabel_buttons[normalized_text] = AvailabelButtons(button, False)

    if "more" in availabel_buttons:
        await availabel_buttons["more"].element.click()

    return availabel_buttons


async def check_connection_status(page, availabel_action_buttons):
    connection_status = ConnectionStatus.NOT_CONNECTED

    # Check for "Connect" button
    if "connect" in availabel_action_buttons:
        connection_status = ConnectionStatus.NOT_CONNECTED
        return connection_status

    # Check for "Pending" (Withdraw) button
    if "pending" in availabel_action_buttons:
        connection_status = ConnectionStatus.PENDING
        return connection_status

    # Check for "Message" button AND existence of "Remove connection" option (implies connected)
    # OR just "Message" as a fallback if "Connect"/"Pending" are absent.
    if (
        "message" in availabel_action_buttons
        or "remove connection" in availabel_action_buttons
    ):
        connection_status = ConnectionStatus.CONNECTED

    return connection_status


async def check_following_status(page, availabel_action_buttons):
    following_status = FollowingStatus.NOT_FOLLOWING

    # Check for "Following" OR "Unfollow" (in menu)
    if (
        "following" in availabel_action_buttons
        or "unfollow" in availabel_action_buttons
    ):
        following_status = FollowingStatus.FOLLOWING

    return following_status


async def get_present_dialog(page):
    dialog = page.locator("//div[contains(@role,'dialog')]")
    if await dialog.count() > 0:
        return dialog
    return None


async def send_connection_request(page, note=""):
    await click_action_button("connect", list_availabel_action_buttons, page)
    dialog = await get_present_dialog(page)
    print("dialog", dialog)
    if dialog:
        if await is_connection_note_dialog(dialog):
            await send_request_with_note(dialog, note)
            # await send_request_without_note(dialog)


async def send_request_with_note(dialog, note):
    send_with_note_btn = dialog.locator("button[aria-label='Add a note']")
    await send_with_note_btn.click()


async def send_request_without_note(dialog):
    send_without_note_btn = dialog.locator("button[aria-label='Send without a note']")
    await send_without_note_btn.click()


async def is_connection_note_dialog(dialog):

    if await dialog.locator("//button[@aria-label='Add a note']").is_visible():
        print("Found 'Add a note' button.")
    if await dialog.locator("//button[@aria-label='Send without a note']").is_visible():
        print("Found 'Send without a note' button.")

    return True


async def add_note_to_invitation_dialog(page):
    print("Checking for invitation modal...")
    try:
        if await get_present_dialog(page):
            print("Invitation modal detected.")
            add_note_btn, send_without_note_btn = await get_invitation_buttons(page)

            if await add_note_btn.is_visible():
                print("Found 'Add a note' button.")

            if await send_without_note_btn.is_visible():
                print("Found 'Send without a note' button.")
        else:
            print("Invitation modal not found (yet).")

    except Exception as e:
        print(f"Error checking invitation modal: {e}")


async def is_invitation_dialog_present(page):
    modal = page.locator("div[aria-labelledby='send-invite-modal']")
    return await modal.count() > 0


async def get_invitation_buttons(page):
    add_note_btn = page.locator("button[aria-label='Add a note']")
    send_without_note_btn = page.locator("button[aria-label='Send without a note']")
    return add_note_btn, send_without_note_btn


async def is_login_required(page):
    login_required = False

    signInPageXpath = """//body[
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

    signInPageElement = page.locator(signInPageXpath)

    try:
        await signInPageElement.wait_for(state="visible", timeout=5000)
        count = await signInPageElement.count()
        if count > 0:
            login_required = True
    except Exception as e:
        print(e)

    for auth_routes_indicator in ["/login", "/checkpoint", "/authwall"]:
        if auth_routes_indicator in page.url:
            login_required = True
            break

    return login_required


async def open_manual_browser():
    config = load_config()
    browser_config = config.get("browser", {})
    context_config = config.get("context", {})
    # context_config = {}

    async with async_playwright() as p:
        print("🚀 Launching browser...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=context_config.get("user_data_dir", "./chrome_user_data1"),
            headless=browser_config.get("headless", False),
            args=browser_config.get("args", []),
            user_agent=context_config.get("user_agent"),
            viewport={"width": 1920, "height": 1080},
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
