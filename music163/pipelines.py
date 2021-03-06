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
from .spiders import db_pool


class my_pipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        logging.debug("item: %s", item)
        conn = db_pool.pool.connection()
        cursor = conn.cursor()
        try:
            if isinstance(item, items.artist_item):
                row = [item['artist_id'], item['artist_name'], item['artist_alias'],
                       item['album_size'], item['music_size'], item['artist_name'],
                       item['artist_alias'], item['album_size'], item['music_size']]
                cursor.execute(r'insert into t_artists values (%s, %s, %s, %s, %s) on duplicate key update f_name=%s, f_alias=%s, f_album_size=%s, f_music_size=%s',
                               row)

            elif isinstance(item, items.albums_item):
                # print("item: ", item)
                row = [item['artist_id'], item['artist_name'], item['album_id'], item['album_name'],
                               item['album_comments_id'], item['album_publishTS'], item['album_company'], item['album_size']]
                cursor.execute(r'insert into t_albums values (%s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update '
                               r'f_artist_id=%s, f_artist_name=%s, f_album_name=%s, f_album_comment_id=%s, f_album_ts=%s,'
                               r'f_album_company=%s, f_album_size=%s', row+[item['artist_id'], item['artist_name'], item['album_name'],
                               item['album_comments_id'], item['album_publishTS'], item['album_company'], item['album_size']])
        except Exception as e:
            print("item: ", item)
            print('exception: ', e)

        conn.commit()

        cursor.close()
        conn.close()

    def open_spider(self, spider):
        logging.info("open spider in pipline")

    def close_spider(self, spider):
        logging.info("close spider in pipline")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
