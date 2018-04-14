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
        yield {
            'number': self.number,
            '总价': extract_with_css('div.price > span.total::text').extract_first(),
            '单价': extract_with_css('div.unitPrice > span.unitPriceValue::text').extract_first(),
            '行政区': getValueSafely(extract_with_css('div.areaName > span.info > a::text').extract(), 0),
            '小区': getValueSafely(extract_with_css('div.areaName > span.info > a::text').extract(), 1),
            # '建筑面积': extract_with_css('div.area > div.mainInfo::text').extract_first(),
            '建筑面积': getValueSafely(extract_with_css('div.area > div.mainInfo::text')[0].re('(\d*\.*\d*)'), 0),
            # '建筑时间': extract_with_css('div.area > div.subInfo::text').extract_first(),
            '建成时间': getValueSafely(extract_with_css('div.area > div.subInfo::text')[0].re('(\d*)'), 0),
            '建筑类型': getValueSafely(extract_with_css('div.area > div.subInfo::text')[0].extract().split('/'), 1),
            '朝向': extract_with_css('div.type > div.mainInfo::text').extract_first(),
            '小区': extract_with_css('div.communityName > a.info::text').extract_first(),
            # '户型': extract_with_css('div.room > div.mainInfo::text').extract_first(),
            '户型2': response.css('div.introContent').css('div.content').css('li::text')[0].extract(),
            '楼层': extract_with_css('div.room > div.subInfo::text').extract_first(),
            '所在楼层': getValueSafely(extract_with_css('div.room > div.subInfo::text').extract_first().split('/'), 0),
            '总楼层': getValueSafely(extract_with_css('div.room > div.subInfo::text').extract_first().split('/'), 1),
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
            '地铁': extract_with_css('a.is_near_subway::text').extract_first(),
            # '税收': extract_with_css('a.taxfree::text').extract_first(),
        }
