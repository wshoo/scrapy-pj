# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class MySQLPipeline:
    
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'wang1108')
        self.conn = pymysql.connect(host=host, port=port, db=db,
                                   user=user, passwd=passwd, charset='utf8')
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        self.insert_db(item)

        return item


    def insert_db(self, item):
        values = (
            item["p_date"],
            item["p_province"],
            item["p_region"],
            item["p_meat_type"],
            item["p_price"],
        )
        try:
            sql = 'INSERT INTO pigprice VALUES (%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, values)
        except Exception:
            pass
        
    def close_spider(self, spider):
        
        self.conn.commit()
        self.conn.close()