from playwright.async_api import async_playwright, BrowserContext, Playwright
import tomllib
import sys
import os

def load_config():
    try:
        # Assuming config.toml is in the root of the workspace (parent of linkedin package)
        # Adjust path if necessary
        with open( "config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("❌ Error: 'config.toml' not found.")
        sys.exit(1)

async def launch_browser(p: Playwright) -> BrowserContext:
    config = load_config()
    browser_config = config.get("browser", {})
    context_config = config.get("context", {})

    print("🚀 Launching browser...")
    args = browser_config.get("args", [])

    # Ensure user_data_dir is absolute or relative to CWD correctly
    user_data_path = context_config.get("user_data_dir", "./chrome_user_data1")

    context = await p.chromium.launch_persistent_context(
        user_data_dir=user_data_path,
        headless=browser_config.get("headless", False),
        args=args,
        user_agent=context_config.get("user_agent"),
    )
    
    return context
