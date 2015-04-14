import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class eenaduSpider(scrapy.Spider):
    name = "eenadu"
    paperweight = 10
    allowed_domains = ["eenadu.net"]
    start_urls = ["http://www.eenadu.net"]

    def parse(self,response):

        target = open('eenadu.txt', 'w')

        for link in response.xpath('//ul[@id="tajanews"]/li'):

            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print url[0]
            print "hi"

            item['engsource'] = 'eenadu'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 10
            target.write(item['url'] + "\n")


            #yield item

            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, 'target': target})

    def parse_desc(self, response):
        item = response.meta['item']
        target = response.meta['target']
        #print response
        item['desc'] = response.xpath('//*[@id="PDSAIbreak"]/font/font/font/text()').extract()
        #item['desc'] = response.xpath('//article/div[@class="ecom-ad-content"]/p/text()').extract()
        desc = item['desc'][0].split()

        if len(desc) > 30:
            size = 30
        else:
            size = len(desc) - 1

        item['mindesc'] = ''
        for index in range(size):
            item['mindesc'] = item['mindesc'] + " " + desc[index]

        #target.write(item['desc'][0].encode("utf-8"))
        print "printing desc"
        print item['mindesc']

        #getting the image url

        image_relative_url = response.xpath('//article//div[@class="big_center_img"]/div/img/@src').extract()

        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





