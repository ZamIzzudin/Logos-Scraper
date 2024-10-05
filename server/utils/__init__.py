from scrapy.crawler import CrawlerProcess
from .scrapper.spider import spider

class Utils:
    def scrape_data(self):

        exec = spider.DynamicSpider

        process = CrawlerProcess(settings={})
        process.crawl(spider.DynamicSpider)
        process.start()

        return exec.items