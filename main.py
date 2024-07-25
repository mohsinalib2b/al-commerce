import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace with the actual WooCommerce website URL
url = "https://macroxoft.com/product-category/crm/"

# Function to extract product details from a page
def extract_product_details(soup):
    products = []
    for product in soup.find_all('li', class_='product'):
        title = product.find('h2', class_='woocommerce-loop-product__title').text
        price = product.find('span', class_='woocommerce-Price-amount').text
        category = product.find('span', class_='cat_product').text if product.find('span', class_='cat_product') else 'Unknown'
        image = product.find('img', class_='attachment-woocommerce_thumbnail')['src']
        link = product.find('a', href=True)['href']
        products.append({
            'Title': title,
            'Price': price,
            'Category': category,
            'Image Link': image,
            'Link': link
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

# Fetch all products from the website
all_products = get_all_products(url)

# Convert the products list to a DataFrame
df = pd.DataFrame(all_products)

# Display the DataFrame to the user for confirmation
print(df)

# Ask for user confirmation before saving
confirmation = input("Do you want to save this data to an Excel file? (yes/no): ")

if confirmation.lower() == 'yes':
    # Save the DataFrame to an Excel file
    output_file = 'woocommerce_products.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Product data has been saved to {output_file}")
else:
    print("Data not saved.")
