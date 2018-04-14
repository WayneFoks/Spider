import scrapy

# 在house工程目录下执行
# cd house
# scrapy crawl house -s JOBDIR=./crawls/somespider-1

class HouseSpider(scrapy.Spider):
    name = "house"
    number = 0
    debug = True

    def start_requests(self):
        start_url = 'https://gz.lianjia.com/ershoufang/pg'

        last_page = 2 if self.debug else 644
        for i in range(1, last_page):  # 643.4
            print('wayne state: page - ' + str(i))
            yield scrapy.Request(url=start_url + str(i), callback=self.parse)

    def parse(self, response):
        for info in response.css("li.clear"):
            next_page = info.css('div.title > a::attr(href)').extract_first()
            if next_page is not None:
                # next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_house)
            if self.debug:
                break  # todo

    def parse_house(self, response):
        def extract_with_css(query):
            return response.css(query)

        self.number += 1
        yield {
            'number': self.number,
            '总价': extract_with_css('div.price > span.total::text').extract(),
            '单价': extract_with_css('div.unitPrice > span.unitPriceValue::text').extract(),
            '建筑面积': extract_with_css('div.area > div.mainInfo::text').extract(),
            '建筑面积1': extract_with_css('div.area > div.mainInfo::text').re('^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$'),
            '建筑时间': extract_with_css('div.area > div.subInfo::text').extract(),
            '建筑时间1': extract_with_css('div.area > div.subInfo::text').re('^[1-9]\d*|0$'),
            '朝向': extract_with_css('div.type > div.mainInfo::text').extract(),
            '小区': extract_with_css('div.communityName > a.info::text').extract(),
            '户型': extract_with_css('div.room > div.mainInfo::text').extract(),
            '户型2': response.css('div.introContent').css('div.content').css('li::text')[0].extract(),
            '楼层': extract_with_css('div.room > div.subInfo::text').extract(),
            # '楼层2': extract_with_css('div.room > div.subInfo::text').extract(),
            '装修': response.css('div.introContent').css('div.content').css('li::text')[8].extract(),
            '梯户比': response.css('div.introContent').css('div.content').css('li::text')[9].extract(),
            '电梯': response.css('div.introContent').css('div.content').css('li::text')[10].extract(),
            '产权年限': response.css('div.introContent').css('div.content').css('li::text')[11].extract(),
            '更新时间': response.css('div.introContent').css('div.transaction').css('li')[0].css('span::text')[
                1].extract(),
            '房屋用途': response.css('div.introContent').css('div.transaction').css('li')[3].css(
                'span::text')[1].extract(),
            '房屋年限': response.css('div.introContent').css('div.transaction').css('li')[4].css(
                'span::text')[1].extract(),
            '地铁': extract_with_css('div.showbasemore > a.is_near_subway::text').extract(),
            '税收': extract_with_css('div.showbasemore > a.taxfree::text').extract(),

        }
