import scrapy


class HtmangaSpider(scrapy.Spider):
    name = "htmanga"
    allowed_domains = ["htmanga3.top"]
    start_urls = ["http://htmanga3.top/"]

    def parse(self, response):
        pass
