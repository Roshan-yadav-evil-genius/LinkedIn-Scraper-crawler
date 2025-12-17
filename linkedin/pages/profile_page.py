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

    async def execute(self):

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
            await self.send_connection_request("Muskan Kindly except my connection request")
        else:
            print("✨ Already connected or pending.")
            await self.withdraw_connection_request()

    async def get_connection_status(self) -> ConnectionStatus:

        if await self.profile.connect_button().count():
            return ConnectionStatus.NOT_CONNECTED
        
        if await self.profile.pending_button().count():
            return ConnectionStatus.PENDING

        return ConnectionStatus.NOT_CONNECTED

    async def get_following_status(self) -> FollowingStatus:
        if await self.profile.follow_button().count():
            return FollowingStatus.NOT_FOLLOWING
        return FollowingStatus.FOLLOWING

    async def send_connection_request(self, note: str = ""):
        connect_btn = self.profile.connect_button()
        
        # Click Connect. It might be inside the "More" menu.
        if await connect_btn.is_visible():
            await connect_btn.click()
        else:
            # Try opening "More" menu
            print("⚠️ 'Connect' button not visible, checking 'More' menu...")

            more_menu_button = self.profile.more_menu_button()
            await more_menu_button.click()
            try:
                await connect_btn.wait_for(state="visible", timeout=5000)
            except:
                print("❌ Could not find 'Connect' button even in 'More' menu.")
                return
            if await connect_btn.is_visible():
                await connect_btn.click()
            else:
                print("❌ Could not find 'Connect' button even in 'More' menu.")
                return

        # Handle Dialog
        dialog = self.profile.dialog()
        try:
            await dialog.wait_for(state="visible", timeout=5000)
        except:
             print("⚠️ No dialog appeared after clicking Connect.")
             return

        if note:
            add_note_btn = self.profile.add_note_button()
            if await add_note_btn.is_visible():
                await add_note_btn.click()
                # Fill text area
                await self.profile.message_input().fill(note)
                await self.page.wait_for_timeout(10000)
                await self.profile.send_button().click()
            else:
                print("⚠️ 'Add a note' button not found.")
        else:
            await self.page.wait_for_timeout(10000)
            send_without_note_btn = self.profile.send_without_note_button()
            if await send_without_note_btn.is_visible():
                await send_without_note_btn.click()
            else:
                print("⚠️ 'Send without a note' button not found.")

    async def withdraw_connection_request(self):
        connection_status = await self.get_connection_status()
        if connection_status != ConnectionStatus.PENDING:
            print("❌ Not in 'Pending' state, cannot withdraw connection request.")
            return
        
        pending_button = self.profile.pending_button()

        if await pending_button.is_visible():
            await self.page.wait_for_timeout(10000)
            await pending_button.click()
            await self.withdraw_connection_request_dialog()
        else:
            more_menu_button = self.profile.more_menu_button()
            await more_menu_button.click()
            try:
                await pending_button.wait_for(state="visible", timeout=5000)
            except:
                print("❌ Could not find 'Pending' button even in 'More' menu.")
                return
            if await pending_button.is_visible():
                self.page.wait_for_timeout(10000)
                await pending_button.click()
                await self.withdraw_connection_request_dialog()
            else:
                print("❌ Could not find 'Pending' button even in 'More' menu.")
                return
    
    async def withdraw_connection_request_dialog(self):
        dialog = self.profile.dialog()
        try:
            await dialog.wait_for(state="visible", timeout=5000)
        except:
             print("⚠️ No dialog appeared after clicking Connect.")
             return
        
        withdraw_button = self.profile.withdraw_button()
        if await withdraw_button.is_visible():
            await withdraw_button.click()
        else:
            print("❌ Could not find 'Withdraw' button.")