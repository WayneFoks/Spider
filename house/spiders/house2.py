import scrapy


# 在house工程目录下执行
# cd house
# scrapy crawl house2 -s JOBDIR=./crawls/somespider-1

class HouseSpider2(scrapy.Spider):
    name = "house2"
    number = 0
    debug = True

    def start_requests(self):
        start_url = 'https://gz.lianjia.com/chengjiao/pg'

        last_page = 2 if self.debug else 644
        for i in range(1, last_page):  # 643.4
            print('wayne state: page - ' + str(i))
            yield scrapy.Request(url=start_url + str(i), callback=self.parse)

    def parse(self, response):
        for info in response.css("ul.listContent > li"):
            next_page = info.css('div.title > a::attr(href)').extract_first()
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse_house)
            if self.debug:
                break

    def parse_house(self, response):
        def extract_with_css(query):
            return response.css(query)

        def getValueSafely(list, index):
            if len(list) > index:
                return list[index]
            else:
                return ""

        self.number += 1
        try:
            yield {
                'number': self.number,
                '出售价': extract_with_css('span.dealTotalPrice > i::text').extract_first().strip(),
                '挂牌价': getValueSafely(extract_with_css('div.msg').css('span > label::text').extract(), 0).strip(),
                '单价': extract_with_css('div.price > b::text').extract_first().strip(),
                '行政区': getValueSafely(extract_with_css('div.deal-bread > a::text').extract(), 2).replace('二手房成交价格', ''),
                '小区': getValueSafely(extract_with_css('div.house-title > div::text').extract_first().split(' '),
                                     0).strip(),
                '建筑面积': getValueSafely(
                    response.css('div.introContent').css('div.content').css('li::text')[2].re('(\d*\.*\d*)'),
                    0).strip(),
                '建筑类型': response.css('div.introContent').css('div.content').css('li::text')[5].extract().strip(),
                '建成时间': response.css('div.introContent').css('div.content').css('li::text')[7].extract().strip(),
                '朝向': response.css('div.introContent').css('div.content').css('li::text')[6].extract().strip(),
                '户型2': response.css('div.introContent').css('div.content').css('li::text')[0].extract().strip(),
                '楼层': response.css('div.introContent').css('div.content').css('li::text')[1].extract().strip(),
                '所在楼层': getValueSafely(
                    response.css('div.introContent').css('div.content').css('li::text')[1].extract().split("("),
                    0).strip(),
                '总楼层': getValueSafely(
                    response.css('div.introContent').css('div.content').css('li::text')[1].re('共(\d*)层'),
                    0).strip(),
                '装修': response.css('div.introContent').css('div.content').css('li::text')[8].extract().strip(),
                '梯户比': response.css('div.introContent').css('div.content').css('li::text')[11].extract().strip(),
                '电梯': response.css('div.introContent').css('div.content').css('li::text')[13].extract().strip(),
                '产权年限': response.css('div.introContent').css('div.content').css('li::text')[12].extract().strip(),
                '成交时间': response.css('p.record_detail::text').extract_first().split(',')[2],
                '房屋用途': response.css('div.introContent').css('div.transaction').css('li::text')[3].extract().strip(),
                '房屋年限': response.css('div.introContent').css('div.transaction').css('li::text')[4].extract().strip(),
                '地铁': extract_with_css('a.is_near_subway::text').extract_first(),
                '税收': extract_with_css('a.taxfree::text').extract_first(),
            }
        except BaseException as err:
            yield {
                'number': self.number,
                'exception': err
            }
