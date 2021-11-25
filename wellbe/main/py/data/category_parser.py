import requests
from bs4 import BeautifulSoup as bS
import pandas as pd
import json


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
}

# with open('categories_brands.json', 'w', encoding="utf-8") as file:
#     json.dump([], file, indent=5)


def get_iteration(categories):
    iter_dict = {'brands_iter': ..., 'categories_iter': ...}
    for i in range(len(categories) - 1):
        text = categories[i].find("div", "filter-header").text.strip()
        if text == "Категории":
            iter_dict['categories_iter'] = i
        if text == "Бренды":
            iter_dict['brands_iter'] = i
            break
    return iter_dict


def get_category(url):
    response = requests.get(url=url, headers=headers)
    soup = bS(response.content, 'lxml')
    categories = soup.find_all("section", "search-filter")
    category_name = soup.find("div", "sub-header").find("h1", "sub-header-title").text.strip()
    product_data = {category_name: {'category': [], 'brands': [None]}}
    categories_links = []
    try:
        i = get_iteration(categories)
        brands_category = categories[i['brands_iter']].find_all("li", "filter-item")
        brands_text = [e.text.strip() for e in brands_category]
        product_data[category_name]["brands"] = brands_text
        if type(i['categories_iter']) is int:
            categories_html = categories[i['categories_iter']].find_all("div", "filter-name")
            categories_text = [e.text.strip() for e in categories_html]
            product_data[category_name]["categories"] = categories_text
            categories_links = [e.get("href") for e in categories[i['categories_iter']].find_all("a")]

        with open('data/categories_brands.json') as file:
            data = json.load(file)
        data.append(product_data)
        with open('data/categories_brands.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=5)

        for e in categories_links:
            print(e)
            get_category(e)

    except AttributeError:
        print("Страница не найдена")


def main(url):
    get_category(url)
    with open('data/categories_brands.json') as file:
        data = json.load(file)
        for e in data:
            print(e.key)


if __name__ == '__main__':
    main('https://ru.iherb.com/c/vitamins')