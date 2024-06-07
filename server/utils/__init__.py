import json
from scrapy.crawler import CrawlerProcess
from .scrapper.spider import spider

class Utils:
    def scrape_data(self):

        exec = spider.DynamicSpider

        process = CrawlerProcess(settings={})
        process.crawl(spider.DynamicSpider)
        process.start()

        # scraped_data = []

        # for item in exec.items:
        #     scraped_data.append(dict(item))

#       return json.dumps(scrapped_data)
        return exec.items