import json
from scrapy import Selector


def extract_profile():
    try:
        with open("page.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(json.dumps({"error": "page.html not found"}))
        return

    sel = Selector(text=html_content)

    data = {}

    # 1. Name
    data["name"] = (
        sel.xpath('//h1[contains(@class, "text-heading-xlarge")]/text()')
        .get(default="")
        .strip()
    )
    if not data["name"]:
        data["name"] = sel.xpath("//h1//text()").get(default="").strip()

    # 2. Headline
    data["headline"] = (
        sel.xpath(
            '//div[contains(@class, "text-body-medium") and contains(@class, "break-words")]/text()'
        )
        .get(default="")
        .strip()
    )

    # 3. Location
    data["location"] = (
        sel.xpath(
            '//span[contains(@class, "text-body-small") and contains(@class, "inline") and contains(@class, "break-words")]/text()'
        )
        .get(default="")
        .strip()
    )

    # 3.5 Followers and Connections
    # They are usually in a list ul.pv-top-card--list-bullet > li
    # We look for text that contains 'followers' or 'connections'

    # Followers
    followers_text = sel.xpath('//li//span[contains(text(), "followers")]/text()').get()
    # Sometimes it's inside a span that is inside the li
    if not followers_text:
        followers_text = sel.xpath(
            '//*[contains(@class, "t-bold") and contains(text(), "followers")]/text()'
        ).get()

    data["followers"] = followers_text.strip() if followers_text else ""

    # Connections
    # Debug showed: <span class="t-black--light"> <span class="t-bold">500+</span> connections </span>
    # Or similar structure.
    # Let's try to grab the t-bold that specifically has a number or "500+" and check parent

    # Text is "500+"
    conn_count = sel.xpath(
        '//span[contains(@class, "t-bold") and contains(text(), "500+")]/text()'
    ).get()

    if conn_count:
        data["connections"] = f"{conn_count} connections"
    else:
        # Fallback if "500+" is not the case
        text_match = sel.xpath('//span[contains(text(), "connections")]/text()').get()
        data["connections"] = text_match.strip() if text_match else ""

    # Helper function to finding section by header text
    def get_section_by_header(header_text):
        # Look for the header text inside an H2 or similar container roughly
        # We look for any text node containing the header_text that is inside an element that looks like a header (e.g., inside 'pvs-header' or just H2)
        # Using a broad search for the text within an id='...' or class='...' context is safer.

        # Try finding the specific section by ID first (most reliable)
        section_id_map = {
            "About": "about",
            "Experience": "experience",
            "Education": "education",
            "Skills": "skills",
            "Interests": "interests",
        }

        target_id = section_id_map.get(header_text)
        if target_id:
            # Look for element with this id
            anchor = sel.xpath(f'//*[@id="{target_id}"]')
            if anchor:
                return anchor.xpath("./ancestor::section[1]")

        # Fallback: Search by visual text in H2
        # Use translate to be case insensitive if needed, but usually capitalized
        # //h2//span[contains(text(), ...)]
        header = sel.xpath(f'//h2//*[contains(text(), "{header_text}")]')
        if header:
            return header[0].xpath("./ancestor::section[1]")

        return None

    # 4. About
    about_section = get_section_by_header("About")
    if about_section:
        # Standard location for text in About section
        texts = about_section.xpath(
            './/div[contains(@class, "inline-show-more-text")]//span[@aria-hidden="true"]/text()'
        ).getall()
        if not texts:
            # Try getting all text in the show-more text div
            texts = about_section.xpath(
                './/div[contains(@class, "inline-show-more-text")]//text()'
            ).getall()

        data["about"] = " ".join([t.strip() for t in texts if t.strip()])
    else:
        # Try finding the summary text directly if section not found via header
        summary_text = sel.xpath(
            '//div[contains(@class, "pv-about__summary-text")]//text()'
        ).getall()
        if summary_text:
            data["about"] = "".join(summary_text).strip()
        else:
            data["about"] = ""

    # Helper to parse list items
    def parse_list_items(section):
        results = []
        if not section:
            return results

        items = section.xpath('.//li[contains(@class, "artdeco-list__item")]')
        for item in items:
            # Extract distinct text blocks (aria-hidden=true for display)
            texts = item.xpath('.//span[@aria-hidden="true"]/text()').getall()
            texts = [t.strip() for t in texts if t.strip()]

            entry = {}
            # Maps first few text items to fields. Structure varies but first is usually Title/School.
            if len(texts) >= 1:
                entry["title"] = texts[0]
            if len(texts) >= 2:
                entry["subtitle"] = texts[1]
            if len(texts) >= 3:
                entry["meta_1"] = texts[2]
            if len(texts) >= 4:
                entry["meta_2"] = texts[3]

            results.append(entry)
        return results

    # 5. Experience
    exp_section = get_section_by_header("Experience")
    data["experience"] = parse_list_items(exp_section)

    # 6. Education
    edu_section = get_section_by_header("Education")
    data["education"] = parse_list_items(edu_section)

    # 7. Skills
    skills_section = get_section_by_header("Skills")
    if skills_section:
        # Skills list usually just has titles in the list items
        skills_data = parse_list_items(skills_section)
        # Extract just the title part
        data["skills"] = [s.get("title") for s in skills_data if s.get("title")]
    else:
        data["skills"] = []

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    extract_profile()
