from scrapy import Selector
from typing import Optional, List, Union
from enum import Enum


class BaseSelector:
    """
    Base class for selector resolution with parent hierarchy.
    Same pattern as automation's BasePage.
    """

    def __init__(self, selector: Selector, registry: dict):
        self.selector = selector
        self.registry = registry
        self._cache: dict = {}

    def get(self, key: Enum) -> List[str]:
        """
        Get XPath list for a key.

        Args:
            key: Enum key from registry

        Returns:
            List of XPath strings
        """
        entry = self.registry.get(key)
        if not entry:
            raise ValueError(f"No selector found for key: {key}")

        selectors = entry.get("selectors", [])
        # Handle case where selectors is a single string (for simple xpaths like section root)
        if isinstance(selectors, str):
            return [selectors]
        return selectors

    def resolve(self, key: Enum) -> Optional[Selector]:
        """
        Resolve a key to a Selector, following parent hierarchy.
        Same pattern as automation's BasePage.get()

        Returns the first matching Selector, or None.
        """
        # Check cache
        if key in self._cache:
            return self._cache[key]

        entry = self.registry.get(key)
        if not entry:
            raise ValueError(f"No selector found for key: {key}")

        selectors = entry.get("selectors", [])
        parent_key = entry.get("parent")

        # Handle single string selector
        if isinstance(selectors, str):
            selectors = [selectors]

        # Determine base: parent selector or document root
        if parent_key is not None:
            base = self.resolve(parent_key)  # Recursive resolution
            if base is None:
                return None
        else:
            base = self.selector

        # Try each XPath until one works
        for xpath in selectors:
            result = base.xpath(xpath)
            if result:
                # Cache and return first match
                resolved = result[0] if len(result) == 1 else result[0]
                self._cache[key] = resolved
                return resolved

        return None

    def resolve_all(self, key: Enum) -> List[Selector]:
        """
        Resolve a key to all matching Selectors.
        """
        entry = self.registry.get(key)
        if not entry:
            raise ValueError(f"No selector found for key: {key}")

        selectors = entry.get("selectors", [])
        parent_key = entry.get("parent")

        # Handle single string selector
        if isinstance(selectors, str):
            selectors = [selectors]

        # Determine base
        if parent_key is not None:
            base = self.resolve(parent_key)
            if base is None:
                return []
        else:
            base = self.selector

        # Try each XPath until one works
        for xpath in selectors:
            result = base.xpath(xpath)
            if result:
                return list(result)

        return []

    def clear_cache(self):
        """Clear the selector cache."""
        self._cache.clear()
