import scrapy
from scrapy.crawler import CrawlerProcess
import mysql.connector


class ProductSpider(scrapy.Spider):
    name = 'products'
    start_urls = ['https://ru.iherb.com/c/vitamins']
    db = ...

    def start_requests(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="2002",
            )

            with self.db.cursor() as cursor:
                cursor.execute('use wellbe;')
                cursor.execute('delete from category')
                cursor.execute('delete from product')
                cursor.execute('ALTER TABLE product AUTO_INCREMENT=1;')
                self.db.commit()

            print('successfully')
            for link in self.start_urls:
                yield scrapy.Request(link, callback=self.parse)
        except Exception as e:
            print(e)

    def parse(self, response, **kwargs):
        print(response)
        for product in response.css('div.product-cell-container'):
            product_link = product.css('a.product-link::attr(href)').get()
            yield response.follow(product_link, callback=self.parse_product)

        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
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
                category = set([e.replace(' ', ' ') for e in bread_crumbs.css('a::text').getall() if e != brand and e != 'Категории' and e != 'Бренды А-Я'])
            except Exception:
                pass

            try:
                rating_tag = detail.css('a.stars::attr(title)').get().split('-')
                rating = rating_tag[0].split('/')[0]
                reviews_count = rating_tag[1].split()[0]
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

            try:
                with self.db.cursor(buffered=True) as cursor:

                    print(f'insert into product (name, brand, price, rating, reviews_count, stock_status, size, size_type, link) '
                          f'values ("{name}", "{brand}", {price}, {rating}, {reviews_count}, {stock_status}, {size}, "{size_type}", "{link}");')
                    cursor.execute('use wellbe;')
                    cursor.execute('insert into product (name, brand, price, rating, reviews_count, stock_status, size, size_type, link) '
                                   f'values ("{name}", "{brand}", {price}, {rating}, {reviews_count}, {stock_status}, {size}, "{size_type}", "{link}");')
                    cursor.execute(f'select id from product where name = "{name}" limit 1')
                    product_id = cursor.fetchone()[0]
                    print(product_id)
                    for cat in category:
                        cursor.execute('insert into category (name, product_id) '
                                       f'values ("{cat}", {product_id});')
                    self.db.commit()
            except Exception as e:
                print('#' * 50 + '\n')
                print(e, '-' * 20)
                print('\n' + '#' * 50)


class StartSpider:
    process = CrawlerProcess()
    process.crawl(ProductSpider)
    process.start()
