from itemadapter import ItemAdapter
import sqlite3
from .items import ChapterItem, ComicItem


class ComicsNoDuplicatesPipeline:
    def __init__(self):
        self.con = sqlite3.connect('comic.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS comics(
            comic_name TEXT NOT NULL PRIMARY KEY,
            comic_author TEXT,
            comic_info TEXT,
            tags TEXT,
            img_url TEXT,
            comic_url TEXT,
            site TEXT NOT NULL,
            status TEXT
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS chapters(
            comic_name TEXT,
            chapter_name TEXT, 
            chapter_url TEXT NOT NULL,
            image_urls TEXT,
            CONSTRAINT fk_name
            FOREIGN KEY(comic_name)
            REFERENCES comics(comic_name)
        )
        """)
        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS images(
        #     chapter_name TEXT,
        #     image_url TEXT NOT NULL,
        #     CONSTRAINT fk_name
        #     FOREIGN KEY(chapter_name)
        #     REFERENCES comics(chapter_name)
        # )
        # """)

    def process_item(self, item, spider):
        if isinstance(item, ComicItem):
            self.cur.execute("select * from comics where comic_name = ? and site = ?",
                             (item['comicName'], item['site']))
            result = self.cur.fetchone()
            if result:
                spider.logger.warn("Comic already in database: %s" % item['comicName'])
                # self.cur.execute("""
                #     UPDATE comics SET comic_author=?, comic_info=?, tags=?, img_url=?, comic_url=?, status=? WHERE comic_name=?
                # """, (
                #     item['comicAuthor'],
                #     item['comicInfo'],
                #     str(item['tags']),
                #     item['imgUrl'],
                #     item['comicUrl'],
                #     item['status'],
                #     item['comicName'],
                # ))
            else:
                self.cur.execute("""
                    INSERT INTO comics (comic_name, comic_author, comic_info, tags, img_url, comic_url, site, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                                 (
                                     item['comicName'],
                                     item['comicAuthor'],
                                     item['comicInfo'],
                                     str(item['tags']),
                                     item['imgUrl'],
                                     item['comicUrl'],
                                     item['site'],
                                     item['status']
                                 ))
                self.con.commit()
        elif isinstance(item, ChapterItem):
            self.cur.execute("select * from chapters where chapter_url = ?", (item['chapterUrl'],))
            result = self.cur.fetchone()
            if result:
                spider.logger.warn("Chapter already in database: %s" % item['chapterName'])
            else:
                self.cur.execute("""
                                INSERT INTO chapters (comic_name, chapter_name, chapter_url, image_urls) VALUES (?, ?, ?, ?)
                            """,
                                 (
                                     item['comicName'],
                                     item['chapterName'],
                                     item['chapterUrl'],
                                     item['chapterImageUrl'],
                                 ))
                self.con.commit()
        # elif isinstance(item, ChapterImageUrlItem):
        #     self.cur.execute("select * from images where image_url = ?", (item['chapterImageUrl'],))
        #     result = self.cur.fetchone()
        #     if result:
        #         spider.logger.warn("Image already in database: %s" % item['chapterImageUrl'])
        #     else:
        #         self.cur.execute("""
        #                         INSERT INTO chapters (chapter_name, image_url) VALUES (?, ?)
        #                         """,
        #                          (
        #                              item['chapterName'],
        #                              item['chapterImageUrl'],
        #                          ))
        #         self.con.commit()
        else:
            return item
