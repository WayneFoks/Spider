import scrapy


class HouseSpider(scrapy.Spider):
    name = "house"
    number = 0

    def start_requests(self):
        start_url = 'https://gz.lianjia.com/ershoufang/pg'

        for i in range(1, 2):  # 643.4
            yield scrapy.Request(url=start_url + str(i), callback=self.parse)

    def parse(self, response):
        for info in response.css("li.clear"):
            next_page = info.css('div.title > a::attr(href)').extract_first()
            if next_page is not None:
                # next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_house)
            break  # todo

    def parse_house(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        self.number += 1
        yield {
            'number': self.number,
            'total': extract_with_css('div.price > span.total::text'),
            'unit_price': extract_with_css('div.unitPrice > span.unitPriceValue::text'),
            'area': extract_with_css('div.area > div.mainInfo::text'),
            'year': extract_with_css('div.area > div.subInfo::text'),
            'direction': extract_with_css('div.type > div.mainInfo::text'),
            'community': extract_with_css('div.communityName > a.info::text'),
            'room_inner': extract_with_css('div.room > div.mainInfo::text'),
            'room_outside': extract_with_css('div.room > div.subInfo::text'),
            'house_type': response.css('div.introContent').css('div.content').css('li::text')[0].extract(),
            'floor': response.css('div.introContent').css('div.content').css('li::text')[1].extract(),
            'decorate': response.css('div.introContent').css('div.content').css('li::text')[8].extract(),
            'area_rate': response.css('div.introContent').css('div.content').css('li::text')[9].extract(),
            'elevator': response.css('div.introContent').css('div.content').css('li::text')[10].extract(),
            'property': response.css('div.introContent').css('div.content').css('li::text')[11].extract(),
            'up_time': response.css('div.introContent').css('div.transaction').css('li')[0].css('span::text')[
                1].extract(),
            'house_type2': response.css('div.introContent').css('div.transaction').css('li')[3].css(
                'span::text')[1].extract(),
            'house_own_year': response.css('div.introContent').css('div.transaction').css('li')[4].css(
                'span::text')[1].extract(),

        }
