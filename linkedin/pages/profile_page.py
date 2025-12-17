from playwright.async_api import Page
from rich import print
from .selectors.profile_page import LinkedInProfilePageSelectors
from linkedin.linkedin_types import ConnectionStatus, FollowingStatus
from urllib.parse import urlparse

class ProfilePage:
    def __init__(self, page: Page, profile_url: str):
        self.page = page
    
        if not self.is_valid_linkedin_profile_url(profile_url):
            raise ValueError("Invalid LinkedIn profile URL.")
        
        self.profile_url = profile_url
        self.profile = LinkedInProfilePageSelectors(self.page)
    
    @staticmethod
    def is_valid_linkedin_profile_url(profile_url: str) -> bool:
        # EX: https://www.linkedin.com/in/zackspear/

        parsed = urlparse(profile_url)

        if parsed.scheme != "https":
            return False

        if parsed.netloc.lower() != "www.linkedin.com":
            return False

        paths = [p for p in parsed.path.strip("/").split("/") if p]

        return len(paths) == 2 and paths[0] == "in"

    async def execute(self, message: str = ""):

        try:
            await self.page.goto(self.profile_url, wait_until="load")
        except Exception as e:
            print(f"Error: {e}")
            return

        connection_status = await self.get_connection_status()
        following_status = await self.get_following_status()

        print(f"Connection Status: {connection_status}")
        print(f"Following Status: {following_status}")

        if connection_status == ConnectionStatus.NOT_CONNECTED:
            print("🚀 Sending connection request...")
            await self.send_connection(message)
        else:
            print("✨ Already connected or pending.")

    async def get_connection_status(self) -> ConnectionStatus:
        # Check visible buttons first
        if await self.profile.connect_button().is_visible():
            return ConnectionStatus.NOT_CONNECTED
        
        if await self.profile.pending_button().is_visible():
            return ConnectionStatus.PENDING

        if await self.profile.message_button().is_visible():
            return ConnectionStatus.CONNECTED

        return ConnectionStatus.NOT_CONNECTED

    async def get_following_status(self) -> FollowingStatus:
        if await self.profile.following_button().is_visible():
            return FollowingStatus.FOLLOWING
        return FollowingStatus.NOT_FOLLOWING

    async def send_connection(self, note: str = ""):
        # Click Connect. It might be inside the "More" menu.
        if await self.profile.connect_button().is_visible():
            await self.profile.connect_button().click()
        else:
            # Try opening "More" menu
            print("⚠️ 'Connect' button not visible, checking 'More' menu...")

            trigger = self.profile.more_menu_trigger()
            if await trigger.is_visible():
                await trigger.click()
                # Wait for menu item
                connect_btn = self.profile.connect_button() # Re-query or uses same locator? 
                # Playwright locators are lazy, so `get_by_role` should work if it appears in DOM.
                if await connect_btn.is_visible():
                    await connect_btn.click()
                else:
                    print("❌ Could not find 'Connect' button even in 'More' menu.")
                    return
            else:
                 print("❌ Could not find 'Connect' button and no 'More' menu found.")
                 return

        # Handle Dialog
        dialog = self.profile.dialog()
        try:
            await dialog.wait_for(state="visible", timeout=5000)
        except:
             print("⚠️ No dialog appeared after clicking Connect.")
             return

        if note:
             if await self.profile.add_note_button().is_visible():
                 await self.profile.add_note_button().click()
                 # Fill text area (need selector in page object, adding it ad-hoc here or updating page object)
                 await self.page.locator("textarea[name='message']").fill(note)
                 await self.profile.send_button().click()
             else:
                  print("⚠️ 'Add a note' button not found.")
        else:
             if await self.profile.send_without_note_button().is_visible():
                 await self.profile.send_without_note_button().click()
             else:
                 # Sometimes it goes straight to "Send" if no note option? Or maybe "Send now"?
                 # User's example: await dialog.get_by_role("button", name="Send without a note").click()
                 print("⚠️ 'Send without a note' button not found.")

