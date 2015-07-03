import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class webduniaSpider(scrapy.Spider):
    name = "webdunia"
    paperweight = 10
    allowed_domains = ["webdunia.com"]
    start_urls = ["http://telugu.webdunia.com"]

    def parse(self, response):
        itemid = 0
        #get the news from slider
        for link in response.xpath('//*[@id="rotate_pane_305"]/li/div[1]/div/div[1]'):

            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('.//a/@href').extract()
            # print url[0]

            item['engsource'] = 'webdunia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3142;&#3116;&#3149; &#3110;&#3137;&#3112;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('.//a/text()').extract()
            item['itemweight'] = 10

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        #get the imp news
        for link in response.xpath('//*[@id="newCont_306_1"]/div/div[2]/ul/li'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('a/@href').extract()
            # print url[0]

            item['engsource'] = 'webdunia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3142;&#3116;&#3149; &#3110;&#3137;&#3112;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 9

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        #get the important news top item
        for link in response.xpath('//*[@id="newCont_306_1"]/div/div[1]/h2'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('a/@href').extract()
            # print url[0]

            item['engsource'] = 'webdunia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3142;&#3116;&#3149; &#3110;&#3137;&#3112;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 8

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        # get the important news list items
        for link in response.xpath('//*[@id="newCont_306_1"]/div/div[1]/div/ul/li'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('a/@href').extract()
            # print url[0]

            item['engsource'] = 'webdunia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3142;&#3116;&#3149; &#3110;&#3137;&#3112;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 7

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

    def parse_desc(self, response):

        item = response.meta['item']
        item['desc'] = response.xpath('//*[@id="contContainer"]/div[4]/div[1]/div[1]/div[2]/div[6]/div[2]/div/div/div[1]/span/text()').extract()

        if item['desc']:
            desc = item['desc'][0].split()
        else:
            desc = ['']
            item['desc'] = [' ']

        if len(desc) > 30:
            size = 30
        else:
            size = len(desc) - 1

        item['mindesc'] = ''
        for index in range(size):
            item['mindesc'] = item['mindesc'] + " " + desc[index]

        # print "printing desc"
        # print item['mindesc']

        #getting the image url
        image_relative_url = response.xpath('//*[@id="contContainer"]/div[4]/div[1]/div[1]/div[2]/div[6]/div[1]/div[1]/div/img/@src')\
            .extract()

        if not image_relative_url:
            response.xpath('//*[@id="contContainer"]/div[4]/div[1]/div[1]/div[2]/div[6]/div[2]/div/div/div[2]/div/img/@src')\
                .extract()
        if not image_relative_url:
            response.xpath('//*[@id="contContainer"]/div[4]/div[1]/div[1]/div[2]/div[7]/div[2]/div[1]/div/div[2]/div/img/@src')\
                .extract()
        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





