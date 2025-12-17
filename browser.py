from playwright.async_api import async_playwright, BrowserContext, Playwright
import tomllib
import sys
import os
import logging

logger = logging.getLogger(__name__)


def load_config():
    logger.debug("Loading config from config.toml")
    try:
        # Assuming config.toml is in the root of the workspace (parent of linkedin package)
        # Adjust path if necessary
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
            logger.debug("Config loaded successfully")
            return config
    except FileNotFoundError:
        logger.error("config.toml not found")
        sys.exit(1)


async def launch_browser(p: Playwright) -> BrowserContext:
    config = load_config()
    browser_config = config.get("browser", {})
    context_config = config.get("context", {})

    args = browser_config.get("args", [])
    headless = browser_config.get("headless", False)

    # Ensure user_data_dir is absolute or relative to CWD correctly
    user_data_path = context_config.get("user_data_dir", "./chrome_user_data1")

    logger.info("Launching browser with headless=%s", headless)
    logger.debug("Using user_data_dir: %s", user_data_path)

    context = await p.chromium.launch_persistent_context(
        user_data_dir=user_data_path,
        headless=headless,
        args=args,
        user_agent=context_config.get("user_agent"),
    )

    logger.debug("Browser context created successfully")
    return context
