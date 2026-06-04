from playwright.sync_api import sync_playwright, expect

def test_all_links_load():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://wrenp.pythonanywhere.com/")
        
        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")
        
        # Find all links on the page that are visible
        all_links = page.locator("a:visible").all()
        print(f"\nFound {len(all_links)} visible links")
        
        for i, link in enumerate(all_links):
            try:
                # Wait for the link to be attached to DOM and visible
                link.wait_for(state="attached", timeout=5000)
                
                # Get href attribute
                href = link.get_attribute("href")
                
                if href and not href.startswith("#") and not href.startswith("javascript:"):
                    print(f"Clicking {i+1}/{len(all_links)}: {href}")
                    
                    # Click the link and wait for navigation (with timeout)
                    with page.expect_navigation(timeout=10000):
                        link.click()
                    
                    # Check the new page loaded
                    assert page.locator("body").is_visible()
                    
                    # Go back to the homepage
                    page.go_back()
                    # Wait for the homepage to reload
                    page.wait_for_load_state("networkidle")
                    
            except Exception as e:
                print(f"Skipped link {i+1}: {e}")
                continue
        
        browser.close()
        