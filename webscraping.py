from bs4 import BeautifulSoup
import pandas as pd
import re # For cleaning extracted text

# --- 1. Simulate Data Collection: HTML Content ---
# In a real scenario, you would use 'requests' to fetch content from a URL:
# import requests
# url = "https://example.com/products"
# response = requests.get(url)
# html_content = response.text

# For this demonstration, we'll use a multi-line string representing HTML.
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Our Products</title>
</head>
<body>
    <div class="header">
        <h1>Welcome to Our Store!</h1>
        <p>Discover our amazing products.</p>
    </div>

    <div class="product-list">
        <div class="product-item" id="product-101">
            <h2 class="product-name">Laptop Pro X</h2>
            <p class="product-price">Price: $1200.99</p>
            <div class="product-rating">Rating: 4.5/5</div>
            <span class="availability">In Stock</span>
        </div>

        <div class="product-item" id="product-102">
            <h2 class="product-name">Wireless Mouse Z</h2>
            <p class="product-price">Price: $25.50</p>
            <div class="product-rating">Rating: 4.0/5</div>
            <span class="availability">Low Stock</span>
        </div>

        <div class="product-item" id="product-103">
            <h2 class="product-name">Ergonomic Keyboard</h2>
            <p class="product-price">Price: $75.00</p>
            <div class="product-rating">Rating: 4.8/5</div>
            <span class="availability">In Stock</span>
        </div>

        <div class="product-item" id="product-104">
            <h2 class="product-name">USB-C Hub Elite</h2>
            <p class="product-price">Price: $49.99</p>
            <div class="product-rating">Rating: Not Rated</div>
            <span class="availability">Out of Stock</span>
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2025 Our Store. All rights reserved.</p>
    </div>
</body>
</html>
"""

print("--- Simulated HTML Content ---")
print(html_content[:300] + "...\n") # Print first 300 chars for brevity

# --- 2. Parse HTML and Extract Data ---

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all product items. We identify them by their class 'product-item'.
product_items = soup.find_all('div', class_='product-item')

extracted_data = []

print("--- Extracting Data ---")
for item in product_items:
    product = {}

    # Extract Product Name
    # Find the h2 tag with class 'product-name' within the current product item
    name_tag = item.find('h2', class_='product-name')
    if name_tag:
        product['name'] = name_tag.get_text(strip=True)
    else:
        product['name'] = 'N/A'

    # Extract Product Price
    # Find the p tag with class 'product-price'
    price_tag = item.find('p', class_='product-price')
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        # Use regex to extract only the numerical part of the price
        price_match = re.search(r'\$([\d.]+)', price_text)
        if price_match:
            product['price'] = float(price_match.group(1))
        else:
            product['price'] = 'N/A'
    else:
        product['price'] = 'N/A'

    # Extract Product Rating
    # Find the div tag with class 'product-rating'
    rating_tag = item.find('div', class_='product-rating')
    if rating_tag:
        rating_text = rating_tag.get_text(strip=True)
        # Extract the rating number (e.g., "4.5" from "Rating: 4.5/5")
        rating_match = re.search(r'Rating: ([\d.]+)/5', rating_text)
        if rating_match:
            product['rating'] = float(rating_match.group(1))
        elif "Not Rated" in rating_text:
            product['rating'] = 'Not Rated'
        else:
            product['rating'] = 'N/A'
    else:
        product['rating'] = 'N/A'

    # Extract Availability (example of another field)
    availability_tag = item.find('span', class_='availability')
    if availability_tag:
        product['availability'] = availability_tag.get_text(strip=True)
    else:
        product['availability'] = 'N/A'

    extracted_data.append(product)
    print(f"Extracted: {product}")

# --- 3. Create Custom Dataset (Pandas DataFrame) ---

df = pd.DataFrame(extracted_data)

print("\n--- Custom Dataset (Pandas DataFrame) ---")
print(df)

print("\n--- Data Types of the DataFrame ---")
print(df.info())

# Example of further analysis (optional)
print("\n--- Products with Price > $100 ---")
# Ensure 'price' column is numeric for comparison
df['price'] = pd.to_numeric(df['price'], errors='coerce')
print(df[df['price'] > 100])

print("\n--- Average Rating of Rated Products ---")
# Filter out 'Not Rated' and 'N/A' before calculating mean
numeric_ratings = pd.to_numeric(df['rating'], errors='coerce').dropna()
if not numeric_ratings.empty:
    print(f"Average Rating: {numeric_ratings.mean():.2f}")
else:
    print("No numeric ratings available to calculate average.")

