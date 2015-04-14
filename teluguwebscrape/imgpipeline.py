from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request


class MyImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            if image_url:
                yield Request(image_url)
     
    def item_completed(self, results, item, info):
        #print results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            item['image_path'] = [" "]
            #raise DropItem("Item contains no images")
        else:
            imagename = image_paths[0].split("/")
            item['image_path'] = imagename[1]

        return item