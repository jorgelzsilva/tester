from playwright.sync_api import Page
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("tester.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()

def safe_click(page: Page, selector: str, timeout=10000):
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        page.click(selector)
        logger.info(f"Clicked on {selector}")
        return True
    except Exception as e:
        logger.warning(f"Could not click on {selector}: {e}")
        return False

def safe_fill(page: Page, selector: str, value: str, timeout=10000):
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        page.fill(selector, value)
        logger.info(f"Filled {selector}")
        return True
    except Exception as e:
        logger.error(f"Could not fill {selector}: {e}")
        return False
