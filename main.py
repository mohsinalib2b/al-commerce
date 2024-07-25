import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to extract product details from a page
def extract_product_details(soup):
    products = []
    for product in soup.find_all('li', class_='product'):
        title = product.find('h2', class_='woocommerce-loop-product__title').text
        price = product.find('span', class_='woocommerce-Price-amount').text
        categories = [cat.text for cat in product.find_all('span', class_='cat_product')]
        category = ', '.join(categories)
        image = product.find('img', class_='attachment-woocommerce_thumbnail')['src']
        link = product.find('a', href=True)['href']
        
        # Fetch the product page for additional details
        product_page = requests.get(link)
        product_soup = BeautifulSoup(product_page.content, 'html.parser')
        
        short_description = product_soup.find('div', class_='woocommerce-product-details__short-description').text.strip() if product_soup.find('div', class_='woocommerce-product-details__short-description') else 'N/A'
        description = product_soup.find('div', id='tab-description').text.strip() if product_soup.find('div', id='tab-description') else 'N/A'
        
        products.append({
            'Title': title,
            'Price': price,
            'Category': category,
            'Image Link': image,
            'Link': link,
            'Short Description': short_description,
            'Description': description
        })
    return products

# Function to get all product details by traversing pagination
def get_all_products(url):
    products = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products.extend(extract_product_details(soup))
        
        next_page = soup.find('a', class_='next', href=True)
        url = next_page['href'] if next_page else None
    return products

# Replace with the actual WooCommerce website URL
url = "https://macroxoft.com/product-category/crm/"

# Fetch all products from the website
all_products = get_all_products(url)

# Convert the products list to a DataFrame
df = pd.DataFrame(all_products)

# Define the path to save the file
output_file = os.path.join(os.getcwd(), 'woocommerce_products.csv')

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)

print(f"Product data has been saved to {output_file}")
