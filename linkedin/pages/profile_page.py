from playwright.async_api import Page, Locator

class LinkedInProfilePage:
    def __init__(self, page: Page):
        self.page = page

    def action_bar(self) -> Locator:
        """
        Locates the action bar section containing the Connect/Message/More buttons.
        """
        return self.page.locator(
            "(//section[contains(@class,'artdeco-card')])[1]"
            "//ul[.//li[contains(normalize-space(.),'connections')]]"
            "/following-sibling::*[1]"
        )

    def visible_buttons(self) -> Locator:
        """
        Returns all button elements within the action bar.
        """
        return self.action_bar().locator("button")

    def more_menu_trigger(self) -> Locator:
        """
        Returns the 'More' menu trigger button (usually an icon or logic relies on aria-label/text).
        Often has artdeco-button--secondary or similar, but the user's xpath was specific.
        Using the user's xpath logic:
        """
        return self.action_bar().locator("//div[@role='button' or @type='button'][.//span[contains(text(), 'More')]] | //button[contains(@aria-label, 'More')]").first

    def connect_button(self) -> Locator:
        return self.page.get_by_role("button", name="Connect")
    
    def pending_button(self) -> Locator:
        return self.page.get_by_role("button", name="Pending")

    def message_button(self) -> Locator:
        return self.page.get_by_role("button", name="Message")
    
    def follow_button(self) -> Locator:
         return self.page.get_by_role("button", name="Follow")
    
    def following_button(self) -> Locator:
         return self.page.get_by_role("button", name="Following")

    def unfollow_button(self) -> Locator:
        # Usually inside a menu, so might need handling
        return self.page.get_by_role("button", name="Unfollow")
    
    def remove_connection_button(self) -> Locator:
        # Inside menu
        return self.page.get_by_role("button", name="Remove connection")

    def dialog(self) -> Locator:
        return self.page.locator("div[role='dialog']").first

    def add_note_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add a note")

    def send_without_note_button(self) -> Locator:
        return self.page.get_by_role("button", name="Send without a note")
    
    def send_button(self) -> Locator:
        # After adding a note, the button might just be "Send"
        return self.page.get_by_role("button", name="Send")
