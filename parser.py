from playwright.async_api import BrowserContext


async def parse_linkedin_profile(context: BrowserContext):
    page1 = await context.new_page()
    await page1.goto("https://www.linkedin.com/in/dr-ds-chauhan-70690b49/")
    await page1.wait_for_timeout(5000)
    page_html = await page1.content()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page_html)
