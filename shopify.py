import csv
import json
import urllib.request
from bs4 import BeautifulSoup

# Hardcoded URL for the Shopify store
base_url = 'https://domain.com'
collection_url = base_url + '/collections/all/products.json'
with_variants = True  # Set this to False if you don't want to scrape variants

def get_page(url, page):
    full_url = f'{url}?page={page}'
    data = urllib.request.urlopen(full_url).read()
    products = json.loads(data)['products']
    return products

def get_tags_from_product(product_url):
    r = urllib.request.urlopen(product_url).read()
    soup = BeautifulSoup(r, "html.parser")

    title = soup.title.string
    description = ''
    meta = soup.find_all('meta')
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == 'description':
            description = tag.attrs['content']
    return [title, description]

def get_image_url(product):
    images = product['images']
    if images:
        return images[0]['src']
    return ''

# Main scraping and writing function
with open('sports_and_fitness_products.csv', 'w', newline='', encoding='utf-8') as f:
    page = 1
    print("[+] Starting script")

    writer = csv.writer(f)
    if with_variants:
        writer.writerow(['Name', 'Variant Name', 'Price', 'URL', 'Image URL', 'Meta Title', 'Meta Description', 'Product Description'])
    else:
        writer.writerow(['Name', 'URL', 'Image URL', 'Meta Title', 'Meta Description', 'Product Description'])

    print("[+] Checking products page")
    products = get_page(collection_url, page)
    while products:
        for product in products:
            name = product['title']
            product_url = base_url + '/products/' + product['handle']
            image_url = get_image_url(product)
            body_description = BeautifulSoup(product['body_html'], "html.parser").get_text()

            print(" ├ Scraping: " + product_url)
            title, description = get_tags_from_product(product_url)

            if with_variants:
                for variant in product['variants']:
                    variant_name = variant['title']
                    price = variant['price']
                    row = [name, variant_name, price, product_url, image_url, title, description, body_description]
                    writer.writerow(row)
            else:
                row = [name, product_url, image_url, title, description, body_description]
                writer.writerow(row)
        page += 1
        products = get_page(collection_url, page)

print("[+] Script completed")
