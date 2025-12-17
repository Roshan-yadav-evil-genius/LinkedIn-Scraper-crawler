import json
import os
import glob
import traceback
import logging

from extractors import LinkedInProfileExtractor

print("Starting extract_profile.py...")

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
    extractor = LinkedInProfileExtractor(html_content)
    return extractor.extract()


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
