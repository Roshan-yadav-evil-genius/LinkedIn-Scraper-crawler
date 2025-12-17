import asyncio
import sys
import logging
from playwright.async_api import async_playwright

from browser import launch_browser
from automation.linkedin.profile_page import ProfilePage

logger = logging.getLogger(__name__)


async def main():
    async with async_playwright() as p:
        context = await launch_browser(p)

        # Create a new page or use the first one if available (persistent context often has one)
        page = await context.new_page()
        profile_url = "https://www.linkedin.com/in/roshanyadavevilgenius/"

        logger.info("Starting workflow for profile: %s", profile_url)

        user_profile = ProfilePage(page=page, profile_url=profile_url)
        await user_profile.load()
        # await user_profile.send_connection_request(note="")
        await user_profile.unfollow_profile()
        # await user_profile.withdraw_connection_request()
        # await user_profile.follow_profile()

        logger.info("Workflow completed successfully")

        # Keep open for manual interaction as requested in the original script
        await page.wait_for_event("close", timeout=0)
        logger.debug("Closing browser context")
        await context.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("Workflow interrupted by user")
