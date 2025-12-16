import asyncio
import sys
from playwright.async_api import async_playwright
from rich import print

from linkedin.browser import launch_browser
from linkedin.operations.profile_page import ProfilePageOperations

async def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    async with async_playwright() as p:
        context = await launch_browser(p)
        
        try:
            # Create a new page or use the first one if available (persistent context often has one)
            if context.pages:
                page = context.pages[0]
            else:
                page = await context.new_page()

            print("🔄 Navigating to LinkedIn profile...")
            # Use the URL from the original script or config
            await page.goto("https://www.linkedin.com/in/roshanyadavevilgenius/", wait_until="domcontentloaded")

            # Check for login requirement (could be a separate check or part of workflow)
            # For brevity, assuming we are logged in or can handle it manually if the persistent context is good.
            # Ideally, we'd have a LoginWorkflow or check here.
            
            workflow = ProfilePageOperations(page)
            await workflow.execute()

            print("✅ Workflow completed.")
            print("   Close the browser window to exit.")
            
            # Keep open for manual interaction as requested in the original script
            await page.wait_for_event("close", timeout=0)

        except Exception as e:
            print(f"🛑 Error: {e}")
        finally:
            print("🔒 Closing context...")
            await context.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
