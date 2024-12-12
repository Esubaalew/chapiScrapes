from selenium import webdriver
from selenium.webdriver.common.by import By


def navigate_to_usa_page():
    driver = webdriver.Chrome()

    url = 'https://www.bestbuy.com/'
    driver.get(url)


    if "Choose a country" in driver.page_source:
        #click the USA country option
        usa_button = driver.find_element(By.CSS_SELECTOR, 'a.us-link')
        usa_button.click()


    current_url = driver.current_url
    page_source = driver.page_source
    driver.quit()

    return current_url, page_source


current_url, page_source = navigate_to_usa_page()

print("Current URL:", current_url)
print(page_source[:500]) 
