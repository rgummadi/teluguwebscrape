import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class teluguoneindiaSpider(scrapy.Spider):
    name = "teluguoneindia"
    paperweight = 10
    allowed_domains = ["telugu.oneindia.com"]
    start_urls = ["http://telugu.oneindia.com"]

    def parse(self, response):

        #main news heading 1
        for link in response.xpath('(//h3[@class="main-news-heading"])[1]'):
            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print url[0]

            item['engsource'] = 'teluguoneindia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        #main news heading 2
        for link in response.xpath('(//h3[@class="main-news-heading"])[2]'):
            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print url[0]

            item['engsource'] = 'teluguoneindia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        # vaarthalu
        for link in response.xpath('//div[@class="news-desc"]'):

            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print url[0]

            item['engsource'] = 'teluguoneindia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 9.5

            #yield item

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        #talkoftoday
        for link in response.xpath('//*[@id="telugu-container"]/section/div[2]/ul/li'):

            item = TeluguwebscrapeItem()
            url = link.xpath('div/a/@href').extract()
            print url[0]
            #print "hi"

            item['engsource'] = 'teluguoneindia'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('div/a/text()').extract()
            item['itemweight'] = 9.5

            #yield item

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item,})

    def parse_desc(self, response):
        item = response.meta['item']

        #print response
        item['desc'] = response.xpath('//article/div[@class="ecom-ad-content"]/p/text()').extract()
        desc = item['desc'][0].split()

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
        image_relative_url = response.xpath('//article//div[@class="big_center_img"]/div/img/@src').extract()

        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





