import scrapy
from comicCol.items import ComicItem

class BaozimhSpider(scrapy.Spider):
    name = "baozimh"
    allowed_domains = ["baozimh.com"]
    start_urls = ["http://baozimh.com/"]

    def parse(self, response):
        comics = response.xpath('//*[@id="layout"]/div[2]/div[1]/div/div[2]/div')
        for comic in comics:
            comic_item = ComicItem()
            comic_item['comicName'] = comic.css('div.comics-card__title::text').get()
            comic_item['tags'] = list(map(lambda x: x.strip(), comic.css('div.comics-card span.tab::text').getall()))
            comic_item['imgUrl'] = comic.css('div.comics-card a > amp-img').attrib['src']
            comic_item['comicUrl'] = "http://baozimh.com{}".format(comic.css('div.comics-card a').attrib['href'])
            comic_item['site'] = "Baozi"
            yield comic_item
            # yield {
            #     'title': comic.css('div.comics-card__title::text').get(),
            #     'tags': comic.css('div.comics-card span.tab::text').getall(),
            #     'imgUrl': comic.css('div.comics-card a > amp-img').attrib['src'],
            #     'comicUrl': comic.css('div.comics-card a').attrib['href']
            # }
    # def parse_recommend(self, response):


