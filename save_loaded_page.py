import asyncio
from playwright.async_api import async_playwright, BrowserContext
from browser import launch_browser


async def parse_linkedin_profile(context: BrowserContext):
    page1 = await context.new_page()
    await page1.goto("https://www.linkedin.com/in/roshan-yadav-4631272a8/")
    await page1.wait_for_timeout(5000)
    page_html = await page1.content()
    with open("profiles/profile9.html", "w", encoding="utf-8") as f:
        f.write(page_html)


async def main():
    async with async_playwright() as p:
        context = await launch_browser(p)

        print("🔄 Running parser...")
        await parse_linkedin_profile(context)
        print("✅ Manual browser is open. You can browse freely.")

        try:
            await context.wait_for_event("close", timeout=0)
        except KeyboardInterrupt:
            print("🛑 Script interrupted.")
        finally:
            print("🔒 Closing context...")
            await context.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
