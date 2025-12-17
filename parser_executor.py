import json
import os
import glob
import traceback
import logging

from extractors import LinkedInProfileExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def extract_data_from_html(html_content: str) -> dict:
    """
    Extract profile data from HTML content.
    Uses the new unified LinkedInProfileExtractor.
    """
    logger.debug("Extracting data from HTML content (%d bytes)", len(html_content))
    extractor = LinkedInProfileExtractor(html_content)
    return extractor.extract()


def main():
    logger.info("Starting profile extraction")

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
            logger.debug("Using fallback page.html")
        else:
            logger.error("No profile HTML files found in profiles/ directory or page.html")
            return

    logger.info("Found %d HTML files to process", len(files))

    results = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        logger.debug("Processing file: %s", file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            extracted_data = extract_data_from_html(content)
            results.append(
                {"filename": file_name, "status": "success", "data": extracted_data}
            )
            logger.info("Successfully processed %s", file_name)
        except Exception as e:
            # Capture traceback for debugging
            tb = traceback.format_exc()
            logger.error("Failed to process %s: %s", file_name, e)
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
