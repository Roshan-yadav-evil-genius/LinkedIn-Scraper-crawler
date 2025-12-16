from playwright.async_api import Page, Locator
from .selector.profile_page import ProfilePageKey, PROFILE_PAGE_SELECTORS
from linkedin.pages.base_page import BasePage

class LinkedInProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, PROFILE_PAGE_SELECTORS)

    def action_bar(self) -> Locator:
        return self._get_locator(ProfilePageKey.ACTION_BAR)

    def visible_buttons(self) -> Locator:
        return self.action_bar().locator("button")

    def more_menu_trigger(self) -> Locator:
        return self._get_locator(ProfilePageKey.MORE_MENU_TRIGGER).first

    def connect_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.CONNECT_BUTTON)
    
    def pending_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.PENDING_BUTTON)

    def message_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.MESSAGE_BUTTON)
    
    def follow_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.FOLLOW_BUTTON)
    
    def following_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.FOLLOWING_BUTTON)

    def unfollow_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.UNFOLLOW_BUTTON)
    
    def remove_connection_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.REMOVE_CONNECTION_BUTTON)

    def dialog(self) -> Locator:
        return self._get_locator(ProfilePageKey.DIALOG).first

    def add_note_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.ADD_NOTE_BUTTON)

    def send_without_note_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.SEND_WITHOUT_NOTE_BUTTON)
    
    def send_button(self) -> Locator:
        return self._get_locator(ProfilePageKey.SEND_BUTTON)
    
    def message_input(self) -> Locator:
        return self._get_locator(ProfilePageKey.MESSAGE_INPUT)

