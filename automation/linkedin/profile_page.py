from playwright.async_api import Page, Locator
from rich import print
from .selectors.profile_page import LinkedInProfilePageSelectors
from urllib.parse import urlparse
from enum import Enum

class ConnectionStatus(Enum):
    NOT_CONNECTED = "not_connected"
    CONNECTED = "connected"
    PENDING = "pending"

class FollowingStatus(Enum):
    NOT_FOLLOWING = "not_following"
    FOLLOWING = "following"


class ProfilePage:
    def __init__(self, page: Page, profile_url: str):
        self.page = page
    
        if not self._is_valid_linkedin_profile_url(profile_url):
            raise ValueError("Invalid LinkedIn profile URL.")
        
        self.profile_url = profile_url
        self.profile = LinkedInProfilePageSelectors(self.page)


    # ─────────────────────────────────────────────────────────────
    # Public Methods
    # ─────────────────────────────────────────────────────────────


    async def load(self):
        await self.page.goto(self.profile_url, wait_until="load")
    
    
    async def follow_profile(self):
        following_status = await self._get_following_status()

        if following_status == FollowingStatus.NOT_FOLLOWING:
            print("🚀 Following profile...")
            follow_btn = self.profile.follow_button()
            await self._click_or_expand_more_menu(follow_btn, "Follow")
        else:
            print("✨ Already following.")
    

    async def unfollow_profile(self):
        following_status = await self._get_following_status()
        print(f"Following Status: {following_status}")
        if following_status == FollowingStatus.FOLLOWING:
            print("🚀 Unfollowing profile...")
            unfollow_btn = self.profile.unfollow_button()
            await self._click_or_expand_more_menu(unfollow_btn, "Unfollow")

            dialog = await self._wait_for_dialog("clicking Pending")
            if not dialog:
                return
            confirm_unfollow_btn = self.profile.dialog_unfollow_button()
            if await confirm_unfollow_btn.is_visible():
                await confirm_unfollow_btn.click()
        else:
            print("✨ Already unfollowing.")
    

    async def send_connection_request(self,note:str=""):
        connection_status = await self._get_connection_status()

        print(f"Connection Status: {connection_status}")

        if connection_status == ConnectionStatus.NOT_CONNECTED:
            await self._send_connection_request(note)
        
        print("Connection request sent successfully.")


    async def withdraw_connection_request(self):
        connection_status = await self._get_connection_status()
        if connection_status != ConnectionStatus.PENDING:
            print("❌ Not in 'Pending' state, cannot withdraw connection request.")
            return
        
        pending_btn = self.profile.pending_button()
        
        await self.page.wait_for_timeout(10000)
        
        if not await self._click_or_expand_more_menu(pending_btn, "Pending"):
            return
        
        dialog = await self._wait_for_dialog("clicking Pending")
        if not dialog:
            return
        
        withdraw_btn = self.profile.withdraw_button()
        if await withdraw_btn.is_visible():
            await withdraw_btn.click()
        else:
            print("❌ Could not find 'Withdraw' button.")

    
    # ─────────────────────────────────────────────────────────────
    # Private Methods
    # ─────────────────────────────────────────────────────────────

    async def _send_connection_request(self, note: str = ""):
        connect_btn = self.profile.connect_button()
        
        if not await self._click_or_expand_more_menu(connect_btn, "Connect"):
            return

        dialog = await self._wait_for_dialog("clicking Connect")
        if not dialog:
            print("❌ Connection dialog did not appear.")
            return

        if note:
            add_note_btn = self.profile.add_note_button()
            if await add_note_btn.is_visible():
                await add_note_btn.click()
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

    @staticmethod
    def _is_valid_linkedin_profile_url(profile_url: str) -> bool:
        # EX: https://www.linkedin.com/in/zackspear/

        parsed = urlparse(profile_url)

        if parsed.scheme != "https":
            return False

        if parsed.netloc.lower() != "www.linkedin.com":
            return False

        paths = [p for p in parsed.path.strip("/").split("/") if p]

        return len(paths) == 2 and paths[0] == "in"


    async def _click_or_expand_more_menu(self, button: Locator, button_name: str) -> bool:
        """
        Click button directly, or expand More menu first if needed.
        
        Returns:
            True if button was clicked successfully, False otherwise.
        """
        if await button.is_visible():
            await button.click()
            return True
        
        print(f"⚠️ '{button_name}' not visible, checking 'More' menu...")
        await self.profile.more_menu_button().click()
        
        try:
            await button.wait_for(state="visible", timeout=5000)
            await button.click()
            return True
        except:
            print(f"❌ Could not find '{button_name}' even in 'More' menu.")
            return False


    async def _wait_for_dialog(self, context: str = "action") -> Locator | None:
        """
        Wait for dialog to appear.
        
        Args:
            context: Description of what triggered the dialog (for error message)
            
        Returns:
            Dialog locator if found, None otherwise.
        """
        dialog = self.profile.dialog()
        try:
            await dialog.wait_for(state="visible", timeout=5000)
            return dialog
        except:
            print(f"⚠️ No dialog appeared after {context}.")
            return None


    async def _get_connection_status(self) -> ConnectionStatus:
        if await self.profile.connect_button().count():
            return ConnectionStatus.NOT_CONNECTED
        
        if await self.profile.pending_button().count():
            return ConnectionStatus.PENDING

        return ConnectionStatus.CONNECTED

    async def _get_following_status(self) -> FollowingStatus:
        if await self.profile.follow_button().count():
            return FollowingStatus.NOT_FOLLOWING
        return FollowingStatus.FOLLOWING
