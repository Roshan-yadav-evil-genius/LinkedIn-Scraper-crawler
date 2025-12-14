import json
import os
import glob
import sys
import traceback
from scrapy import Selector


def extract_data_from_html(html_content):
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
    # Followers
    followers_text = sel.xpath('//li//span[contains(text(), "followers")]/text()').get()
    if not followers_text:
        followers_text = sel.xpath(
            '//*[contains(@class, "t-bold") and contains(text(), "followers")]/text()'
        ).get()
    data["followers"] = followers_text.strip() if followers_text else ""

    # Connections
    conn_count = sel.xpath(
        '//span[contains(@class, "t-bold") and contains(text(), "500+")]/text()'
    ).get()

    if conn_count:
        data["connections"] = f"{conn_count} connections"
    else:
        text_match = sel.xpath('//span[contains(text(), "connections")]/text()').get()
        data["connections"] = text_match.strip() if text_match else ""

    # Helper function to finding section by header text
    def get_section_by_header(header_text):
        section_id_map = {
            "About": "about",
            "Experience": "experience",
            "Education": "education",
            "Skills": "skills",
            "Interests": "interests",
            "Licenses & certifications": "licenses_and_certifications",
            "Volunteering": "volunteering_experience",
            "Projects": "projects",
            "Honors & awards": "honors_and_awards",
            "Languages": "languages",
            "Publications": "publications",
            "Recommendations": "recommendations",
        }
        target_id = section_id_map.get(header_text)
        if target_id:
            anchor = sel.xpath(f'//*[@id="{target_id}"]')
            if anchor:
                return anchor.xpath("./ancestor::section[1]")

        header = sel.xpath(f'//h2//*[contains(text(), "{header_text}")]')
        if header:
            return header[0].xpath("./ancestor::section[1]")
        return None

    # 4. About
    about_section = get_section_by_header("About")
    if about_section:
        texts = about_section.xpath(
            './/div[contains(@class, "inline-show-more-text")]//span[@aria-hidden="true"]/text()'
        ).getall()
        if not texts:
            texts = about_section.xpath(
                './/div[contains(@class, "inline-show-more-text")]//text()'
            ).getall()
        data["about"] = " ".join([t.strip() for t in texts if t.strip()])
    else:
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
            texts = item.xpath('.//span[@aria-hidden="true"]/text()').getall()
            texts = [t.strip() for t in texts if t.strip()]

            entry = {}
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
        skills_data = parse_list_items(skills_section)
        data["skills"] = [s.get("title") for s in skills_data if s.get("title")]
    else:
        data["skills"] = []

    # 8. Licenses & certifications
    licenses_section = get_section_by_header("Licenses & certifications")
    data["licenses_and_certifications"] = parse_list_items(licenses_section)

    # 9. Volunteering
    vol_section = get_section_by_header("Volunteering")
    data["volunteering"] = parse_list_items(vol_section)

    # 10. Projects
    projects_section = get_section_by_header("Projects")
    data["projects"] = parse_list_items(projects_section)

    # 11. Honors & awards
    honors_section = get_section_by_header("Honors & awards")
    data["honors_and_awards"] = parse_list_items(honors_section)

    # 12. Languages
    languages_section = get_section_by_header("Languages")
    data["languages"] = parse_list_items(languages_section)

    # 13. Publications
    publications_section = get_section_by_header("Publications")
    data["publications"] = parse_list_items(publications_section)

    # 14. Recommendations
    # Recommendations structure is often specialized (Received/Given tabs), but list items might still work if present in DOM
    recommendations_section = get_section_by_header("Recommendations")
    data["recommendations"] = parse_list_items(recommendations_section)

    return data


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_dir = os.path.join(base_dir, "profiles")
    pattern = os.path.join(profiles_dir, "*.html")
    files = glob.glob(pattern)

    # Sort files to ensure deterministic order
    files.sort()

    if not files:
        # Fallback to local page.html
        page_path = os.path.join(base_dir, "page.html")
        if os.path.exists(page_path):
            files = [page_path]
        else:
            print(
                json.dumps(
                    {
                        "error": "No profile HTML files found in profiles/ directory or page.html"
                    }
                )
            )
            return

    results = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            extracted_data = extract_data_from_html(content)
            results.append(
                {"filename": file_name, "status": "success", "data": extracted_data}
            )
        except Exception as e:
            # Capture traceback for debugging
            tb = traceback.format_exc()
            results.append(
                {
                    "filename": file_name,
                    "status": "error",
                    "error": str(e),
                    "traceback": tb,
                }
            )

    with open("profile.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
