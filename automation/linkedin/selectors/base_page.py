from playwright.async_api import Page, Locator
from typing import Union
from enum import Enum


class BasePage:
    def __init__(self, page: Page, registry: dict):
        self.page = page
        self.registry = registry
        self._locator_cache: dict = {}

    def get(self, key: Enum) -> Locator:
        """
        Unified method to get a locator by key.
        Automatically resolves parent hierarchy from the registry.
        
        Args:
            key: Enum key from the registry (e.g., ProfilePageKey.CONNECT_BUTTON)
            
        Returns:
            Locator with all fallback selectors chained via .or_()
        """
        # Check cache first
        if key in self._locator_cache:
            return self._locator_cache[key]
        
        entry = self.registry.get(key)
        if not entry:
            raise ValueError(f"No selector found in registry for key: {key}")
        
        selectors = entry.get("selectors", [])
        parent_key = entry.get("parent")
        
        if not selectors:
            raise ValueError(f"No selectors defined for key: {key}")
        
        # Determine base: parent locator or page
        if parent_key is not None:
            base = self.get(parent_key)  # Recursive resolution
        else:
            base = self.page
        
        # Build locator with .or_() chaining
        locator = base.locator(selectors[0])
        for selector in selectors[1:]:
            locator = locator.or_(base.locator(selector))
        
        # Cache and return
        self._locator_cache[key] = locator
        return locator

    def clear_cache(self):
        """Clear the locator cache. Call after navigation if needed."""
        self._locator_cache.clear()
