from playwright.sync_api import sync_playwright
import time
import config
from selectors import Selectors
from utils import logger, safe_click, safe_fill

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            # 1. Login
            logger.info(f"Navigating to {config.BASE_URL}")
            page.goto(config.BASE_URL)
            
            logger.info("Attempting Login...")
            safe_fill(page, Selectors.USERNAME_INPUT, config.USERNAME)
            safe_fill(page, Selectors.PASSWORD_INPUT, config.PASSWORD)
            safe_click(page, Selectors.LOGIN_BUTTON)
            
            # Wait for navigation to dashboard - adjust URL or selector as needed
            try:
                page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

            # Check if still on login page (Captcha likely)
            if "auth/signin" in page.url or page.is_visible("iframe[src*='recaptcha']") or page.is_visible("#captcha"):
                logger.warning("Possible CAPTCHA detected or login slow.")
                print("\n" + "!"*50)
                print("CAPTCHA DETECTED OR LOGIN STALLED")
                print("Please solve the CAPTCHA in the browser window manually.")
                print("!"*50 + "\n")
                input("Press Enter here AFTER you have solved it and the Dashboard is loading...")
                
            logger.info("Login submitted. Waiting for dashboard...")
            
            # --- Handle Potental Modal ---
            try:
                # Wait explicitly for the close button to appear
                logger.info("Looking for modal close button...")
                close_btn = page.wait_for_selector(Selectors.CLOSE_MODAL_BUTTON, state="visible", timeout=10000)
                if close_btn:
                    logger.info("Found close button. Clicking...")
                    close_btn.click()
                    time.sleep(1) # Wait for animation
            except Exception as e:
                logger.info(f"No modal close button found (or timeout): {e}")
                # Try Escape as backup
                logger.info("Trying Escape key...")
                page.keyboard.press("Escape")
            # -----------------------------

            # 2. Select Program (Accordion)
            try:
                logger.info("Waiting for program panels...")
                page.wait_for_selector(Selectors.PROGRAM_PANEL, state="visible", timeout=15000)
                panels = page.query_selector_all(Selectors.PROGRAM_PANEL)
                
                if not panels:
                    logger.error("No program panels found!")
                    return

                print("\n--- Available Programs ---")
                valid_panels = []
                for i, panel in enumerate(panels):
                    # Get title from header
                    try:
                        header = panel.query_selector(Selectors.PROGRAM_HEADER)
                        if header:
                            text = header.inner_text().replace('\n', ' ').strip()
                            # Print simplified title
                            print(f"{len(valid_panels) + 1}. {text}")
                            valid_panels.append(panel)
                    except Exception as e:
                        logger.warning(f"Error reading panel {i}: {e}")

                if not valid_panels:
                    logger.error("No valid program headers found.")
                    return

                # Interactive Selection: Program
                while True:
                    try:
                        choice = int(input("Enter the number of the program to test: "))
                        if 1 <= choice <= len(valid_panels):
                            selected_panel = valid_panels[choice - 1]
                            logger.info(f"Expanding program #{choice}")
                            
                            # Check if already expanded
                            is_expanded = selected_panel.get_attribute("aria-expanded") == "true"
                            if not is_expanded:
                                header = selected_panel.query_selector(Selectors.PROGRAM_HEADER)
                                header.click()
                                time.sleep(1) # Wait for expansion
                            break
                        else:
                            print("Invalid selection. Try again.")
                    except ValueError:
                        print("Please enter a number.")

                # 3. Select Volume (Tabs inside the panel)
                logger.info("Waiting for volume tabs...")
                # Scope to the selected panel
                tabs = selected_panel.query_selector_all(Selectors.VOLUME_TAB)
                
                if tabs:
                    print("\n--- Available Volumes ---")
                    for i, tab in enumerate(tabs):
                        print(f"{i + 1}. {tab.inner_text().strip()}")
                    
                    while True:
                        try:
                            # Default to last volume (usually latest) if user just hits enter? No, let's force choice.
                            v_choice = input(f"Select Volume # (1-{len(tabs)}): ")
                            v_choice = int(v_choice)
                            if 1 <= v_choice <= len(tabs):
                                logger.info(f"Clicking Volume #{v_choice}")
                                tabs[v_choice - 1].click()
                                time.sleep(2) # Wait for content load
                                break
                            else:
                                print("Invalid volume.")
                        except ValueError:
                            print("Enter a number.")
                else:
                    logger.info("No volume tabs found. Content might be directly available.")

            except Exception as e:
                logger.error(f"Error during Program/Volume selection: {e}")
                page.screenshot(path="debug_selection_error.png")
                return

            # 4. Navigate Articles
            logger.info("Looking for articles...")
            try:
                # Wait for ANY article link to appear (could be anywhere, but we want the list from our panel)
                # But better to wait for one inside our panel?
                # selected_panel.wait_for_selector is not standard playwright sync api on element handle? 
                # Actually ElementHandle has wait_for_selector.
                selected_panel.wait_for_selector(Selectors.ARTICLE_LINK, timeout=10000)
                
                # Scope query to the selected program panel
                articles = selected_panel.query_selector_all(Selectors.ARTICLE_LINK)
                
                if not articles:
                    logger.error("No articles found in this volume.")
                    return
                
                print(f"\nFound {len(articles)} articles.")
                # Automatically start first article? Or ask?
                # Let's ask to specific start or "All"
                print("1. Start from beginning")
                print("2. Choose specific article")
                
                mode = input("Choose mode (1/2): ")
                start_index = 0
                if mode == "2":
                    for i, art in enumerate(articles):
                         print(f"{i+1}. {art.inner_text().splitlines()[0]}")
                    try:
                        idx = int(input("Enter article #: ")) - 1
                        if 0 <= idx < len(articles):
                            start_index = idx
                    except:
                        pass
                
                logger.info(f"Opening article #{start_index + 1}...")
                current_article = articles[start_index]
                
                # Check target: does it open in new tab or same tab?
                # Usually single page apps open in same tab.
                
                # Track stats
                articles_viewed = 0
                btns_clicked = 0
                
                # Initial click to start the sequence
                current_article.click()
                
                while True:
                    # --- Handle Article First Access Modal ---
                    try:
                        logger.info("Looking for 'First Access' modal close button...")
                        # Wait up to 5 seconds for the modal to appear
                        close_btn = page.wait_for_selector(Selectors.CLOSE_MODAL_BUTTON, state="visible", timeout=5000)
                        if close_btn:
                            logger.info("Found modal close button. Clicking...")
                            close_btn.click()
                            time.sleep(2) # wait for fade out
                    except Exception:
                        logger.info("No 'First Access' modal detected (timeout).")
                    # -----------------------------------------

                    # --- New Strategy: Reverse Traversal (Bottom to Top) ---
                    # 1. Scroll to Bottom to force lazy loading
                    logger.info("Scrolling to bottom to load all content...")
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(3)
                    
                    # 2. Interact with elements from Bottom to Top
                    logger.info("Interacting with elements in reverse order...")
                    try:
                        # Collect all interactive candidates
                        candidates = page.query_selector_all(f"{Selectors.ALTERNATIVE_OPTION}, {Selectors.CHECK_ANSWER_BUTTON}")
                        
                        for el in reversed(candidates):
                            try:
                                if el.is_visible():
                                    # Use force=True for speed, skip checks
                                    el.click(timeout=500, force=True)
                                    btns_clicked += 1
                                    time.sleep(0.05) # ~50ms delay
                            except Exception:
                                pass
                    except Exception as e:
                        logger.warning(f"Error in reverse interaction: {e}")

                    # 3. Go to Top
                    logger.info("Scrolling to top...")
                    page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(0.5)
                    
                    # 4. Continuous Scroll Top to Bottom
                    logger.info("Reading article (scrolling down)...")
                    current_scroll = 0
                    while True:
                        page.evaluate("window.scrollBy(0, 600)")
                        time.sleep(0.4)
                        new_scroll = page.evaluate("window.scrollY + window.innerHeight")
                        doc_height = page.evaluate("document.body.scrollHeight")
                        
                        if new_scroll >= doc_height:
                            break
                        
                        if new_scroll == current_scroll:
                            break
                        current_scroll = new_scroll

                    # 5. Mark as Read (At the bottom)
                    try:
                        logger.info("Looking for 'Marcar como concluído'...")
                        mark_btn = page.query_selector(Selectors.MARK_READ_BUTTON)
                        if mark_btn:
                            mark_btn.scroll_into_view_if_needed()
                            if mark_btn.is_visible():
                                mark_btn.click()
                                logger.info("Clicked 'Marcar como concluído'")
                                time.sleep(1)
                    except Exception as e:
                        logger.warning(f"Mark read error: {e}")

                    # 6. Next Article
                    logger.info("Looking for Next button...")
                    try:
                        next_btn = page.query_selector(Selectors.NEXT_BUTTON)
                        if next_btn and next_btn.is_visible():
                            logger.info("Found Next button. Clicking...")
                            next_btn.scroll_into_view_if_needed()
                            next_btn.click()
                            articles_viewed += 1
                            time.sleep(3) # Wait for page load
                        else:
                            logger.info("No 'Next' button found (End of Volume).")
                            break
                    except Exception as e:
                        logger.error(f"Error clicking Next: {e}")
                        break
                    
                    if articles_viewed > 15: # Safety break
                        logger.info("Viewed 15 articles. Stopping for safely.")
                        break

                logger.info("="*40)
                logger.info("      TEST RUN SUMMARY      ")
                logger.info("="*40)
                logger.info(f"Total Articles Processed: {articles_viewed}")
                logger.info(f"Total Buttons Clicked:    {btns_clicked}")
                logger.info("="*40)

            except Exception as e:
                logger.error(f"Error in Article Navigation flow: {e}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            try:
                page.screenshot(path="error_screenshot.png")
            except:
                logger.error("Could not save screenshot (browser closed).")
        finally:
            # Leave browser open for a bit if we want to inspect
            time.sleep(2)
            browser.close()

if __name__ == "__main__":
    run()


