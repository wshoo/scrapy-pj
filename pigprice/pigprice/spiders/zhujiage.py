# -*- coding: utf-8 -*-
import scrapy
from pigprice.items import PigpriceItem
import re


class ZhujiageSpider(scrapy.Spider):
    name = 'zhujiage'
    allowed_domains = ['zhujiage.com.cn']
    start_urls = ['http://www.zhujiage.com.cn/article/showlist.php?tid=26&TotalResult=33680&PageNo=1']
    
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"}
    print("start cralwing..")
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],
                             headers=self.header,
                             callback=self.parse_url)  
  
    def parse_url(self, response):
             
        items = response.xpath("//*[@id='contentbox']/div[10]/ul")[0]
        urls = items.xpath("//ul/li/div/a[2]/@href").extract()
        for url in urls:
            print(url)
            yield scrapy.Request(url=url,
                                headers=self.header,
                                callback=self.parse_page)
            
        next_page = response.xpath("//*[@class='showpage']/a[last()-2]/text()").extract_first()
        print("正在抓取下一页")
        if next_page == '下一页':
            next_url = response.xpath("//*[@class='showpage']/a[last()-2]/@href").extract_first()
            print('http://www.zhujiage.com.cn' + next_url)
            yield scrapy.Request(url='http://www.zhujiage.com.cn' + next_url,
                           headers=self.header,
                           callback=self.parse_url)


    def parse_page(self, response):
        
        try:
            p_date = response.xpath("//*[@id='left']/div[4]/text()[1]").extract()[0]
            pattern =re.compile(r"\d{4}-\d{2}-\d{2}")
            f_date = pattern.findall(p_date)[0]
            text = response.xpath("//*[@id='content']/p[position()>1]/text()").extract()
            item = PigpriceItem()
            for datas in text:
                data = datas.split(' ')
                item["p_date"] = f_date
                item["p_province"] = "".join(data[0].split())
                item["p_region"] = "".join(data[1].split())
                item["p_meat_type"] = "".join(data[4].split())
                item["p_price"] = data[5]
                yield item
        except Exception as e:
            pass