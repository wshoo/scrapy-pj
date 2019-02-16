import MySQLdb



class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '')
        self.db_conn = MySQLdb.connect(host=host, port=port, db=db,
                                   user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()


    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()


    def process_item(self, item, spider):
        self.insert_db(item)

        return item


    def insert_db(self, item):
        values = (
            item['name'],
            item['price'],
            item['desc'],
            item['image_urls'],
        )

        sql = 'INSERT INTO jacket VALUES (%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)