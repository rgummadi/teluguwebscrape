import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class AJSpider(scrapy.Spider):
    name = "AJ"
    paperweight = 10
    allowed_domains = ["andhrajyothy.com"]
    start_urls = ["http://andhrajyothy.com"]

    def parse(self, response):

        #mukhyamsalu
        for link in response.xpath('//*[@id="ContentPlaceHolder1_dlstImpNews"]/tr'):

            item = TeluguwebscrapeItem()
            url = link.xpath('td/div/table/tr/td/a/@href').extract()
            print url[0]


            item['engsource'] = 'andhrajyothy'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3078;&#3074;&#3111;&#3149;&#3120;&#3100;&#3149;&#3119;&#3147;&#3108;&#3135;')

            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('td/div/table/tr/td/a/text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item})

        #marinni mukhyamsalu
        for link in response.xpath('//*[@id="ContentPlaceHolder1_ulOthImpNews"]/li'):

            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print "hi"
            print url[0]


            item['engsource'] = 'andhrajyothy'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3078;&#3074;&#3111;&#3149;&#3120;&#3100;&#3149;&#3119;&#3147;&#3108;&#3135;')

            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 9

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item})


    def parse_desc(self, response):

        item = response.meta['item']
        item['desc'] = " "

        # getdesc = response.xpath('//*[@id="ContentPlaceHolder1_lblStoryDetails"]/div/text()')
        getdesc = response.xpath('//*[@id="ContentPlaceHolder1_lblStoryDetails"]/descendant::*/text()')
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract()

        # if not getdesc:
        getdesc = response.xpath('//*[@id="ContentPlaceHolder1_lblStoryDetails"]/text()')
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract()
        # print item['desc']

        # if not item['desc']:
        #     item['desc'] = response.xpath('//*[@id="ContentPlaceHolder1_lblStoryDetails"]/text()').extract()
        #
        # desc = item['desc'][0].split()
        # #desc = "hello"
        desc = item['desc'].split()
        if len(desc) > 30:
            size = 30
        else:
            size = len(desc) - 1

        item['mindesc'] = ''
        for index in range(size):
            item['mindesc'] = item['mindesc'] + " " + desc[index]

        # #target.write(item['desc'][0].encode("utf-8"))
        # print "printing desc"
        # print item['mindesc']

        #getting the image url

        image_relative_url = response.xpath('//td[@id="ContentPlaceHolder1_tdStoryImg"]/img/@src').extract()


        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





