# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 10:21:43 2019

@author: oo
"""
import re
import jieba
import collections
import wordcloud
import imageio
from os.path import join
from matplotlib import pyplot as plt

root_path = r"C:\Users\oo\Desktop\my\code\scrapy-pj\douban_comment\qinyunian"
user_dict_path = join(root_path, "user_dict.txt")
file_path = join(root_path, "qinyunian.txt")
img_path = join(root_path, "bg.jpg")
clond_path = join(root_path, "cloud.jpg")
font_path = join(root_path, "simhei.ttf")
file = open(file_path, 'r')
text = file.read()
file.close()

jieba.load_userdict(user_dict_path)
words = jieba.cut(text)

words = [w for w in words if len(w)>1 and not re.match('^[a-z|A-Z|0-9|.]*$',w)]
remove_words = [u'的', u'什么',u'和', u'是', u'…', u'也', u'对',u'等',u'能',u'都',u'没有',u' ',u'、',u'中',u'在',u'了',
                u'！',u'就',u'我',u'？','真的','这么','这部','一个','还是']
object_list = [word for word in words if word not in remove_words]
print(object_list)   
word_counts = collections.Counter(object_list)
word_counts_top10 = word_counts.most_common(10)
print(word_counts_top10)

mask = imageio.imread(img_path)
word_cloud = wordcloud.WordCloud(
        background_color = 'white',
        font_path = font_path,
        mask = mask
        )

wc = word_cloud.generate(str(object_list))
wc.to_file(clond_path)

plt.imshow(wc, interpolation = 'bilinear')
plt.axis('off')
plt.show()


