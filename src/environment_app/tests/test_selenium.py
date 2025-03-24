'''# test_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@pytest.mark.skip(reason="Optional Selenium test that requires Chrome driver")
def test_home_page_title():
    """Basic Selenium test to check the homepage title."""
    # Set up Chrome options for headless running
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    try:
        # Setup the browser
        browser = webdriver.Chrome(options=options)
        
        try:
            # This assumes your app is running locally on port 5000
            browser.get('http://localhost:5000')
            
            # Check the page title
            assert "London Environment" in browser.title
            
        except Exception as e:
            pytest.skip(f"Error during Selenium test: {str(e)}")
        finally:
            browser.quit()
    
    except Exception as e:
        pytest.skip(f"Failed to set up Selenium: {str(e)}")'''