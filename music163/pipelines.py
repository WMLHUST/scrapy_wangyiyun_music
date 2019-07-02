# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import threading
from os import path

from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
import logging

from music163 import items, settings


# artist_queue = queue.Queue(maxsize=10000)
# album_queue = queue.Queue(maxsize=10000)

class my_pipeline(object):
    def __init__(self):
        db_path = path.join(settings.DB_PATH, 'music163.db')
        self.conn = sqlite3.connect(db_path)
        pass

    def process_item(self, item, spider):
        logging.debug("item: %s", item)
        cursor = self.conn.cursor()
        try:
            if isinstance(item, items.artist_item):
                row = [item['artist_id'], item['artist_name'], item['artist_alias'],
                    item['album_size'], item['music_size']]
                cursor.execute(r'insert into t_artists values (?, ?, ?, ?, ?)', row)

            elif isinstance(item, items.albums_item):
                # print("item: ", item)
                row = [item['artist_id'], item['artist_name'], item['album_id'], item['album_name'],
                               item['album_comments_id'], item['album_publishTS'], item['album_company'], item['album_size']]
                cursor.execute(r'insert into t_albums values (?, ?, ?, ?, ?, ?, ?, ?)', row)
        except sqlite3.IntegrityError as e:
            pass
        except Exception as e:
            print("item: ", item)
            print('exception: ', e)

        cursor.close()
        self.conn.commit()

    def open_spider(self, spider):
        logging.info("open spider in pipline")

    def close_spider(self, spider):
        logging.info("close spider in pipline")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

class artist_intodb_thread(threading.Thread):
    def run(self) -> None:

        pass

class album_intodb_thread(threading.Thread):
    def run(self) -> None:
        pass
