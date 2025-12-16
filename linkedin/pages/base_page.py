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
        """Helper to parse registry item (dict vs string)"""
        if isinstance(selector_def, dict):
            # It's a role-based selector definition, e.g. {"role": "button", "name": "Connect"}
            if "role" in selector_def:
                return self.page.get_by_role(selector_def["role"], name=selector_def.get("name"))
            # Can expand to get_by_label, get_by_text if needed
            elif "text" in selector_def:
                return self.page.get_by_text(selector_def["text"])
        elif isinstance(selector_def, str):
            # Assume it's an XPath or CSS selector
            return self.page.locator(selector_def)
        
        raise ValueError(f"Unknown selector definition: {selector_def}")
