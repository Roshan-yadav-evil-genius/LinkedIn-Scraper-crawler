from scrapy import Selector
from typing import Optional, List, Dict, Any
from extractors.core.utils import clean_text, parse_int
from .selectors.profile import ProfileSelectors


class LinkedInProfileExtractor:
    """
    Single extractor class for LinkedIn profiles.
    Same pattern as automation's ProfilePage - one class, multiple methods.
    """

    def __init__(self, html: str):
        self.selector = Selector(text=html)
        self.selectors = ProfileSelectors(self.selector)

    # ═══════════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════════

    def extract(self) -> Dict[str, Any]:
        """Extract complete profile data."""
        data = {}

        # Header (name, headline, location)
        data.update(self.extract_header())

        # About
        data["about"] = self.extract_about()

        # Metrics (followers, connections)
        data.update(self.extract_metrics())

        # Experience
        data["experience"] = self.extract_experience()

        # Education
        data["education"] = self.extract_education()

        # Skills (just titles)
        data["skills"] = self.extract_skills()

        # Other sections
        data["licenses_and_certifications"] = self.extract_certifications()
        data["volunteering"] = self.extract_volunteering()
        data["projects"] = self.extract_projects()
        data["honors_and_awards"] = self.extract_honors()
        data["languages"] = self.extract_languages()
        data["publications"] = self.extract_publications()
        data["recommendations"] = self.extract_recommendations()

        return data

    # ═══════════════════════════════════════════════════════════════
    # HEADER EXTRACTION
    # ═══════════════════════════════════════════════════════════════

    def extract_header(self) -> Dict[str, str]:
        """Extract header: name, headline, location."""
        section = self.selectors.header_section()
        if not section:
            return {"name": "", "headline": "", "location": ""}

        return {
            "name": self._extract_first(self.selectors.name_xpaths(), section),
            "headline": self._extract_first(self.selectors.headline_xpaths(), section),
            "location": self._extract_first(self.selectors.location_xpaths(), section),
        }

    # ═══════════════════════════════════════════════════════════════
    # ABOUT EXTRACTION
    # ═══════════════════════════════════════════════════════════════

    def extract_about(self) -> str:
        """Extract about text from ABOUT_SECTION with global fallback."""
        # Try section-based extraction first
        section = self.selectors.about_section()
        if section:
            result = self._extract_first(self.selectors.about_xpaths(), section)
            if result:
                return result

        # Fallback: global search using original XPaths
        global_about_xpaths = [
            './/div[contains(@class, "inline-show-more-text")]//span[@aria-hidden="true"]/text()',
            '//div[contains(@class, "pv-about__summary-text")]//text()',
            '//*[@id="about"]//following-sibling::div//span[@aria-hidden="true"]/text()',
        ]
        return self._extract_first(global_about_xpaths, self.selector)

    # ═══════════════════════════════════════════════════════════════
    # METRICS EXTRACTION
    # ═══════════════════════════════════════════════════════════════

    def extract_metrics(self) -> Dict[str, int]:
        """Extract follower/connection counts."""
        followers_raw = self._extract_first(
            self.selectors.followers_xpaths(), self.selector
        )
        connections_raw = self._extract_first(
            self.selectors.connections_xpaths(), self.selector
        )

        return {
            "followers": parse_int(followers_raw),
            "connections": parse_int(connections_raw),
        }

    # ═══════════════════════════════════════════════════════════════
    # SECTION EXTRACTORS
    # ═══════════════════════════════════════════════════════════════

    def extract_experience(self) -> List[Dict[str, Any]]:
        """Extract work experience."""
        section = self.selectors.experience_section()
        return self._extract_section_items(section)

    def extract_education(self) -> List[Dict[str, Any]]:
        """Extract education history."""
        section = self.selectors.education_section()
        return self._extract_section_items(section)

    def extract_skills(self) -> List[str]:
        """Extract skills as a flat list of titles."""
        section = self.selectors.skills_section()
        items = self._extract_section_items(section)
        return [item["title"] for item in items if item.get("title")]

    def extract_certifications(self) -> List[Dict[str, Any]]:
        """Extract licenses and certifications."""
        section = self.selectors.certifications_section()
        return self._extract_section_items(section)

    def extract_volunteering(self) -> List[Dict[str, Any]]:
        """Extract volunteering experience."""
        section = self.selectors.volunteering_section()
        return self._extract_section_items(section)

    def extract_projects(self) -> List[Dict[str, Any]]:
        """Extract projects."""
        section = self.selectors.projects_section()
        return self._extract_section_items(section)

    def extract_honors(self) -> List[Dict[str, Any]]:
        """Extract honors and awards."""
        section = self.selectors.honors_section()
        return self._extract_section_items(section)

    def extract_languages(self) -> List[Dict[str, Any]]:
        """Extract languages."""
        section = self.selectors.languages_section()
        return self._extract_section_items(section)

    def extract_publications(self) -> List[Dict[str, Any]]:
        """Extract publications."""
        section = self.selectors.publications_section()
        return self._extract_section_items(section)

    def extract_recommendations(self) -> List[Dict[str, Any]]:
        """Extract recommendations."""
        section = self.selectors.recommendations_section()
        return self._extract_section_items(section)

    # ═══════════════════════════════════════════════════════════════
    # PRIVATE HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _extract_section_items(
        self, section: Optional[Selector]
    ) -> List[Dict[str, Any]]:
        """Extract list items from a section."""
        if section is None:
            return []

        items = []
        list_item_xpaths = self.selectors.list_item_xpaths()

        # Find all list items within the section
        item_nodes = []
        for xpath in list_item_xpaths:
            item_nodes = section.xpath(xpath)
            if item_nodes:
                break

        for node in item_nodes:
            entry = self._extract_item(node)
            items.append(entry)

        return items

    def _extract_item(self, item: Selector) -> Dict[str, Any]:
        """Extract fields from a list item."""
        entry = {}

        # Title
        entry["title"] = self._extract_first(
            self.selectors.item_title_xpaths(), item
        )

        # Subtitle
        entry["subtitle"] = self._extract_first(
            self.selectors.item_subtitle_xpaths(), item
        )

        # Meta fields (dates, locations, etc.)
        meta_vals = self._extract_all(self.selectors.item_meta_xpaths(), item)
        for i, val in enumerate(meta_vals):
            entry[f"meta_{i + 1}"] = val

        return entry

    def _extract_first(self, xpaths: List[str], context: Selector) -> str:
        """Try XPaths, return first match."""
        for xpath in xpaths:
            val = context.xpath(xpath).get()
            if val:
                cleaned = clean_text(val)
                if cleaned:
                    return cleaned
        return ""

    def _extract_all(self, xpaths: List[str], context: Selector) -> List[str]:
        """Try XPaths, return all matches from first successful."""
        for xpath in xpaths:
            vals = context.xpath(xpath).getall()
            if vals:
                return [clean_text(v) for v in vals if clean_text(v)]
        return []

