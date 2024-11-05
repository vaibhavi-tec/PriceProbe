import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

def flipkart_search(name):
    try:
        name1 = name.replace(" ","+")
        flipkart_url = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(flipkart_url, headers=headers)
        print("\nSearching in Flipkart....")
        soup = BeautifulSoup(res.text,'html.parser')

        if soup.select('._4rR01T'):
            flipkart_name = soup.select('._4rR01T')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                flipkart_name = soup.select('._4rR01T')[0].getText().strip()
                print("Flipkart:")
                print(flipkart_name)
                print(flipkart_price)
                print("---------------------------------")
                return flipkart_price
        elif soup.select('.s1Q9rs'):
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip().upper()
            if name.upper() in flipkart_name:
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                flipkart_name = soup.select('.s1Q9rs')[0].getText().strip()
                print("Flipkart:")
                print(flipkart_name)
                print(flipkart_price)
                print("---------------------------------")
                return flipkart_price
        else:
            flipkart_price = '0'
            return flipkart_price
    except Exception as e:
        print("Flipkart: No product found!")
        print("---------------------------------")
        flipkart_price = '0'
        return flipkart_price

def amazon_search(name):
    try:
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon_url = f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(amazon_url, headers=headers)
        print("\nSearching in Amazon...")
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = len(amazon_page)

        for i in range(amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                print("Amazon:")
                print(amazon_name)
                print("₹"+amazon_price)
                print("---------------------------------")
                return amazon_price
        else:
            print("Amazon: No product found!")
            print("---------------------------------")
            amazon_price = '0'
            return amazon_price
    except Exception as e:
        print("Amazon: No product found!")
        print("---------------------------------")
        amazon_price = '0'
        return amazon_price

def convert(a):
    b = a.replace(" ", '')
    c = b.replace("INR", '')
    d = c.replace(",", '')
    f = d.replace("₹", '')
    g = int(float(f))
    return g

def compare_prices(name):
    flipkart_price = flipkart_search(name)
    amazon_price = amazon_search(name)

    if flipkart_price == '0' and amazon_price == '0':
        print("No product found on Flipkart and Amazon!")
        return None, None  # Return None for both lowest_price and urls
    else:
        if flipkart_price != '0':
            print("\nFlipkart Price:", flipkart_price)
            flipkart_price = convert(flipkart_price)

        if amazon_price != '0':
            print("\nAmazon price: ₹", amazon_price)
            amazon_price = convert(amazon_price)

        lst = [int(flipkart_price), int(amazon_price)]
        lst2 = [price for price in lst if price > 0]

        if len(lst2) == 0:
            print("No relative products found on all websites....")
            return None, None  # Return None for both lowest_price and urls
        else:
            min_price = min(lst2)
            print("_")
            print("\nMinimum Price: ₹", min_price)

            price = {
                f'{amazon_price}': f'https://www.amazon.in/{name.replace(" ", "-")}/s?k={name.replace(" ", "+")}',
                f'{flipkart_price}': f'https://www.flipkart.com/search?q={name.replace(" ", "+")}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',
            }

            urls = {
                "Amazon": price.get(f'{amazon_price}'),
                "Flipkart": price.get(f'{flipkart_price}')
            }

            for key, value in price.items():
                if int(key) == min_price:
                    print ('\nURL:', price[key],'\n')

            print("---------------------------------------------------------URLs--------------------------------------------------------------")
            print("Flipkart : \n", price[f'{flipkart_price}'])
            print("\nAmazon : \n", price[f'{amazon_price}'])
            print("---------------------------------------------------------------------------------------------------------------------------")

            return min_price, urls  # Return both lowest_price and urls