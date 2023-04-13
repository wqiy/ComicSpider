import scrapy


class A6manhuaSpider(scrapy.Spider):
    name = "6manhua"
    allowed_domains = ["6mh67.com"]
    start_urls = ["http://6mh67.com/rank/1-1.html"]

    def parse(self, response):
        for comic in response.css('div.cy_list_mh ul'):
            yield {
                'title': comic.css('li.title a::text').get(),
                'tags': comic.css('li.biaoqian::text').get(),
                'desc': comic.css('li.info::text').get(),
                'img': comic.css('li a img').attrib['src'],
                'url': comic.css('li a').attrib['href'],
            }