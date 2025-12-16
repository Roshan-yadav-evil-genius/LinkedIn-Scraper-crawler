from playwright.async_api import Page, Locator
from .registries.profile_page_registry import PROFILE_PAGE_SELECTORS
from linkedin.pages.base_page import BasePage

class LinkedInProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, PROFILE_PAGE_SELECTORS)

    def action_bar(self) -> Locator:
        return self._get_locator("action_bar")

    def visible_buttons(self) -> Locator:
        # This one is tricky as it depends on action_bar. 
        # We can just assume action_bar locator works and append ' button'.
        # Or define it in registry. Let's keep it relative for now.
        return self.action_bar().locator("button")

    def more_menu_trigger(self) -> Locator:
        return self._get_locator("more_menu_trigger").first

    def connect_button(self) -> Locator:
        return self._get_locator("connect_button")
    
    def pending_button(self) -> Locator:
        return self._get_locator("pending_button")

    def message_button(self) -> Locator:
        return self._get_locator("message_button")
    
    def follow_button(self) -> Locator:
        return self._get_locator("follow_button")
    
    def following_button(self) -> Locator:
        return self._get_locator("following_button")

    def unfollow_button(self) -> Locator:
        return self._get_locator("unfollow_button")
    
    def remove_connection_button(self) -> Locator:
        return self._get_locator("remove_connection_button")

    def dialog(self) -> Locator:
        return self._get_locator("dialog").first

    def add_note_button(self) -> Locator:
        return self._get_locator("add_note_button")

    def send_without_note_button(self) -> Locator:
        return self._get_locator("send_without_note_button")
    
    def send_button(self) -> Locator:
        return self._get_locator("send_button")
    
    def message_input(self) -> Locator:
        return self._get_locator("message_input")

