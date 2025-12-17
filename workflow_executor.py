import asyncio
import sys
from playwright.async_api import async_playwright
from rich import print

from browser import launch_browser
from linkedin.pages import ProfilePage

async def main():
    async with async_playwright() as p:
        context = await launch_browser(p)
        
        # Create a new page or use the first one if available (persistent context often has one)
        page = await context.new_page()
        profile_url="https://www.linkedin.com/in/roshanyadavevilgenius/"
        
        workflow = ProfilePage(page=page,profile_url=profile_url)
        await workflow.execute()

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
