import pymongo
from bs4 import BeautifulSoup
import requests
import time
from mongoengine import *

client = pymongo.MongoClient('localhost',27017)
proginn_news = client['proginn_news']
sslk3 = proginn_news['sslk3']
sslklinks2 = proginn_news['sslklinks2']
linkexists3 = proginn_news['linkexists3']
zhihu_cxykz3 = proginn_news['zhihu_cxykz3']
linkexists_ZH1 = proginn_news['linkexists_ZH1']
weibo = proginn_news['weibo']
linkexists_weibo = proginn_news['linkexists_weibo']

def get_sslk(cat):
    url_0 = 'http://36kr.com/search?q={}'.format(cat)
    time.sleep(1)
    wb_data=requests.get(url_0,'utf-8')
    soup=BeautifulSoup(wb_data.text,'lxml')
    # print (soup)

    titles = soup.select('a.title')
    timeagos = soup.select('abbr.timeago')
    contents = soup.select('div.content')
    print (len(titles))


    for title,timeago,content in zip(titles,timeagos,contents):

        link = title.get('href')
        if linkexists3.find({'link':link}).count():  # 如果连接存在,则之后的所有连接都不用再爬.
            print ('exists')
        else:
            title = title.get_text()
            timeago = timeago.get_text()
            date_time = timeago
            date_modified = date_time.split(' ')[0]
            tags = ['36kr',cat,timeago]
            content = content.get_text()
            sslk3.insert_one({'cat':cat,'date_modified':date_modified,'link':link,'title':title,'tags':tags,'date_time':timeago,'content':content})
            linkexists3.insert_one({'link':link})
        # print (title,link,tags)
        # print (content.get_text())
        # print ('='*20)



# 2016-3-27 给数据库增加 date_modified 字段,用 update 功能

# for i in sslk3.find():
#     date_modified = i['date_time'].split(' ')[0]
#     print (date_modified)
#     sslk3.update({'_id':i['_id']},{'$set':{'date_modified':date_modified}})


for i in sslk3.find():
    cat = i['tags'][1]
    print (cat)
    sslk3.update({'_id':i['_id']},{'$set':{'cat':cat}})




# 运行
get_sslk('外包')
get_sslk('兼职')
get_sslk('私活')
get_sslk('程序员')
get_sslk('远程')
get_sslk('共享经济')

print(sslk3.find().count())


def get_ZH(url_ZH):
    wb_data = requests.get(url_ZH)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('a.js-title-link')
    answers = soup.select('div.summary.hidden-expanded')
    answerlinks = soup.select('a.toggle-expand.inline')
    votes = soup.select('a.action-item.votenum-mobile.zm-item-vote-count.js-mobi-vote')
    comments = soup.select('a.action-item.js-toggle-commentbox > span.label')
    date_times = soup.select('a.time.text-muted')

    for title,answer,vote,comment,answerlink,date_time in zip(titles,answers,votes,comments,answerlinks,date_times):
        answer_link = 'https://zhihu.com'+answerlink.get('href')
        if linkexists_ZH1.find({'link':answer_link}).count():
            print ('exists')
        else:
            linkexists_ZH1.insert_one({'link':answer_link})

            question_title = title.get_text()
            question_link = 'https://zhihu.com'+title.get('href')
            answer_content = answer.get_text()
            vote = vote.get_text()
            comment = comment.get_text()
            zhihu_cxykz3.insert_one({'question_title':question_title,
                                    'question_link':question_link,
                                    'answer':answer_content,
                                    'answer_link':answer_link,
                                    'vote':vote,
                                    'comment':comment,
                                     'date_time':date_time.get_text()
                                    })

# 程序员客栈  'https://www.zhihu.com/search?type=content&q=%E7%A8%8B%E5%BA%8F%E5%91%98%E5%AE%A2%E6%A0%88'
# 外包  'https://www.zhihu.com/search?type=content&q=%E5%A4%96%E5%8C%85'
# 私活  'https://www.zhihu.com/search?type=content&q=%E7%A7%81%E6%B4%BB'
# url_ZH = 'https://www.zhihu.com/search?type=content&q=%E7%A8%8B%E5%BA%8F%E5%91%98%E5%AE%A2%E6%A0%88'
# https://www.zhihu.com/search?type=content&q=%E8%BF%9C%E7%A8%8B%E5%B7%A5%E4%BD%9C

get_ZH('https://www.zhihu.com/search?type=content&q=%E5%A4%96%E5%8C%85') #外包
get_ZH('https://www.zhihu.com/search?type=content&q=%E7%A7%81%E6%B4%BB') #私活
get_ZH('https://www.zhihu.com/search?type=content&q=%E7%A8%8B%E5%BA%8F%E5%91%98%E5%AE%A2%E6%A0%88') #程序员客栈
get_ZH('https://www.zhihu.com/search?type=content&q=%E8%BF%9C%E7%A8%8B%E5%B7%A5%E4%BD%9C') #远程工作
get_ZH('https://www.zhihu.com/search?type=content&q=%E5%85%B1%E4%BA%AB%E7%BB%8F%E6%B5%8E') #共享经济


# print(zhihu_cxykz3.find().count())
# print (str(time.ctime()))


# 微博爬虫

#def get_weibo(ID):
    #url_0 = 'http://36kr.com/search?q={}'.format(ID)
url = 'http://s.weibo.com/weibo/%25E7%25A8%258B%25E5%25BA%258F%25E5%2591%2598%25E5%25AE%25A2%25E6%25A0%2588?topnav=1&wvr=6&b=1'
#time.sleep(1)




    #
    # for title,timeago,content in zip(titles,timeagos,contents):
    #
    #     link = title.get('href')
    #     if linkexists3.find({'link':link}).count():  # 如果连接存在,则之后的所有连接都不用再爬.
    #         print ('exists')
    #     else:
    #         title = title.get_text()
    #         timeago = timeago.get_text()
    #         date_time = timeago
    #         tags = ['36kr',cat,timeago]
    #         content = content.get_text()
    #         sslk3.insert_one({'link':link,'title':title,'tags':tags,'date_time':timeago,'content':content})
    #         linkexists3.insert_one({'link':link})




#Sat Mar 19 22:59:48 2016

# print (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) )
#2016-03-19 22:59:48
#mongoengine 的Datetime 格式:YYYY,MM,DD,HH,MM,SS,NNNNNN    %Y-%m-%d %H:%M:%S

# https://www.zhihu.com/topic/19609455/top-answers?page=2
#获取某个具体页面的 问题,问题链接;精华回答,回答链接




