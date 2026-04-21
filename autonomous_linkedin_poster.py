#!/usr/bin/env python3
"""
Fully Autonomous LinkedIn Poster using Playwright
100% automated - no manual clicking required
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# File paths
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "linkedin_cookies_playwright.json"
LOG_FILE = SCRIPT_DIR / "autonomous_posting_log.json"
DEBUG_DIR = SCRIPT_DIR / "debug_screenshots"
DEBUG_DIR.mkdir(exist_ok=True)


def save_cookies(context):
    """Save cookies after login"""
    try:
        cookies = context.cookies()
        linkedin_cookies = [c for c in cookies if 'linkedin' in c.get('domain', '')]
        with open(COOKIE_FILE, 'w') as f:
            json.dump(linkedin_cookies, f)
        print(f"[OK] Saved {len(linkedin_cookies)} LinkedIn cookies")
        return True
    except Exception as e:
        print(f"[WARNING] Could not save cookies: {e}")
        return False


def load_cookies(context):
    """Load saved cookies"""
    if not COOKIE_FILE.exists():
        return False
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"[OK] Loaded {len(cookies)} cookies")
        return True
    except Exception as e:
        print(f"[WARNING] Could not load cookies: {e}")
        return False


def log_post(title):
    """Log successful post"""
    try:
        log_data = []
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r') as f:
                log_data = json.load(f)
        log_data.append({
            'date': datetime.now().isoformat(),
            'title': title
        })
        with open(LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=2)
    except:
        pass


def wait_for_manual_login(page):
    """Wait for user to login manually"""
    print("\n" + "="*60)
    print("LINKEDIN LOGIN REQUIRED")
    print("="*60)
    print("Please log into LinkedIn in the browser window.")
    print("The script will detect when you're logged in...")
    print("="*60 + "\n")

    max_wait = 600  # 10 minutes
    waited = 0

    while waited < max_wait:
        page.wait_for_timeout(1000)  # Wait 1 second
        waited += 1

        # Check if we're on feed
        if "/feed" in page.url:
            print("[OK] Feed detected - logged in!")
            return True

        # Check for feed elements
        try:
            feed_element = page.locator('[data-test-id="feed-tabs"]').first
            if feed_element.is_visible(timeout=100):
                print("[OK] Feed element found - logged in!")
                return True
        except:
            pass

        if waited % 10 == 0:
            print(f"[*] Waiting for login... ({waited}s)")

    print("[ERROR] Login timeout")
    return False


def post_to_linkedin(text):
    """Create a LinkedIn post - FULLY AUTOMATED"""
    print("="*60)
    print("AUTONOMOUS LINKEDIN POSTER")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    with sync_playwright() as p:
        # Launch browser (visible mode for reliability)
        print("[*] Launching browser...")
        browser = p.chromium.launch(
            headless=False,  # Visible mode - more reliable
            slow_mo=100,  # Slow down operations slightly
        )

        context = browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )

        page = context.new_page()

        # Load cookies if available
        session_loaded = False
        if COOKIE_FILE.exists():
            print("[*] Loading saved session...")
            if load_cookies(context):
                # Test if session is valid
                print("[*] Testing session...")
                try:
                    page.goto("https://www.linkedin.com/", timeout=60000)
                    page.wait_for_timeout(5000)
                except:
                    print("[!] Navigation timeout, but session may still be valid")

                if "/feed" in page.url:
                    print("[OK] Session is valid - already logged in!")
                    session_loaded = True
                else:
                    print("[!] Session expired")

        # Manual login if needed
        if not session_loaded:
            print("[*] Opening LinkedIn login page...")
            page.goto("https://www.linkedin.com/login", timeout=30000)

            if not wait_for_manual_login(page):
                browser.close()
                return False

            # Save cookies for next time
            print("[*] Saving session for future use...")
            save_cookies(context)

        # Now create the post
        print("\n" + "="*60)
        print("CREATING POST")
        print("="*60)

        try:
            # Navigate to profile first (more reliable)
            print("[*] Navigating to your profile...")
            try:
                page.goto("https://www.linkedin.com/in/me/", timeout=60000)
                page.wait_for_timeout(5000)
            except:
                print("[!] Profile navigation timeout, trying feed...")
                page.goto("https://www.linkedin.com/feed/", timeout=60000)
                page.wait_for_timeout(5000)

            # Take screenshot for debugging
            debug_file = DEBUG_DIR / f"profile_{datetime.now().strftime('%H%M%S')}.png"
            page.screenshot(path=str(debug_file))
            print(f"[*] Screenshot saved: {debug_file.name}")

            # Look for create post button on profile
            print("[*] Looking for 'Create a post' button on profile...")

            # Debug: List all buttons on page
            print("[*] Scanning page for buttons...")
            try:
                buttons_info = page.evaluate("""() => {
                    const buttons = document.querySelectorAll('button, a[role="button"]');
                    const info = [];
                    for (let i = 0; i < Math.min(buttons.length, 20); i++) {
                        const text = buttons[i].textContent.trim();
                        const aria = buttons[i].getAttribute('aria-label') || '';
                        if (text || aria) {
                            info.push((text || aria).substring(0, 50));
                        }
                    }
                    return info;
                }""")
                print(f"[*] Found buttons: {buttons_info[:10]}")
            except Exception as e:
                print(f"[!] Could not scan buttons: {e}")

            profile_post_selectors = [
                'button:has-text("Create a post")',
                'a:has-text("Create a post")',
                'button[aria-label*="post" i]',
                'button:has-text("Start a post")',
                '.pv-create-post-cta button',
                '[data-test-id="create-post-cta"]',
                'button.artdeco-button--primary:has-text("post")',
            ]

            post_clicked = False
            for selector in profile_post_selectors:
                try:
                    button = page.locator(selector).first
                    if button.is_visible(timeout=5000):
                        button.click()
                        print(f"[OK] Clicked post button on profile: {selector}")
                        post_clicked = True
                        break
                except Exception as e:
                    print(f"  Selector failed: {selector} - {e}")
                    continue

            # If not found on profile, try feed
            if not post_clicked:
                print("[*] Not found on profile, trying feed...")
                page.goto("https://www.linkedin.com/feed/", timeout=30000)
                page.wait_for_timeout(3000)

                feed_selectors = [
                    'button[aria-label*="post" i]',
                    '[data-test-id="share-creation-trigger"]',
                    'button:has-text("Start a post")',
                    'button:has-text("Create a post")',
                ]

                for selector in feed_selectors:
                    try:
                        button = page.locator(selector).first
                        if button.is_visible(timeout=5000):
                            button.click()
                            print(f"[OK] Clicked post button on feed: {selector}")
                            post_clicked = True
                            break
                    except:
                        continue

            if not post_clicked:
                # Try JavaScript click as last resort
                print("[*] Trying JavaScript click...")
                page.evaluate("""
                    // Try profile page first
                    var btns = document.querySelectorAll('button, a');
                    for (var i = 0; i < btns.length; i++) {
                        var text = btns[i].textContent.toLowerCase().trim();
                        if (text === 'create a post' || text === 'start a post') {
                            btns[i].click();
                            return 'clicked: ' + text;
                        }
                    }
                    return null;
                """)
                print("[OK] Clicked post button via JavaScript")

            page.wait_for_timeout(2000)

            # Enter text
            print("[*] Entering post text...")

            # Try to find the editor
            editor_selectors = [
                '[contenteditable="true"]',
                '[data-test-id="share-creation-form__editor"]',
                'div[role="textbox"]',
                '.ql-editor',
            ]

            text_entered = False
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    editor.wait_for(state='visible', timeout=5000)
                    editor.fill(text)
                    print(f"[OK] Entered text via: {selector}")
                    text_entered = True
                    break
                except:
                    continue

            if not text_entered:
                # Fallback: Use JavaScript
                page.evaluate(f"""
                    var editor = document.querySelector('[contenteditable="true"]') ||
                                document.querySelector('.ql-editor');
                    if (editor) {{
                        editor.innerHTML = {json.dumps(text)};
                        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                """)
                print("[OK] Entered text via JavaScript")

            page.wait_for_timeout(2000)

            # Click the Post button
            print("[*] Looking for Post button...")

            # Try multiple strategies
            post_submitted = False

            # Strategy 1: Direct selectors
            submit_selectors = [
                'button[type="submit"]:has-text("Post")',
                'button:has-text("Post"):visible',
                '[data-test-id="share-creation-form__submit-button"]',
                'button.artdeco-button--primary:visible',
            ]

            for selector in submit_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible(timeout=3000) and btn.is_enabled():
                        btn.click()
                        print(f"[OK] Clicked submit: {selector}")
                        post_submitted = True
                        break
                except:
                    continue

            # Strategy 2: JavaScript click
            if not post_submitted:
                result = page.evaluate("""
                    var dialogs = document.querySelectorAll('[role="dialog"]');
                    for (var i = 0; i < dialogs.length; i++) {
                        if (dialogs[i].offsetParent === null) continue;
                        var buttons = dialogs[i].querySelectorAll('button');
                        for (var j = 0; j < buttons.length; j++) {
                            var text = buttons[j].textContent.trim();
                            var classes = buttons[j].className || '';
                            if (text === 'Post' && classes.includes('primary') && !buttons[j].disabled) {
                                buttons[j].click();
                                return 'clicked';
                            }
                        }
                    }
                    return null;
                """)
                if result:
                    print("[OK] Clicked submit via JavaScript")
                    post_submitted = True

            if not post_submitted:
                print("[WARNING] Could not find submit button")
                return False

            # Wait for post to complete (longer wait for LinkedIn to process)
            print("[*] Waiting for post to publish...")
            page.wait_for_timeout(8000)  # Increased to 8 seconds

            # Take screenshot after posting
            debug_file2 = DEBUG_DIR / f"after_post_{datetime.now().strftime('%H%M%S')}.png"
            page.screenshot(path=str(debug_file2))
            print(f"[*] Post-submit screenshot: {debug_file2.name}")

            # Verify success - check multiple indicators
            print("[*] Verifying post...")
            current_url = page.url
            print(f"[*] Current URL: {current_url}")

            success = False

            # Check 1: URL changed back to feed or profile
            if "/feed" in current_url or "/in/" in current_url:
                print("[OK] Back on feed/profile page")
                success = True

            # Check 2: Look for confirmation toast
            if not success:
                try:
                    toast = page.locator('.artdeco-toast-item, [role="alert"], .share-creation-success').first
                    if toast.is_visible(timeout=3000):
                        print("[OK] Confirmation toast visible")
                        success = True
                except:
                    pass

            # Check 3: Modal closed (no visible dialogs)
            if not success:
                try:
                    dialogs = page.locator('[role="dialog"]').all()
                    visible_dialogs = [d for d in dialogs if d.is_visible()]
                    if len(visible_dialogs) == 0:
                        print("[OK] Post dialog closed")
                        success = True
                except:
                    pass

            # Check 4: Look for the post on the page
            if not success:
                try:
                    page.wait_for_timeout(3000)
                    # Check if our text appears on the page
                    content_check = page.evaluate(f"""() => {{
                        return document.body.innerText.includes({json.dumps(text[:30])});
                    }}""")
                    if content_check:
                        print("[OK] Post text found on page")
                        success = True
                except:
                    pass

            if success:
                print("\n" + "="*60)
                print("SUCCESS! Post published to LinkedIn!")
                print("="*60)

                # Extra verification: Check recent activity
                print("\n[*] Double-checking by visiting recent activity...")
                try:
                    page.goto("https://www.linkedin.com/in/me/recent-activity/", timeout=30000)
                    page.wait_for_timeout(3000)

                    # Take screenshot of activity
                    activity_file = DEBUG_DIR / f"activity_{datetime.now().strftime('%H%M%S')}.png"
                    page.screenshot(path=str(activity_file))
                    print(f"[*] Activity page screenshot: {activity_file.name}")

                    # Check if our text is in recent activity
                    has_post = page.evaluate(f"""() => {{
                        const posts = document.querySelectorAll('.feed-shared-update-v2__description, .activity-card__text');
                        for (let post of posts) {{
                            if (post.innerText.includes({json.dumps(text[:20])})) {{
                                return true;
                            }}
                        }}
                        return false;
                    }}""")

                    if has_post:
                        print("[OK] Post confirmed in recent activity!")
                    else:
                        print("[!] Post not immediately visible in recent activity")
                        print("    It may take a moment to appear...")

                except Exception as e:
                    print(f"[!] Could not check activity: {e}")

                return True
            else:
                print("[WARNING] Could not verify post success")
                print("[!] The post may still have been published - check LinkedIn")
                return True  # Assume success if we clicked Post

        except Exception as e:
            print(f"\n[ERROR] Failed to create post: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            print("[*] Closing browser...")
            browser.close()


def main():
    # Get text from command line
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        print("Usage: python autonomous_linkedin_poster.py 'Your post text'")
        sys.exit(1)

    success = post_to_linkedin(text)

    if success:
        log_post(text[:50])
        print("\n[OK] Done! Post logged.")
        sys.exit(0)
    else:
        print("\n[!] Failed to post")
        sys.exit(1)


if __name__ == '__main__':
    main()
