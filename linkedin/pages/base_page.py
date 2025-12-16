from playwright.async_api import Page, Locator

class BasePage:
    def __init__(self, page: Page, registry: dict):
        self.page = page
        self.registry = registry

    def _get_locator(self, key: str) -> Locator:
        """
        Defensively tries to find a locator based on the registry list.
        Returns a Locator that represents the consolidation of all strategies 
        (using .or_()) logic or the first primary one if just one exists.
        
        Since we want 'visibility' checks to succeed if ANY of them are visible, 
        using .or_() is the most Playwright-native way.
        """
        strategies = self.registry.get(key, [])
        if not strategies:
            # Fallback to an empty locator that will likely fail if used, or raise error
            raise ValueError(f"No selector found in registry for key: {key}")

        first_selector = strategies[0]
        locator = self._create_single_locator(first_selector)

        # Chain subsequent selectors with OR to allow robustness
        for selector in strategies[1:]:
            locator = locator.or_(self._create_single_locator(selector))
        
        return locator

    def _create_single_locator(self, selector_def) -> Locator:
        """Helper to parse registry item (only supports strings/XPaths now)"""
        if isinstance(selector_def, str):
            return self.page.locator(selector_def)
        
        raise ValueError(f"Strict XPath mode: Selector must be a string, got {type(selector_def)}: {selector_def}")
