# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 15:41:39 2019

@author: oo
"""

import requests
import re
from lxml import etree
from fake_useragent import UserAgent
import time


base_url = 'https://movie.douban.com/subject/25853071/comments?start={}&limit=20&sort=new_score&status=P'
ua = UserAgent().random
cookies = ''
header = {"User-Agent": ua,
          "Cookie": cookies,
          "Host": "movie.douban.com"}
file_path = r"C:\Users\oo\Desktop\my\code\scrapy-pj\douban_comment\qinyunian\qinyunian.txt"

def get_comment(url):
    try:
        req = requests.get(url, headers=header)
        req.encoding = 'utf_8'
        html = req.text
        pattern = re.compile(r'<span class="short">(.*?)</span>',re.S)
        comments = re.findall(pattern, html)
        print(comments)
        with open(file_path, 'a') as f:
            for comment in comments:
                f.write(comment+'\n')

    except Exception as e:
        print(e)

def main():
    for i in range(0, 1000, 20):
        url = base_url.format(i)
        get_comment(url)
        time.sleep(3)
        
    
if __name__ == "__main__":
    main()
    