import concurrent.futures
import requests
from bs4 import BeautifulSoup

from utils import convert_to_latin, save_json


def parse_pages(page, URL):
    try:
        data_list = []

        print(f"Scraping page {page}...")
        page_url = f'{URL}page/{page}/'

        response = requests.get(url=page_url)
        soup = BeautifulSoup(response.content, 'html5lib')
        content_product = soup.find_all('div', {'class': 'content-product'})

        for product_div in content_product:
            product_name = product_div.h2.text.strip()
            product_link = product_div.h2.a['href']
            price_span = product_div.find('span', {'class': 'price'})

            if not price_span or product_div.find('p', {'class': 'stock out-of-stock'}):
                product_price = None
            elif price_span.find('ins'):
                product_price = price_span.find('ins').bdi.text
                product_price = convert_to_latin(number=product_price)
            else:
                bdi = price_span.find_all('bdi')
                min_price = convert_to_latin(number=bdi[0].text)
                max_price = convert_to_latin(number=bdi[1].text)
                product_price = f"{min_price}, {max_price}"

            data_list.append({
                'name': product_name,
                'link': product_link,
                'price': product_price
            })

        return data_list
    except Exception as ex:
        print(f"Exception Error: {ex}")


def parse_category(*, URL: str) -> list:
    response = requests.get(url=URL)
    soup = BeautifulSoup(response.content, 'html5lib')

    page_links = soup.find('ul', {'class': 'page-numbers'}).find_all('a')
    num_pages = int(page_links[-2].text)

    results = []

    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        futures = [ex.submit(parse_pages, page, URL) for page in range(1, num_pages+1)]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            results.extend(res)

        return results


URL = "https://xiaomi360.ir"
response = requests.get(url=URL)
soup = BeautifulSoup(response.content, 'html5lib')
ul_category = soup.find('ul', {'class': 'menu'})
li_categories = ul_category.find_all('li', {'class': 'menu-item'})

categories = {}

for category in li_categories:
    name = category.a.text
    url = category.a['href']

    categories[name] = url

for name, url in categories.items():
    print(f"Crawling {name} is starting!")
    data = parse_category(URL=url)
    print(f"Crawling {name} finished!")

    print(f"Saving {name} to json is starting!")
    save_json(data=list(data), file_name=name)
    print(f"Saving {name} to json finished!")

    print("x"*30)
