import asyncio
import logging
from playwright.async_api import async_playwright, BrowserContext
from browser import launch_browser

logger = logging.getLogger(__name__)


async def parse_linkedin_profile(context: BrowserContext):
    profile_url = "https://www.linkedin.com/in/roshan-yadav-4631272a8/"
    output_path = "bin/profiles/profile9.html"

    logger.debug("Creating new page for profile parsing")
    page1 = await context.new_page()

    logger.debug("Navigating to profile: %s", profile_url)
    await page1.goto(profile_url)
    await page1.wait_for_timeout(5000)

    page_html = await page1.content()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page_html)

    logger.info("Page saved to %s", output_path)


async def main():
    async with async_playwright() as p:
        context = await launch_browser(p)

        logger.info("Running LinkedIn profile parser")
        await parse_linkedin_profile(context)
        logger.info("Browser ready for manual interaction")

        try:
            await context.wait_for_event("close", timeout=0)
        except KeyboardInterrupt:
            logger.warning("Script interrupted by user")
        finally:
            logger.debug("Closing browser context")
            await context.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
