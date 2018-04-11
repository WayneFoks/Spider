import scrapy


class HouseSpider(scrapy.Spider):
    name = "house"

    def start_requests(self):
        start_url = 'https://gz.lianjia.com/ershoufang/pg'

        for i in range(1, 2):
            yield scrapy.Request(url=start_url + str(i), callback=self.parse)

    def parse(self, response):
        for info in response.css("li.clear"):
            yield {
                'house_name': info.css("div.houseInfo > a::text").extract_first(),
                'house_link': info.css("div.houseInfo > a::attr(href)").extract_first(),
                'price': info.css("div.totalPrice > span::text").extract_first(),
                'follow': info.css("div.followInfo::text").re('.*')
            }

        # url = self.start_urls
        # yield scrapy.Request(url=url, callback=self.parse)
        # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
