from itemadapter import ItemAdapter
from .items import ComicItem, ChapterItem
import sqlite3


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
            comic_url TEXT NOT NULL,
            site TEXT NOT NULL
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS details(
            comic_name TEXT,
            chapter_name TEXT NOT NULL PRIMARY KEY, 
            chapter_url TEXT NOT NULL,
            CONSTRAINT fk_name
            FOREIGN KEY(comic_name)
            REFERENCES comics(comic_name)
        )
        """)

    def process_item(self, item, spider):
        if isinstance(item, ComicItem):
            self.cur.execute("select * from comics where comic_name = ? and site = ?",
                             (item['comicName'], item['site']))
            result = self.cur.fetchone()
            if result:
                spider.logger.warn("Comic already in database: %s" % item['comicName'])
            else:
                self.cur.execute("""
                    INSERT INTO comics (comic_name, comic_author, comic_info, tags, img_url, comic_url, site) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                                 (
                                     item['comicName'],
                                     item['comicAuthor'],
                                     item['comicInfo'],
                                     str(item['tags']),
                                     item['imgUrl'],
                                     item['comicUrl'],
                                     item['site']
                                 ))
                self.con.commit()
        elif isinstance(item, ChapterItem):
            self.cur.execute("select * from details where chapter_name = ?", (item['chapterName'],))
            result = self.cur.fetchone()
            if result:
                spider.logger.warn("Chapter already in database: %s" % item['chapterName'])
            else:
                self.cur.execute("""
                                INSERT INTO details (comic_name, chapter_name, chapter_url) VALUES (?, ?, ?)
                            """,
                                 (
                                     item['comicName'],
                                     item['chapterName'],
                                     item['chapterUrl'],
                                 ))
                self.con.commit()
        else:
            return item