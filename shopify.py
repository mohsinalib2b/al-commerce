import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to extract product details from a page
def extract_product_details(soup):
    products = []
    product_items = soup.find_all('div', class_='grid__item')  # Adjust this according to the actual structure
    total_products = len(product_items)
    for index, product in enumerate(product_items):
        try:
            title = product.find('div', class_='grid-product__title').text.strip() if product.find('div', class_='grid-product__title') else 'N/A'
            price = product.find('span', class_='grid-product__price').text.strip() if product.find('span', class_='grid-product__price') else 'N/A'
            category = 'N/A'  # Update this if category info is available on the product listing page
            image = product.find('img', class_='grid__image')['src'] if product.find('img', class_='grid__image') else 'N/A'
            link = 'https://cartbeaststore.com' + product.find('a', href=True)['href'] if product.find('a', href=True) else 'N/A'
            
            # Fetch the product page for additional details
            product_page = requests.get(link)
            product_soup = BeautifulSoup(product_page.content, 'html.parser')
            
            short_description = product_soup.find('div', class_='product-single__description').text.strip() if product_soup.find('div', class_='product-single__description') else 'N/A'
            description = product_soup.find('div', class_='product-single__description').text.strip() if product_soup.find('div', class_='product-single__description') else 'N/A'
            
            products.append({
                'Title': title,
                'Price': price,
                'Category': category,
                'Image Link': image,
                'Link': link,
                'Short Description': short_description,
                'Description': description
            })

            # Print progress
            print(f"Processed {index + 1}/{total_products} products.")
        
        except Exception as e:
            print(f"Failed to process product {index + 1}/{total_products}. Error: {e}")
    
    return products

# Function to get all product details by traversing pagination
def get_all_products(url):
    products = []
    page = 1
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products.extend(extract_product_details(soup))
        
        next_page = soup.find('link', rel='next')
        url = 'https://cartbeaststore.com' + next_page['href'] if next_page else None

        print(f"Completed page {page}. Moving to next page...")
        page += 1

    return products

# Replace with the actual Shopify website URL
url = "https://cartbeaststore.com/collections/all"

# Fetch all products from the website
all_products = get_all_products(url)

# Convert the products list to a DataFrame
df = pd.DataFrame(all_products)

# Define the path to save the file
output_file = os.path.join(os.getcwd(), 'shopify_products.csv')

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)

print(f"Product data has been saved to {output_file}")
