from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

URL = 'https://www.bestbuy.com'

def navigate_to_usa_page():
    """ Navigate to the Best Buy USA page and return the page source"""

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






def get_category_page_source(category_name, categories, sort_by="Featured"):
    """
    Fetches the page source for the specified category, handling pagination, sorting, and subcategories.

    :param category_name: Name of the category to fetch.
    :param categories: List of categories from get_categories_from_page function.
    :param sort_by: Sorting option (default is "Featured").
    :return: Page source of the category page, subcategories, and product details.
    """
    
    category = next((cat for cat in categories if cat['name'].lower() == category_name.lower()), None)
    
    if not category:
        print(f"Category '{category_name}' not found.")
        return None, []
    
    driver = webdriver.Chrome()
    driver.get(category['url'])
    
    
    if "Choose a country" in driver.page_source:
        usa_button = driver.find_element(By.CSS_SELECTOR, 'a.us-link')
        usa_button.click()
        driver.refresh()

   # Check for subcategories (if found, break as it's a subcategory)
    if driver.find_elements(By.CSS_SELECTOR, 'li.crumb-list-item a.crumb[href^="https://www.bestbuy.com/"]'):
        print(f"Subcategory found for '{category_name}', terminating.")
        driver.quit()
        return None

      
    
    # Sort dropdown and fetch products
    sort_dropdown = driver.find_element(By.ID, 'sort-by-select')
    sort_dropdown.click()
    sort_option = driver.find_element(By.CSS_SELECTOR, f'option[value="{sort_by}"]')
    sort_option.click()
    driver.refresh()

    page_source = driver.page_source
    products = []

    # Handle pagination
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items_on_page = soup.select('li.sku-item')

        if not items_on_page:
            break
        
        for item in items_on_page:
            name_tag = item.select_one('h4.sku-title a')
            image_tag = item.select_one('img.product-image')
            price_tag = item.select_one('div.priceView-hero-price span')

            if name_tag and image_tag and price_tag:
                products.append({
                    'name': name_tag.text.strip(),
                    'photo': image_tag['src'],
                    'price': price_tag.text.strip()
                })

        next_page = soup.select_one('a.sku-list-page-next')
        if not next_page or 'disabled' in next_page.get('class', []):
            break

        next_page_url = URL + next_page['href']
        driver.get(next_page_url)
    
    driver.quit()
    
    # Extract total item count
    total_count_tag = soup.select_one('span.item-count')
    total_items = total_count_tag.text.strip() if total_count_tag else "Unknown"

    return {
        'total_items': total_items,
        'products': products,
    }




# Example
page_source = navigate_to_usa_page()
categories = get_categories_from_page(page_source)

# Fetch page source for a specific category
category_name = ""
category_page_source = get_category_page_source(category_name, categories)

if category_page_source:
    product_details = category_page_source
    print(f"Total items in {category_name}: {product_details['total_items']}")
    for product in product_details['products']:
        print(product)
else:
    print(f"Could not fetch page source for {category_name}.")


