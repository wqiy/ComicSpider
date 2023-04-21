import jsbeautifier
import scrapy
from comicCol.items import ComicItem
from comicCol.items import ChapterItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class A6manhuaSpider(scrapy.Spider):
    name = "6manhua"
    allowed_domains = ["6mh67.com"]
    base_url = "http://www.6mh67.com/rank/1-{}.html"

    def start_requests(self):
        for page in range(1, 2):
            url = self.base_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    # get comic url
    def parse(self, response):
        comics = response.css('div.cy_list_mh ul')
        for i in range(len(comics)):
            url = "http://www.6mh67.com{}".format(comics[i].css('li.title a').attrib['href'])
            yield SeleniumRequest(
                url=url,
                callback=self.parse_detail,
                wait_time=20,
                script="document.querySelector('#zhankai').click()"
            )

    # get comic info and chapter url
    def parse_detail(self, response):
        comic_item = ComicItem()
        comic_item['site'] = '6manhua'
        comic_item['comicName'] = str(response.css('div.cy_title h1::text').get())
        comic_item['comicAuthor'] = str(response.xpath('//*[@id="intro_l"]/div[3]/span[1]/text()').get()[3:])
        comic_item['comicInfo'] = str(response.xpath('//*[@id="comic-description"]/text()').get())
        comic_item['tags'] = str(response.xpath('//*[@id="intro_l"]/div[4]/span[2]/text()').get()[3:])
        comic_item['imgUrl'] = str(response.xpath('//*[@id="intro_l"]/div[1]/img/@src').get())
        comic_item['comicUrl'] = "http://www.6mh67.com/{}/".format(
            response.xpath('//*[@id="intro_l"]/div[6]/div[1]/a/@href').get().split("/")[1])
        comic_item['status'] = str(response.xpath('//*[@id="intro_l"]/div[3]/span[2]/font/text()').get())

        yield comic_item
        chapters = response.css('div.cy_plist ul li')

        for chapter in chapters:
            yield SeleniumRequest(
                url="http://www.6mh67.com{}".format(chapter.css('a').attrib['href']),
                callback=self.parse_chapter_detail,
                wait_time=2,
            )

    # get chapter info and image urls
    def parse_chapter_detail(self, response):
        script = response.xpath('/html/body/script[2]/text()').get()
        urls = jsbeautifier.beautify(script).replace("var newImgs = [", "").replace('"]', "").strip().split(",")
        chapter_item = ChapterItem()
        chapter_item['comicName'] = str(response.css('a#chapter::text').get())
        chapter_item['chapterName'] = str(response.css('h1.chaptername_title::text').get())
        chapter_item['chapterUrl'] = str(response.xpath('/html/head/meta[5]/@content').get())
        image_urls = []
        for url in urls:
            image_urls.append(url.strip().strip('"'))
        chapter_item['chapterImageUrl'] = str(image_urls)

        yield chapter_item

        # url_item = ChapterImageUrlItem()
        # script = response.xpath('/html/body/script[2]/text()').get()
        # urls = jsbeautifier.beautify(script).replace("var newImgs = [", "").replace('"]', "").strip().split(",")
        # url_item['chapterName'] = response.css('h1.chaptername_title::text').get()
        #
        # url_item['chapterImageUrl'] = urls
        # yield url_item
