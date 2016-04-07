
from django.shortcuts import render
from zhihu_parse.models import wb_data,zhihu1,sslk
from django.core.paginator import Paginator
import time
# Create your views here.

#不同区域发帖量前三名


# def new_data(date1,date2):
#     pipeline1 = [
#         {'$match' :{'date_modified':{'$gte':date1,'$lte':date2}}},
#         {'$group':{'_id':'$cat','counts':{'$sum':1}}}
#         ]
#
#     for item in wb_data._get_collection().aggregate(pipeline1):
#         data = {
#                 'name': item['_id'],
#                 'data': [item['counts']],
#                 'type': 'column'
#             }
#         yield data
#
# s1 = [i for i in new_data('2016/03/1','2016/03/25')]
# s2 = [i for i in new_data('2016/02/1','2016/02/29')]

def get_series(cats,months):
    for cat in cats:
        data = []
        for month in months:
            pipeline2 = [
                 {'$match':{'$and':[{'date_modified':{'$gte':month[0],'$lte':month[1]}},{'cat':cat}]}},
                 {'$group':{'_id':'$cat','counts':{'$sum':1}}}
            ]
            a = 0

            if wb_data._get_collection().aggregate(pipeline2):

                for item in wb_data._get_collection().aggregate(pipeline2):
                        a = item['counts']
            data.append(a)
        info = {
            'name':cat,
            'data':data,
            'type':'line'
        }
        yield info

cats = ['外包','共享经济','远程','程序员','兼职']
months = [['2015/11/1','2015/11/30'],['2015/12/1','2015/12/30'],['2016/01/1','2016/01/30'],['2016/02/1','2016/02/29'],['2016/03/1','2016/03/25']]
s4 = [i for i in get_series(cats,months)]


print (s4)

s3 = [{'type': 'column', 'name': '共享经济', 'data': [1,4]}, {'type': 'column', 'name': '远程', 'data': [4,12]}, {'type': 'column', 'name': '程序员', 'data': [3,2]}, {'type': 'column','name':'兼职','data':[5,4]},{'type': 'column', 'name': '外包', 'data': [7,12]}]

series_CY=s4


# def topx(date1,date2,area,limit):
#
#     options = {
#         'chart':{'zoomType':'xy'},
#         'title':{'text':'每日关键词热度'},
#         'subtitle':{'text':'数据图表'},
#         'yAxis':{'title':'数量'}
#
#     }
#
#     pipeline1 = [
#         {'$match':{'$and':[{'pub_date':{'$gte':date1,'$lte':date2}},{'area':{'$all':area}}]}},
#         {'$group':{'_id':'$cates','counts':{'$sum':1}}},
#         {'$limit':limit},
#         {'$sort':{'counts':-1}}
#
#     ]
#
#     for item in wb_data._get_collection().aggregate(pipeline1):
#         data = {
#                 'name': item['_id'],
#                 'data': [item['counts']],
#                 'type': 'column'
#             }
#         yield data
#
# series_CY = [i for i in topx('2015.12.25','2016.1.30',['朝阳'],5)]
# series_hd = [i for i in topx('2015.12.25','2016.1.30',['海淀'],5)]
# series_tz = [i for i in topx('2015.12.25','2016.1.30',['通州'],5)]
#
# print(series_CY)
# print (series_CY)
#----------------------------------

def index(request):
    limit = 10
    webinfo_all=sslk
    paginator_all = Paginator(webinfo_all,limit)
    page_all = request.GET.get('page',1)
    loaded_all = paginator_all.page(page_all)

    webinfo_wb=sslk(cat = '外包')
    paginator_wb = Paginator(webinfo_wb,limit)
    page_wb = request.GET.get('page',1)
    loaded_wb = paginator_wb.page(page_wb)

    context={
        'wb_data_all':loaded_all,
        'counts_all':webinfo_all.count(),
        'last_time_all':webinfo_all.order_by('-date_time').limit(1),
        'wb_data_wb':loaded_wb,
        'counts_wb':webinfo_wb.count(),
        'last_time_wb':webinfo_wb.order_by('-date_time').limit(1),
    }

    return render(request, "new_data.html",context)

def sslkwb(request):
    limit = 10
    webinfo_wb=sslk(cat = '外包')
    paginator_wb = Paginator(webinfo_wb,limit)
    page_wb = request.GET.get('page',1)
    loaded_wb = paginator_wb.page(page_wb)

    context={
        'wb_data_wb':loaded_wb,
        'counts_wb':webinfo_wb.count(),
        'last_time_wb':webinfo_wb.order_by('-date_time').limit(1),
    }

    return render(request, "sslk_waibao.html",context)

def sslkcxy(request):
    limit = 10
    webinfo_cxy=sslk(cat = '程序员')
    paginator_cxy = Paginator(webinfo_cxy,limit)
    page_cxy = request.GET.get('page',1)
    loaded_cxy = paginator_cxy.page(page_cxy)

    context={
        'wb_data_cxy':loaded_cxy,
        'counts_cxy':webinfo_cxy.count(),
        'last_time_cxy':webinfo_cxy.order_by('-date_time').limit(1),
    }

    return render(request, "sslk_cxy.html",context)

def sslknew(request):
    limit = 10
    webinfo_new=sslk(ipt_time = time.strftime("%Y-%m-%d", time.localtime()))
    paginator_new = Paginator(webinfo_new,limit)
    page_new = request.GET.get('page',1)
    loaded_new = paginator_new.page(page_new)

    context={
        'wb_data_new':loaded_new,
        'counts_new':webinfo_new.count(),
        'last_time_cxy':webinfo_new.order_by('-date_time').limit(1),
    }

    return render(request, "sslk_new.html",context)
# waibao = sslk(cat = '外包')
#
# for item in waibao[:10]:
#     print (item.cat)

def zhihu(request):
    limit = 10
    webinfo=zhihu1
    paginator = Paginator(webinfo,limit)
    page = request.GET.get('page',1)
    loaded = paginator.page(page)

    context={
        'wb_data_zhihu':loaded,
        'counts':webinfo.count(),
        'last_time':webinfo.order_by('-date_time').limit(1),
    }

    return render(request, "zhihu.html",context)



def chart(request):
    context = {
        'chart_CY':series_CY,
        # 'chart_TZ':series_tz,
        # 'chart_hd':series_hd
    }
    return render(request,'chart.html',context)


