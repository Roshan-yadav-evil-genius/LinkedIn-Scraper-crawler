import asyncio
import sys
from playwright.async_api import async_playwright
from rich import print

from browser import launch_browser
from automation.linkedin.profile_page import ProfilePage

async def main():
    async with async_playwright() as p:
        context = await launch_browser(p)
        
        # Create a new page or use the first one if available (persistent context often has one)
        page = await context.new_page()
        profile_url="https://www.linkedin.com/in/roshanyadavevilgenius/"
        
        user_profile = ProfilePage(page=page,profile_url=profile_url)
        await user_profile.load()
        # await user_profile.send_connection_request(note="")
        await user_profile.unfollow_profile()
        # await user_profile.withdraw_connection_request()
        # await user_profile.follow_profile()

        print("✅ Workflow completed.")
        
        # Keep open for manual interaction as requested in the original script
        await page.wait_for_event("close", timeout=0)
        print("🔒 Closing context...")
        await context.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
