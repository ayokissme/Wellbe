import scrapy


class TestingSpider(scrapy.Spider):
    name = 'testing'
    allowed_domains = ['iHerb_spider']
    start_urls = ['https://ru.iherb.com/pr/california-gold-nutrition-gold-c-vitamin-c-1-000-mg-240-veggie-capsules/61865',
                  'https://ru.iherb.com/pr/california-gold-nutrition-immune-4-immune-system-support-60-veggie-capsules/101714']

    def parse(self, response, **kwargs):
        product_details = response.css('div.product-detail-container')
        name = None
        category = None
        brand = None
        price = None
        aver_rating = None
        reviews_count = None
        stock_status = None
        product_size = None
        product_size_type = None
        # description = None
        link = None

        for detail in product_details:
            try:
                name = detail.xpath('//*[@id="name"]').get().split('\n')[1]
                name = [e.strip().replace(' ', ' ') for e in name.split(', ')]
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
                aver_rating = rating[0].split('/')[0]
                reviews_count = rating[1].split()[0]
            except Exception:
                aver_rating = 0
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
                        product_size = text[0]
                        product_size_type = ' '.join(text[1::])
                        break
            except Exception:
                pass

            # try:
            #     description = response.css('.col-md-14 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li::text').getall()
            #     description = [e.replace(' ', ' ') for e in description]
            # except Exception:
            #     pass

            yield {
                'name': name,
                'category': category,
                'brand': brand,
                'price': price,
                'rating': aver_rating,
                'reviews_count': reviews_count,
                'stock_status': stock_status,
                'size': product_size,
                'size_type': product_size_type,
                # 'description': description,
                'link': link,
            }
