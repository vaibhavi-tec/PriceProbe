import requests

from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_price(url, product_name):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Search for price based on product name
        product_elements = soup.find_all(lambda tag: product_name.upper() in tag.text.strip().upper())
        for element in product_elements:
            price_element = element.find_next_sibling(lambda tag: re.search(r'\bprice\b', tag.name, re.IGNORECASE))
            if price_element:
                return price_element.text.strip().replace(',', '')

        # If not found by product name, search for generic price elements
        price_elements = soup.find_all(lambda tag: re.search(r'\bprice\b', tag.name, re.IGNORECASE))
        for element in price_elements:
            price = element.text.strip().replace(',', '')
            if price:
                return price

        return None
    except requests.exceptions.RequestException as e:
        print(f"Error in {url}: {e}")
        return None

def get_flipkart_price(name):
    try:
        name1 = name.replace(" ", "+")
        url = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        print("\nSearching in Flipkart....")
        soup = BeautifulSoup(res.text, 'html.parser')

        if soup.select('._4rR01T'):
            flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                print("Flipkart:")
                print(flipkart_name)
                print(flipkart_price)
                print("---------------------------------")
                return int(float(flipkart_price.replace("₹", "").replace(",", "")))

        elif soup.select('.s1Q9rs'):
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                print("Flipkart:")
                print(flipkart_name)
                print(flipkart_price)
                print("---------------------------------")
                return int(float(flipkart_price.replace("₹", "").replace(",", "")))

        else:
            print("Flipkart: No product found!")
            print("---------------------------------")
            return -1  # Return -1 if the product is not found

    except Exception as e:
        print(f"Error in Flipkart: {e}")
        print("---------------------------------")
        return -1  # Return -1 in case of an error

def get_amazon_price(name):
    try:
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        url = f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        print("\nSearching in Amazon...")
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = len(amazon_page)

        for i in range(amazon_page_length):
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name.upper() in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                print("Amazon:")
                print(amazon_name)
                print("₹" + amazon_price)
                print("---------------------------------")
                return int(float(amazon_price.replace("₹", "").replace(",", "")))

        print("Amazon: No product found!")
        print("---------------------------------")
        return -1  # Return -1 if the product is not found

    except Exception as e:
        print(f"Error in Amazon: {e}")
        print("---------------------------------")
        return -1  # Return -1 in case of an error

def get_croma_price(name):
    try:
        name1 = name.replace(" ", "-")
        url = f'https://www.croma.com/search/?text={name1}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        print("\nSearching in Croma....")
        soup = BeautifulSoup(res.text, 'html.parser')

        if soup.select('.product-title'):
            croma_name = soup.select('.product-title')[0].getText().strip().upper()
            if name.upper() in croma_name:
                croma_price = soup.select('.price span')[0].getText().strip()
                print("Croma:")
                print(croma_name)
                print(croma_price)
                print("---------------------------------")
                return int(float(croma_price.replace("₹", "").replace(",", "")))
        else:
            print("Croma: No product found!")
            print("---------------------------------")
            return -1  # Return -1 if the product is not found

    except Exception as e:
        print(f"Error in Croma: {e}")
        print("---------------------------------")
        return -1  # Return -1 in case of an error

def convert(a):
    b = a.replace(" ", '')
    c = b.replace("INR", '')
    d = c.replace(",", '')
    f = d.replace("₹", '')
    g = int(float(f))
    return g

def compare_prices(product_name):
    try:
        flipkart_price = get_flipkart_price(product_name)
        amazon_price = get_amazon_price(product_name)
        croma_price = get_croma_price(product_name)

        prices = {'Flipkart': flipkart_price, 'Amazon': amazon_price, 'Croma': croma_price}

        if all(price == -1 for price in prices.values()):
            return "No product found on Flipkart, Amazon, or Croma.", {}

        # Filter prices greater than 0
        valid_prices = [price for price in prices.values() if price is not None and price > 0]

        if not valid_prices:
            return "No relative product found on all three websites.", {}

        lowest_price = min(valid_prices)

        # Create a dictionary with URLs
        urls = {'Flipkart': f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}',
                'Amazon': f'https://www.amazon.in/{product_name.replace(" ", "-")}/s?k={product_name.replace(" ", "+")}',
                'Croma': f'https://www.croma.com/search/?text={product_name.replace(" ", "-")}'}

        # Print the minimum price and corresponding URL
        print("___________")
        print(f"\nMinimum Price: ₹{lowest_price}")
        for platform, price in prices.items():
            if price == lowest_price:
                print(f"{platform} URL: {urls[platform]}\n")

        print("---------------------------------------------------------URLs--------------------------------------------------------------")
        print("Flipkart : \n", urls['Flipkart'])
        print("\nAmazon : \n", urls['Amazon'])
        print("\nCroma : \n", urls['Croma'])
        print("---------------------------------------------------------------------------------------------------------------------------")

        return lowest_price, prices

    except Exception as e:
        print(f"Error in comparing prices: {e}")
        return "An error occurred while comparing prices. Please try again.", {}

def main():
    print("Welcome to the E-commerce Price Comparison Chatbot!")

    while True:
        user_input = input(">> ").strip()

        if any(word in user_input.lower() for word in ["bye", "see you later", "goodbye"]):
            print("Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!")
            break
        elif any(word in user_input.lower() for word in ["nice chatting to you, bye", "see you till next time", "exit"]):
            print("Bye! Have a nice day, come back again soon.")
            break

        # Rule 2
        if any(word in user_input.lower() for word in ["hi", "hey", "hello", "hola", "good day"]):
            print("Hello, thanks for asking!")
        elif any(word in user_input.lower() for word in ["hi there", "is anyone there?"]):
            print("Hi there, how can I help?")
        elif any(word in user_input.lower() for word in ["how are you"]):
            print("I am fine, how are you?")
        elif any(word in user_input.lower() for word in ["hi there"]):
            print("Good to see you again!")

        # Rule 3
        if any(word in user_input.lower() for word in ["how you could help me?", "what you can do?", "what help you provide?", "how you can be helpful?", "what support is offered"]):
            print("I can guide you through different websites and find great offers for the products you want to buy.")
        elif any(word in user_input.lower() for word in ["help", "support", "guide"]):
            print("Offering support to get the best deal out of your purchase.")

        # Rule 4
        if any(word in user_input.lower() for word in ["websites", "which are the websites do you compare the products with", "which are the websites do you compare with?", "how many website sdo u compare with?", "website names"]):
            print("Comparing products from Flipkart, Amazon, and Croma...")

        # Rule 5
        if any(word in user_input.lower() for word in ["find best deal"]):
            print("Sure, please provide me with the product names or keywords you want to compare.")
        elif any(word in user_input.lower() for word in ["compare products", "product comparison", "which one is better", "compare"]):
            product_name = input("What product would you like to compare prices for?\n").strip()

            lowest_price, prices = compare_prices(product_name)

            if isinstance(lowest_price, str):
                print(lowest_price)
            else:
                print(f"The lowest price found is ₹{lowest_price}.")

            # Rule 6
            print("________________________")
            print("Here are the URLs for your comparison:")
            print("Flipkart:", f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}')
            print("Amazon:", f'https://www.amazon.in/{product_name.replace(" ", "-")}/s?k={product_name.replace(" ", "+")}')
            print ("Croma:", f'https://www.croma.com/search/?text={product_name.replace(" ", "-")}')
            print("________________________")

            # Rule 9
            more_queries = input("Would you like to compare prices for another product? (yes/no)\n").lower()
            if any(word in more_queries for word in ["no", "bye", "see you later", "goodbye"]):
                # Rule 7
                print("Bye! Have a nice day, come back again soon.")
                break
            elif any(word in more_queries for word in ["nice chatting to you, bye", "see you till next time", "exit"]):
                print("Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!")
                break
            else:
                print("See you!")

        # Rule 8
        if any(word in user_input.lower() for word in ["thanks", "thank you", "that's helpful", "awesome, thanks", "thanks for helping me"]):
            print("Happy to help!")

if __name__ == "__main__":
    main()