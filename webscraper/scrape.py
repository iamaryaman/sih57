import requests
from bs4 import BeautifulSoup

# Specific API keys for Amazon and Flipkart
AMAZON_API_KEY = 'af935b4d202eaa8051e6689b89d2c98b'
FLIPKART_API_KEY = '6b0bf7e591e4ea71156dde994a635d49'

def scrape_amazon(url):
    """
    Scrapes a product page from Amazon.
    """
    print("--- Scraping Amazon Product Page ---")
    payload = {
        'api_key': AMAZON_API_KEY,
        'url': url,
        'render': 'true',
        'wait_for_selector': 'h1#productTitle',
        'country_code': 'in',
        'device_type': 'desktop',
        'max_cost': '50',
        'follow_redirect': 'false',
        'premium': 'true'
    }

    try:
        r = requests.get('https://api.scraperapi.com/', params=payload)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        # --- Product Name ---
        product_name = (
            soup.select_one('#productTitle') or
            soup.select_one('span#title')
        )
        product_name = product_name.get_text(strip=True) if product_name else "Product Name not found"

        # --- Price ---
        price = "Price not found"
        try:
            price_whole = soup.select_one('.a-price .a-price-whole')
            price_fraction = soup.select_one('.a-price .a-price-fraction')
            if price_whole and price_fraction:
                price = price_whole.get_text(strip=True) + price_fraction.get_text(strip=True)
            else:
                price = soup.select_one('#priceblock_dealprice, #priceblock_ourprice').get_text(strip=True)
        except Exception:
            pass

        # --- Original Price ---
        original_price = "Original Price not found"
        try:
            original_price = soup.select_one('.a-text-price .a-offscreen').get_text(strip=True)
        except Exception:
            pass

        # --- Rating ---
        rating = "Rating not found"
        try:
            rating = soup.select_one('.a-icon-alt').get_text(strip=True)
        except Exception:
            pass

        # --- Number of Ratings/Reviews ---
        num_ratings_reviews = "Number of ratings/reviews not found"
        try:
            num_ratings_reviews = soup.select_one('#acrCustomerReviewText').get_text(strip=True)
        except Exception:
            pass

        # --- Description ---
        description = "Product description not found"
        try:
            description_list = [li.get_text(strip=True) for li in soup.select('#feature-bullets ul li span.a-list-item') if li.get_text(strip=True)]
            if description_list:
                description = " ".join(description_list)
            else:
                description_element = soup.select_one('#productDescription p')
                description = description_element.get_text(strip=True) if description_element else "Product description not found"
        except Exception:
            pass

        # --- Product Details ---
        product_details = {}
        try:
            details_table = soup.select_one('#detailBullets_feature_div')
            if details_table:
                list_items = details_table.select('li')
                for item in list_items:
                    key_element = item.select_one('span.a-text-bold')
                    if key_element:
                        key = key_element.get_text(strip=True).replace(':', '')
                        value = item.get_text(strip=True).replace(key_element.get_text(strip=True), '').strip()
                        product_details[key] = value
            else:
                tech_details = soup.select('#productDetails_techSpec_section_1 tr')
                for row in tech_details:
                    cols = row.select('td, th')
                    if len(cols) == 2:
                        key, value = cols[0].get_text(strip=True), cols[1].get_text(strip=True)
                        product_details[key] = value
        except Exception:
            pass

        # --- Print results ---
        print("\n--- Core Product Info ---")
        print(f"Product Name: {product_name}")
        print(f"Price: {price}")
        print(f"Original Price: {original_price}")
        print(f"Rating: {rating}")
        print(f"Number of Ratings & Reviews: {num_ratings_reviews}")
        print(f"Product Description: {description}")

        print("\n--- Product Details Table ---")
        if product_details:
            for key, value in product_details.items():
                print(f"{key}: {value}")
        else:
            print("Product details table not found or parsed incorrectly.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def scrape_flipkart(url):
    """
    Scrapes a product page from Flipkart.
    """
    print("--- Scraping Flipkart Product Page ---")
    payload = {
        'api_key': FLIPKART_API_KEY,
        'url': url,
        'render': 'true',
        'wait_for_selector': 'h1._6EBuvT',
        'output_format': 'json',
        'autoparse': 'true',
        'country_code': 'in',
        'device_type': 'desktop',
        'max_cost': '50',
        'follow_redirect': 'false',
        'premium': 'true'
    }

    try:
        r = requests.get('https://api.scraperapi.com/', params=payload)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        # --- Extracting Core Product Details ---
        product_name_element = soup.find('h1', class_='_6EBuvT')
        product_name = product_name_element.text.strip() if product_name_element else "Product Name not found"
        
        price_element = soup.find('div', class_='Nx9bqj CxhGGd')
        price = price_element.text.strip() if price_element else "Price not found"
        
        original_price_element = soup.find('div', class_='yRaY8j A6+E6v')
        original_price = original_price_element.text.strip() if original_price_element else "Original Price not found"

        discount_element = soup.find('div', class_='UkUFwK WW8yVX dB67CR')
        discount = discount_element.text.strip() if discount_element else "Discount not found"

        rating_element = soup.find('div', class_='XQDdHH _1Quie7')
        rating = rating_element.text.strip() if rating_element else "Rating not found"
        
        num_ratings_reviews_element = soup.find('span', class_='Wphh3N')
        num_ratings_reviews = num_ratings_reviews_element.text.strip() if num_ratings_reviews_element else "Number of ratings/reviews not found"

        description_element = soup.find('div', class_='_4aGEkW')
        product_description = description_element.text.strip() if description_element else "Product description not found"

        # --- Extracting Product Details from the table ---
        product_details = {}
        details_table_container = soup.find('div', class_='_5Pmv5S')
        if details_table_container:
            detail_rows = details_table_container.find_all('div', class_='row')
            for row in detail_rows:
                key_element = row.find('div', class_='_9NUIO9')
                value_element = row.find('div', class_='-gXFvC')
                if key_element and value_element:
                    key = key_element.text.strip()
                    value = value_element.text.strip()
                    product_details[key] = value

        # --- Print all extracted details ---
        print("\n--- Core Product Info ---")
        print(f"Product Name: {product_name}")
        print(f"Price: {price}")
        print(f"Original Price: {original_price}")
        print(f"Discount: {discount}")
        print(f"Rating: {rating}")
        print(f"Number of Ratings & Reviews: {num_ratings_reviews}")
        print(f"Product Description: {product_description}")

        print("\n--- Product Details Table ---")
        if product_details:
            for key, value in product_details.items():
                print(f"{key}: {value}")
        else:
            print("Product details table not found or parsed incorrectly.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    """
    Main function to run the menu-driven scraper.
    """
    
    while True:
        print("\n--- Web Scraper Menu ---")
        print("1. Scrape a product from Amazon")
        print("2. Scrape a product from Flipkart")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            url = input("Enter the Amazon product URL: ")
            scrape_amazon(url)
        elif choice == '2':
            url = input("Enter the Flipkart product URL: ")
            scrape_flipkart(url)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
