from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def navigate_to_usa_page():
    driver = webdriver.Chrome()
    url = 'https://www.bestbuy.com/'
    driver.get(url)
    if "Choose a country" in driver.page_source:
        usa_button = driver.find_element(By.CSS_SELECTOR, 'a.us-link')
        usa_button.click()
    current_url = driver.current_url
    page_source = driver.page_source
    driver.quit()
    return page_source


def get_categories_from_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    categories = []

    for item in soup.select('li.c-carousel-item'):
        # Exclude items containing product-specific details like ratings
        if item.select_one('.product-rating'):
            continue
        
        category = item.find('a')
        if category:
            name = category.get_text(strip=True)
            url = category['href']
            
            if name:
                categories.append({
                    'name': name,
                    'url': url
                })

    return categories




page_source = navigate_to_usa_page()
categories = get_categories_from_page(page_source)

print("Categories found:")
for category in categories:
    print(category)
