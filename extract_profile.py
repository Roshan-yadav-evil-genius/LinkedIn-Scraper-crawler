import json
import os
import glob
import traceback
import logging
from scrapy import Selector

from extractors.header import HeaderExtractor
from extractors.metrics import MetricsExtractor
from extractors.experience import ExperienceExtractor
from extractors.education import EducationExtractor
from extractors.section import SectionExtractor

print("Starting extract_profile.py...")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("extraction.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def extract_data_from_html(html_content):
    sel = Selector(text=html_content)
    data = {}

    # 1. Header (Name, Headline, Location, About)
    header_ext = HeaderExtractor(sel)
    data.update(header_ext.extract())

    # 2. Metrics (Followers, Connections)
    metrics_ext = MetricsExtractor(sel)
    data.update(metrics_ext.extract())

    # 3. Experience
    exp_ext = ExperienceExtractor(sel)
    data["experience"] = exp_ext.extract()

    # 4. Education
    edu_ext = EducationExtractor(sel)
    data["education"] = edu_ext.extract()

    # 5. Generic Sections (Skills, Projects, etc.)
    # We can reuse SectionExtractor for these straightforward lists
    section_ext = SectionExtractor(sel)

    # Skills - slightly special handling in original, but let's try generic first
    # Original extracted titles only.
    skills_data = section_ext.extract_section(["Skills"])
    data["skills"] = [s.get("title") for s in skills_data if s.get("title")]

    data["licenses_and_certifications"] = section_ext.extract_section(
        ["Licenses & certifications"]
    )
    data["volunteering"] = section_ext.extract_section(["Volunteering"])
    data["projects"] = section_ext.extract_section(["Projects"])
    data["honors_and_awards"] = section_ext.extract_section(["Honors & awards"])
    data["languages"] = section_ext.extract_section(["Languages"])
    data["publications"] = section_ext.extract_section(["Publications"])
    data["recommendations"] = section_ext.extract_section(["Recommendations"])

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
            error_msg = {
                "error": "No profile HTML files found in profiles/ directory or page.html"
            }
            print(json.dumps(error_msg))
            logger.error(error_msg["error"])
            return

    results = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        logger.info(f"Processing {file_name}...")
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
            logger.error(f"Failed to process {file_name}: {e}")
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

    logger.info("Extraction complete. Results saved to profile.json")


if __name__ == "__main__":
    main()
