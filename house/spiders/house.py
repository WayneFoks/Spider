import scrapy


class HouseSpider(scrapy.Spider):
    name = "house"
    start_urls = [
        'https://gz.lianjia.com/ershoufang/pg1/',
    ]

    def parse(self, response):
        for info in response.css("li.clear"):
            yield {
                'title': info.css("div.title > a::text").extract(),
                'price': info.css("div.totalPrice > span::text").extract()
            }
        yield {
            'test': 'test1'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
