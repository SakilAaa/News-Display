from django.shortcuts import render
from django.db.models import Q
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import random
import sqlite3
import jieba
import time as timetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from haystack.views import SearchView
from .models import Comment, News, Category
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from final.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
# Create your views here

def get_single(text):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    cursor.close()
    conn.close()
    return set(lst)

def frontpage(request):
    template = loader.get_template('news/lookfor.html')
    cater = Category.objects.all()
    context = {
        'category_list': cater
    }
    return HttpResponse(template.render(context, request))

def lookfor_page(request, page_id):
    start = timetime.time()
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    template = loader.get_template('news/lookfor_page.html')
    data = request.GET
    content = data.get('content')
    sort = data.get('sort')
    category = data.getlist('category')
    if category == []:
        category = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    category = [Category.objects.get(id=int(i)) for i in category]
    x = []
    for i in category:
        temp = i.news_list.lstrip('[').rstrip(']').split(',')
        temp = [int(j) for j in temp]
        x = x + temp
    source = [i.name for i in category]
    lianjie =''
    for g in category:
        lianjie = lianjie + str('category=' + str(g.id) + '&')
    if content is not None:
        news_list = News.objects.filter(Q(title__icontains=content)|Q(body__icontains=content))#0.1秒
    else:
        news_list = News.objects.all()
    news_list = news_list.filter(Q(id__in=x))
    if sort == 'time':
        sortmethod = '按时间排序'
        news_list = news_list.order_by("-time")
    else:
        sortmethod = '按热度排序'
        news_list = news_list.order_by("-popularity")
    paginator = Paginator(news_list, 20)
    currentPage = int(page_id)
    try:
        page = paginator.page(page_id)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if paginator.num_pages > 12:
        if currentPage <= 5:  # 当前页小于5
            page_range = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:  # 当前页+5大于总页码
            page_range = range(currentPage - 5, paginator.num_pages + 1)
        else:
            page_range = range(currentPage - 5, currentPage + 5)
    else:
        page_range = paginator.page_range 
    
    end_time = Decimal(timetime.time() - start).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    context = {'page': page,
               'paginator': paginator,
               'currentPage': currentPage,
               'page_range': page_range,
               'content': content,
               'sort': sortmethod,
               'sort_type': sort,
               'category_list': category,
               'num': len(news_list),
               'time': end_time,
               'lianjie': lianjie
               }
    return HttpResponse(template.render(context, request))

def lookfor(request):
    template = loader.get_template('news/lookfor_page.html')
    desti = request.POST['destination']
    data = request.GET
    content = data.get('content')
    sort = data.get('sort')
    category = data.getlist('category')
    if category == []:
        category = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    category = [Category.objects.get(id=int(i)) for i in category]
    x = []
    for i in category:
        temp = i.news_list.lstrip('[').rstrip(']').split(',')
        temp = [int(j) for j in temp]
        x = x + temp
    source = [i.name for i in category]
    lianjie =''
    for g in category:
        lianjie = lianjie + str('category=' + str(g.id) + '&')
    return HttpResponseRedirect(f'/lookfor/{desti}?content={content}&sort={sort}&{{ lianjie }}')

class MySearchView(SearchView):
    def build_page(self):
        context = super(MySearchView, self).extra_context()
        try:
            page_no = int(self.request.GET.get('page', 1))
        except Exception:
            return HttpResponse("Not a valid number for page.")
        
        if page_no < 1:
            return HttpResponse("Pages should be 1 or greater.")
        a = []
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a, HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        page = paginator.page(page_no)
        return (paginator, page)
    
def category(request):
    category_list = Category.objects.all()
     #计算数量
    template = loader.get_template('news/category.html')
    context = {'category_list': category_list}
    return HttpResponse(template.render(context, request))

def category_detail(request, category_id, page_id):
    news_list = Category.objects.get(id=category_id).news_list.lstrip('[').rstrip(']').split(',')
    news_list = [int(i) for i in news_list]
    news_list = [News.objects.get(id=i) for i in news_list]
    paginator = Paginator(news_list, 20)
    currentPage= page_id
    try:
        page = paginator.page(page_id)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if paginator.num_pages > 12:
        if currentPage <= 5:  # 当前页小于5
            page_range = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:  # 当前页+5大于总页码
            page_range = range(currentPage - 5, paginator.num_pages + 1)
        else:
            page_range = range(currentPage - 5, currentPage + 5)
    else:
        page_range = paginator.page_range
    context = {'page': page,
               'paginator': paginator,
               'currentPage': currentPage,
               'page_range': page_range,
               'category': Category.objects.get(id=category_id)}
    template = loader.get_template('news/category_detail.html')
    return HttpResponse(template.render(context, request))

def category_detail_jump(request, id):
    desti = request.POST['destination']
    return HttpResponseRedirect(f'/category/detail/{id}/{desti}')

def news_all_jump(request):
    id = request.POST['destination']
    return HttpResponseRedirect(f'/news_all/{id}')

def news_all(request, page_id):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 20)
    currentPage = int(page_id)
    try:
        page = paginator.page(page_id)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    template = loader.get_template('news/news_all.html')
    if paginator.num_pages > 12:
        if currentPage <= 5:  # 当前页小于5
            page_range = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:  # 当前页+5大于总页码
            page_range = range(currentPage - 5, paginator.num_pages + 1)
        else:
            page_range = range(currentPage - 5, currentPage + 5)
    else:
        page_range = paginator.page_range
    context = {'page': page,
               'paginator': paginator,
               'currentPage': currentPage,
               'page_range': page_range}
    return HttpResponse(template.render(context, request))

def mainpage(request):
    num_list = random.sample(range(0, 5044), 20)
    news_list = [News.objects.get(id=i) for i in num_list]
    template = loader.get_template('news/mainpage.html')
    context = {
        'news_list': news_list,
        'categories': Category.objects.all()
    }
    return HttpResponse(template.render(context, request))

def jump(request):
    id = request.POST['destination']
    return HttpResponseRedirect(f'/news/{id}')

def show_news(request, id):
    news = News.objects.get(id=id)
    template = loader.get_template('news/index.html')
    comments = news.comment_set.all()
    comments = comments[::-1]
    pic_list = news.pic.lstrip('[\'').rstrip('\']').split('\', \'')
    body = news.body.split('\n')
    try:
        category = Category.objects.get(name=news.source)
    except:
        category = Category.objects.get(name='其它')
    context = {
        'news': news,
        'comments': comments,
        'pic_list': pic_list,
        'body': body,
        'category': category
    }
    return HttpResponse(template.render(context, request))

def comment(request, id):
    data = request.POST
    user = data['user']
    content = data['content']
    time = timetime.strftime('%Y-%m-%d %H:%M:%S')
    news = News.objects.get(id=id)
    news.comment_cnt += 1
    news.save()
    obj = Comment(news=news, user=user, content=content, time=time)
    obj.full_clean()
    obj.save()
    return HttpResponseRedirect(f'/news/{id}')

def delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    news_id = comment.news_id
    comment.delete()
    news = News.objects.get(id=news_id)
    news.comment_cnt -= 1
    news.save()
    return HttpResponseRedirect(f'/news/{news_id}')