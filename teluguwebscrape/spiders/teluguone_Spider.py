import scrapy
from teluguwebscrape.items import TeluguwebscrapeItem
import urlparse
import HTMLParser


class teluguoneSpider(scrapy.Spider):
    name = "teluguone"
    paperweight = 10
    allowed_domains = ["teluguone.com"]
    start_urls = ["http://teluguone.com/news"]

    def parse(self,response):

        for link in response.xpath('//div[@class="news_thumb_container_main"]//div[@class="telugu_newstitle_txt_12px"]'):
            item = TeluguwebscrapeItem()
            url = link.xpath('a/@href').extract()
            print url[0]
            #print "hi"

            item['engsource'] = 'teluguone'
            absolute_url = urlparse.urljoin(response.url, url[0].strip())
            h = HTMLParser.HTMLParser()
            item['source'] = h.unescape('&#3125;&#3112;&#3149; &#3079;&#3074;&#3105;&#3135;&#3119;&#3134;')
            #print absolute_url
            item['url'] = absolute_url
            item['title'] = link.xpath('a/text()').extract()
            item['itemweight'] = 10

            #yield item
            yield scrapy.http.Request(absolute_url, callback=self.parse_desc, meta={'item': item,})

    def parse_desc(self, response):
        item = response.meta['item']
        item['desc'] = " "
        getdesc = response.xpath('//div[@class="description_box_main"]/descendant::*/text()')
        #print getdesc
        for des in getdesc:
            item['desc'] = item['desc'] + des.extract().strip()
            # print des.extract().strip()
        # print item['desc']

        desc = item['desc'].split()
        # print desc

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

        image_relative_url = response.xpath('//div[@class="description_box_main"]/div/div/div[1]/img/@src').extract()

        if image_relative_url:
            image_relative_url = image_relative_url[0]
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
        else:
            item['image_urls'] = ['']

        return item





