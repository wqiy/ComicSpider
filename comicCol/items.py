# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComiccolItem(scrapy.Item):
    pass


class ComicItem(scrapy.Item):
    comicName = scrapy.Field()
    comicAuthor = scrapy.Field()
    comicInfo = scrapy.Field()
    tags = scrapy.Field()
    imgUrl = scrapy.Field()
    comicUrl = scrapy.Field()
    site = scrapy.Field()


class ChapterItem(scrapy.Item):
    comicName = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
