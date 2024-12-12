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

    # Parse the page source and extract products
    soup = BeautifulSoup(page_source, 'html.parser')
    products = []

    for item in soup.select('li.sku-item'):
        name_tag = item.select_one('h4.sku-title a')
        image_tag = item.select_one('img.product-image')
        price_tag = item.select_one('div.priceView-hero-price span')

        if name_tag and image_tag and price_tag:
            products.append({
                'name': name_tag.text.strip(),
                'photo': image_tag['src'],
                'price': price_tag.text.strip()
            })

    # Extract total item count
    total_count_tag = soup.select_one('span.item-count')
    total_items = total_count_tag.text.strip() if total_count_tag else "Unknown"

    return {
        'total_items': total_items,
        'products': products
    }


# Example
page_source = navigate_to_usa_page()
categories = get_categories_from_page(page_source)

# Fetch page source for a specific category
category_name = "Laptops & Computers"
category_page_source = get_category_page_source(category_name, categories)

if category_page_source:
    product_details = category_page_source
    print(f"Total items in {category_name}: {product_details['total_items']}")
    for product in product_details['products']:
        print(product)
else:
    print(f"Could not fetch page source for {category_name}.")
