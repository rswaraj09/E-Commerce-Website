import requests
import time
import json
from django.conf import settings
from decouple import config

GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY
}

def fetch_market_price(product_name):
    prompt = f"What is the current market price of {product_name} in India (INR)? Only give the number, no currency symbol or text."
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(GEMINI_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        try:
            result = response.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            price = int(''.join(filter(str.isdigit, text.split()[0])))
            return price
        except Exception as e:
            print(f"Error parsing response for {product_name}: {e}")
    else:
        print(f"API error for {product_name}: {response.status_code}")
    return None

import re

def update_populate_data_py(updated_prices):
    populate_path = "d:/PROJECTS/E-COMMERCE/products/management/commands/populate_data.py"
    with open(populate_path, "r", encoding="utf-8") as f:
        content = f.read()
    def price_replacer(match):
        name = match.group(1)
        old_price = match.group(2)
        new_price = updated_prices.get(name)
        if new_price:
            return f"{{'name': '{name}', 'price': {new_price}, 'category':"  # rest of line remains
        return match.group(0)
    # Replace prices in products_data
    content = re.sub(r"\{'name': '([^']+)', 'price': (\d+), 'category':", price_replacer, content)
    with open(populate_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    products = [
        "iPhone 15 Pro",
        "Samsung Galaxy S24",
        "MacBook Air M3",
        "Dell XPS 13",
        "Sony WH-1000XM5",
        "Casual Cotton T-Shirt",
        "Denim Jeans Classic",
        "Winter Wool Sweater",
        "Running Sneakers",
        "Leather Jacket",
        "Python Programming Guide",
        "Machine Learning Basics",
        "Web Development Handbook",
        "Data Science Cookbook",
        "Smart Home Speaker",
        "Garden Tool Set",
        "LED Desk Lamp",
        "Yoga Mat Premium",
        "Dumbbell Set",
        "Fitness Tracker"
    ]
    updated_prices = {}
    for product in products:
        print(f"Fetching price for {product}...")
        price = fetch_market_price(product)
        updated_prices[product] = price
        print(f"{product}: {price}")
        time.sleep(2)  # Avoid hitting rate limits
    print("\nUpdated prices:")
    for k, v in updated_prices.items():
        print(f"{k}: {v}")
    update_populate_data_py(updated_prices)
