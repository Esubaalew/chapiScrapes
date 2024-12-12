from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

URL = 'https://www.bestbuy.com'

def navigate_to_usa_page():
    driver = webdriver.Chrome()
    driver.get(URL)
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
                    'url': URL+url
                })

    return categories




def get_category_page_source(category_name, categories):
    """
    Fetches the page source for the specified category.

    :param category_name: Name of the category to fetch.
    :param categories: List of categories from get_categories_from_page function.
    :return: Page source of the category page, or None if not found.
    """
    # Find the category in the list
    category = next((cat for cat in categories if cat['name'].lower() == category_name.lower()), None)
    
    if not category:
        print(f"Category '{category_name}' not found.")
        return None
    
    # Open the link and fetch the page source
    driver = webdriver.Chrome()
    driver.get(category['url'])
    if "Choose a country" in driver.page_source:
        usa_button = driver.find_element(By.CSS_SELECTOR, 'a.us-link')
        usa_button.click()
    page_source = driver.page_source
    driver.quit()
    return page_source

# page_source = navigate_to_usa_page()
# categories = get_categories_from_page(page_source)

# print("Categories found:")
# for category in categories:
#     print(category)

page_source = navigate_to_usa_page()
categories = get_categories_from_page(page_source)

# Fetch the page source for a specific category
category_name = "Laptops & Computers"
category_page_source = get_category_page_source(category_name, categories)

if category_page_source:
    print(f"Page source for {category_name} fetched successfully.")
    print(category_page_source)
else:
    print(f"Could not fetch page source for {category_name}.")
