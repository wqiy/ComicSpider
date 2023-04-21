import scrapy
from comicCol.items import ComicItem, ChapterItem
from scrapy_selenium import SeleniumRequest


class BaozimhSpider(scrapy.Spider):
    name = "baozimh"
    allowed_domains = ["cn.kukuc.co"]

    def start_requests(self):
        base_url = "https://cn.kukuc.co/classify"
        yield SeleniumRequest(
            url=base_url,
            callback=self.parse,
            wait_time=2,
            script="window.scrollTo(0, document.body.scrollHeight*10);"
        )

    def parse(self, response):
        comics = response.css('div.classify-items div')
        for i in range(len(comics)):
            url = "https://cn.kukuc.co{}".format(comics[i].css('a.comics-card__poster').attrib['href'])
            yield SeleniumRequest(
                url=url,
                callback=self.parse_detail,
                wait_time=20,
                script="document.querySelector('#button_show_all_chatper').click()"
            )

    def parse_detail(self, response):
        pass
        comic_item = ComicItem()
        comic_item['site'] = "Baozimh"
        comic_item['comicName'] = str(response.css('h1.comics-detail__title::text').get())
        comic_item['comicAuthor'] = str(response.css('h2.comics-detail__author::text').get())
        comic_item['comicInfo'] = str(response.css('p.comics-detail__desc::text').get())
        comic_item['tags'] = str(list(map(lambda x: x.strip(), response.css('div.tag-list span::text').getall()[1:])))
        comic_item['imgUrl'] = str(response.xpath('//*[@id="layout"]/div[2]/div[1]/div[3]/div/div[1]/amp-img/@src').get())
        comic_item['comicUrl'] = str(response.xpath('/html/head/link[14]/@href').get())
        comic_item['status'] = str(response.xpath('//*[@id="layout"]/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div[1]/span[1]/text()').get())

        yield comic_item
        chapters = response.css('div#chapter-items div')
        comic_name = response.xpath('/html/head/link[14]/@href').get().split("/")[-1]

        for i in range(len(chapters)):
            yield SeleniumRequest(
                url="https://cn.kukuc.co/comic/chapter/{}/0_{}.html".format(comic_name, i),
                callback=self.parse_chapter_detail,
                wait_time=2,
            )

    def parse_chapter_detail(self, response):
        urls = response.css('ul.comic-contain div amp-img')
        chapter_item = ChapterItem()
        chapter_item['comicName'] = str(response.xpath('/html/head/title/text()').get().split()[-3])
        chapter_item['chapterName'] = str(response.css('span.title::text').get())
        chapter_item['chapterUrl'] = str(response.xpath('/html/head/link[14]/@href').get())
        image_urls = []
        for i in range(len(urls)):
            image_urls.append(urls[i].attrib['src'])
        chapter_item['chapterImageUrl'] = str(image_urls)
        yield chapter_item
