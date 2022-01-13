import mysql.connector
from scrapy.crawler import CrawlerProcess
import scrapy


class TestingSpider(scrapy.Spider):
    name = 'testing'
    allowed_domains = ['iHerb_spider']
    start_urls = ['https://ru.iherb.com/pr/a-taste-of-thai-garlic-chili-pepper-sauce-7-fl-oz-207-ml/112059',
                  'https://ru.iherb.com/pr/a-taste-of-thai-sweet-chili-sauce-7-fl-oz-207-ml/112074',
                  'https://ru.iherb.com/pr/a-taste-of-thai-fish-sauce-7-fl-oz-207-ml/112063',
                  'https://ru.iherb.com/pr/a-taste-of-thai-peanut-satay-sauce-7-fl-oz-207-ml/112071']

    def parse(self, response, **kwargs):
        product_details = response.css('div.product-detail-container')
        name = None
        category = None
        brand = None
        price = None
        rating = None
        reviews_count = None
        stock_status = None
        size = None
        size_type = None
        # description = None
        link = None

        for detail in product_details:
            try:
                name = detail.xpath('//*[@id="name"]').get().split('\n')[1].strip()
                # name = [e.strip().replace(' ', ' ') for e in name.split(', ')]
            except Exception:
                pass

            try:
                price = detail.css('div.price::text').get().strip().replace('₽', '').replace(',', '')
            except Exception:
                pass

            try:
                link = response.request.url
            except Exception:
                pass

            try:
                bread_crumbs = response.css('#breadCrumbs')
                is_brand = bread_crumbs.css('a:nth-child(1)::text').get().strip()
                if is_brand == 'Бренды А-Я':
                    brand = bread_crumbs.css('a.last:nth-child(2)::text').get()
                else:
                    brand = list(name)[0]
                category = [e.replace(' ', ' ') for e in bread_crumbs.css('a::text').getall() if e != brand and e != 'Категории' and e != 'Бренды А-Я']
            except Exception:
                pass

            try:
                rating = detail.css('a.stars::attr(title)').get().split('-')
                rating = rating[0].split('/')[0]
                reviews_count = rating[1].split()[0]
                if reviews_count == '.':
                    reviews_count = 0
            except Exception:
                rating = 0
                reviews_count = 0

            try:
                in_stock = detail.css('strong.text-primary::text').get()
                if in_stock is not None:
                    stock_status = 1
                elif in_stock is None:
                    stock_status = 0
            except Exception:
                pass

            try:
                size = detail.css('#product-specs-list > li').getall()
                for i in range(len(size)):
                    text = str(detail.css(f'#product-specs-list > li:nth-child({i})::text').get())
                    if 'Количество в упаковке' in text:
                        text = text.split(':')[1].strip().split()
                        size = text[0]
                        size_type = ' '.join(text[1::])
                        break
            except Exception:
                pass

            # try:
            #     description = response.css('.col-md-14 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li::text').getall()
            #     description = [e.replace(' ', ' ') for e in description]
            # except Exception:
            #     pass

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="2002",
            )
            print(f'values ("{name}", {price}, {rating}, {reviews_count}, {stock_status}, {size}, "{size_type}", "{link}");')
            cursor = db.cursor()
            # cursor.execute('use wellbe;')
            cursor.execute('use wellbe;'
                           'insert into product (name, price, rating, reviews_count, stock_status, size, size_type, link) '
                           f'values ("{name}", {price}, {rating}, {reviews_count}, {stock_status}, {size}, "{size_type}", "{link}");')
            db.commit()
            print(1)
            #
            # product_id = cursor.execute(f'select id from product where name = "{ name }";')
            #
            # for cat in category:
            #     cursor.execute('use wellbe;').execute('insert into category (name, product_id) '
            #                    f'values ("{cat}", {product_id});')
            # db.commit()
            #
            # cursor.execute('use wellbe;').execute('insert into category (name, product_id) '
            #                f'values ("{brand}", {product_id});')
            # db.commit()

            # print({
            #     'name': name,
            #     'category': category,
            #     'brand': brand,
            #     'price': price,
            #     'rating': rating,
            #     'reviews_count': reviews_count,
            #     'stock_status': stock_status,
            #     'size': size,
            #     'size_type': size_type,
            #     # 'description': description,
            #     'link': link,
            # })


class StartSpider:
    process = CrawlerProcess()
    process.crawl(TestingSpider)
    process.start()
