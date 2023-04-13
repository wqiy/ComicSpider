import scrapy
import json


class CopycomicSpider(scrapy.Spider):
    name = "copycomic"
    allowed_domains = ["copymanga.site"]
    start_urls = ["http://copymanga.site/comics?ordering=-datetime_updated&offset=0&limit=50"]

    def parse(self, response):
        for comic in json.loads(response.css("div.exemptComic-box").attrib['list'].replace("'", "\"")):
            yield {
                'title': comic['name'],
                'tags': "",
                'comicUrl': comic['path_word'],
                'imgUrl': comic['cover'],
            }
        next_page = response.css('li.page-all-item a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
