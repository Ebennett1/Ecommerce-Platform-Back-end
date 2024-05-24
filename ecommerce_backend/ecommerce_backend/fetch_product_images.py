import os
import sys
import django
import requests
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from api.models import Product  # Import your Product model

# Your Unsplash API Access Key
access_key = 'W6QdnPQaUc4sWRhhdos4jN6ZOwAHfHeCsROn4xrB0jQ'

# Base URL for the Unsplash API
base_url = 'https://api.unsplash.com'

# Function to search for images based on a keyword
def search_images(query, per_page=10, page=1):
    search_endpoint = f'{base_url}/search/photos'
    params = {
        'query': query,
        'client_id': access_key,
        'per_page': per_page,
        'page': page
    }
    response = requests.get(search_endpoint, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Failed to fetch images: {response.status_code}')
        return []

# Function to select the best image from the results
def select_best_image(images, strategy='first'):
    if not images:
        return None

    if strategy == 'first':
        return images[0]
    elif strategy == 'random':
        return random.choice(images)
    elif strategy == 'most_likes':
        return max(images, key=lambda img: img['likes'])
    elif strategy == 'most_relevant':
        return images[0]
    else:
        return images[0]

# Main function to fetch and store images
def main():
    products = Product.objects.filter(image='')  # Fetch products without images
    if not products:
        print('No products found without images')
        return

    for product in products:
        product_name = product.name
        images = search_images(product_name)
        best_image = select_best_image(images, strategy='first')
        if best_image:
            image_url = best_image['urls']['regular']
            # Save image URL to the product's image field
            product.image = image_url
            product.save()
            print(f'Updated image for Product ID: {product.id}')
        else:
            print(f'No image found for Product: {product_name}')

if __name__ == '__main__':
    main()
