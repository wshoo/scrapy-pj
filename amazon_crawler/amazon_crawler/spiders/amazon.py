# -*- coding: utf-8 -*-
import scrapy
from amazon_crawler.items import AmazonCrawlerItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=jacket&i=fashion-mens&page=1&qid=1550281384']
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"}

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],
                             headers=self.header,
                             callback=self.parse_page)

    def parse_page(self, response):
        items = response.xpath("//div[@class='s-result-list sg-row']")
        urls = items.xpath("//a[@class='a-link-normal a-text-normal']/@href").extract()
        for url in urls:
            if url:
                if '/s?k=' in url:
                    pass
                else:
                    url = 'https://www.amazon.com{}'.format(url)
                    yield scrapy.Request(url, headers=self.header, callback=self.parse_item)

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            print(next_page)
            next_url = 'https://www.amazon.com{}'.format(next_page)
            scrapy.Request(url=next_url,headers=self.header,callback=self.parse_page)


    def parse_item(self, response):
        item = AmazonCrawlerItem()
        item['name'] = response.xpath("normalize-space(//span[@id='productTitle']/text())").extract()
        item['price'] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract()
        item['desc'] = response.xpath("normalize-space(//ul[@class='a-unordered-list a-vertical a-spacing-none']//text())").extract()
        item['image_urls'] = response.xpath("//div[@id='imgTagWrapperId']/img/@data-old-hires").extract()
        yield item

