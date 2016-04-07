
from django.db import models
from mongoengine import *
import datetime
import time

connect('proginn_news',host='127.0.0.1',port=27017)
# Create your models here.

class wb_data(Document):
    title = StringField()
    link = StringField()
    tags = ListField(StringField(max_length=30))
    content = StringField()
    date_time = DateTimeField()
    date_modified = StringField()
    cat = StringField()
    ipt_time = StringField()


    meta = {'collection':'sslk3'}

class wb_data_zhihu(Document):
    question_title = StringField()
    question_link = StringField()
    answer = StringField()
    answer_link = StringField()
    vote = StringField()
    comment = StringField()
    date_time = DateTimeField()
    tags = ListField(StringField(max_length=30))

    meta = {'collection':'zhihu_cxykz3'}


# for data in wb_data_zhihu.objects:
#     print (data.date_time)
#     i = i+1

zhihu1 = wb_data_zhihu.objects.order_by('-date_time') #按照时间倒序来存储



sslk = wb_data.objects.order_by('-date_time')


waibao = sslk(date_modified ='2016/03/14')

# for item in waibao:
#     print (item.date_modified,item.cat)

# for data in wb_data_zhihu.objects:
#     print (data.tags)


ipt_time = time.strftime("%Y-%m-%d", time.localtime())
print (ipt_time)

# for data in wb_data.objects[:10]:
#     print (data.title,data.link,data.tags,data.content,data.date_time)

