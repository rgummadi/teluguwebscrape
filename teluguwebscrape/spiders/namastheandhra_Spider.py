import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class namastheandhraSpider(scrapy.Spider):
    name = "namastheandhra"
    paperweight = 10
    allowed_domains = ["namastheandhra.com","namastheamerica.com"]
    start_urls = ["http://www.namastheandhra.com"]

    def parse(self, response):
        itemid = 0

        #top left - taja vartalu
        for link in response.xpath('//div[@style="margin-bottom:5px; border-bottom:solid 1px #999999;"]/div[2]/a'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('@href').extract()
            # print url[0]

            item['engsource'] = 'namastheandhra'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3112;&#3118;&#3128;&#3149;&#3108;&#3143; &#3078;&#3074;&#3111;&#3149;&#3120;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item, })

        #bottom -left - all the news items
        for link in response.xpath('//div[@style="padding:5px; "]/div[@class="row-fluid"]/div/div/a'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('@href').extract()
            # print url[0]

            item['engsource'] = 'namastheandhra'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3112;&#3118;&#3128;&#3149;&#3108;&#3143; &#3078;&#3074;&#3111;&#3149;&#3120;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('h3/text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item})

        #special story
        for link in response.xpath('/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/a'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('@href').extract()
            # print url[0]

            item['engsource'] = 'namastheandhra'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3112;&#3118;&#3128;&#3149;&#3108;&#3143; &#3078;&#3074;&#3111;&#3149;&#3120;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('div/text()').extract()
            item['itemweight'] = 10
            #target.write(item['url'] + "\n")

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item})

        #rajakeeyalu
        for link in response.xpath('//div[@style="padding:5px; "][2]/ul[@class="article-array"]/li/a'):
            item = TeluguwebscrapeItem()
            item['itemid'] = itemid
            itemid = itemid + 1
            url = link.xpath('@href').extract()
            # print url[0]

            item['engsource'] = 'namastheandhra'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3112;&#3118;&#3128;&#3149;&#3108;&#3143; &#3078;&#3074;&#3111;&#3149;&#3120;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('text()').extract()

            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item})


    def parse_desc(self, response):
        item = response.meta['item']
        item['desc'] = " "

        #print response

        getdesc = response.xpath('///html/body/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/p[2]/text()')
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract()

        # if not getdesc:
        getdesc = response.xpath('///html/body/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div[2]/text()')
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract()

        getdesc = response.xpath('//div[@class="post"]/p/text()')
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract()

        # item['desc'] = response.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/p[2]/text()')\
        #                 .extract()
        #
        # if not item['desc']:
        #     item['desc'] = response.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div[2]/text()')\
        #         .extract()

        desc = item['desc'].split()

        if len(desc) > 30:
            size = 30
        else:
            size = len(desc) - 1

        item['mindesc'] = ''
        for index in range(size):
            item['mindesc'] = item['mindesc'] + " " + desc[index]

        #target.write(item['desc'][0].encode("utf-8"))
        # print "printing desc"
        # print item['mindesc']

        #getting the image url

        image_relative_url = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]/a/img\
                                            /@src').extract()
        if not image_relative_url:
            image_relative_url = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/p[1]/a/\
            img/@src').extract()

        if not image_relative_url:
            image_relative_url = response.xpath('//div[@class="post"]/p/a/img/@src').extract()

        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





