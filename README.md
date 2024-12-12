# Best Buy Web Scraper Documentation

## Overview
This project is a dynamic web scraper for Best Buy, designed to retrieve categories, subcategories, and product information while handling pagination and sorting. The scraper uses **Selenium** for browser automation and **BeautifulSoup** for HTML parsing.

---

## Function Descriptions

### 1. `navigate_to_usa_page`
Navigates to the Best Buy USA page and retrieves the page source.

**Purpose**:
- Detects "Choose a country" prompt and selects the USA option.

**Returns**:
- HTML source of the Best Buy USA homepage.

**Example**:
```python
page_source = navigate_to_usa_page()
print(page_source[:500])  # Print the first 500 characters



### 2. `get_categories_from_page`

**Purpose**:  
Extracts categories and their corresponding URLs from the homepage.

**Parameters**:  
- `page_source`: HTML source of the homepage.

**Returns**:  
- A list of dictionaries, each containing:
  - `name`: Name of the category.
  - `url`: URL to the category.

**Example**:  
```python
categories = get_categories_from_page(page_source)
print(categories)
# Output:
# [
#     {'name': 'Laptops & Computers', 'url': 'https://www.bestbuy.com/site/promo/laptop-and-computer-deals'},
#     {'name': 'Apple', 'url': 'https://www.bestbuy.com/site/all-electronics-on-sale/all-apple-on-sale/...'}
# ]



### 3. `get_category_page_source`
**Purpose**:  
Fetches product details for a specified category, handling pagination, sorting, and detecting subcategories.

**Parameters**:  
- `category_name`: Name of the category to fetch.  
- `categories`: List of categories from `get_categories_from_page`.  
- `sort_by`: Sorting criteria (e.g., "Featured", "Price-Low-To-High"). Defaults to "Featured".

**Returns**:  
- A dictionary with:  
  - `total_items`: Total number of items.  
  - `products`: List of product dictionaries with:  
    - `name`: Product name.  
    - `photo`: Product image URL.  
    - `price`: Product price.  
  - `subcategories`: List of subcategories (if present).  

**Example**:  
```python
result = get_category_page_source("Apple", categories, sort_by="Price-Low-To-High")
print(result['total_items'])
for product in result['products']:
    print(product)


**Code Workflow**

```python
page_source = navigate_to_usa_page()

categories = get_categories_from_page(page_source)
print(categories)

category_data = get_category_page_source("Apple", categories)
print(category_data)