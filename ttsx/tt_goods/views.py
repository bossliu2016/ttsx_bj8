# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator
from models import TypeInfo, GoodsInfo


# Create your views here.
def index(request):
    '''
    book.heroinfo_set.all()
    模板中需要的数据包括：分类信息，当前分类的最新的4个商品，当前分类的人气最高的3个商品
    共6个分类，所以会有6组以上的信息
    list=[{type:,list_new:,list_click:},{type:,list_new:,list_click:},....]
    '''
    type_list = TypeInfo.objects.all()
    list = []
    for typeinfo in type_list:
        list.append({
            'type': typeinfo,
            'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
            'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
        })
    context = {'title': '首页', 'cart': '1', 'list': list}
    return render(request, 'tt_goods/index.html', context)


def list_goods(request, type_id, page_index, order_by):
    typeinfo = TypeInfo.objects.get(pk=type_id)

    order_bystr = '-id'
    if order_by == '2':
        order_bystr = 'gprice'
    elif order_by == '3':
        order_bystr = '-gclick'

    list = typeinfo.goodsinfo_set.order_by(order_bystr)
    list_new = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    paginator = Paginator(list, 10)

    page_index = int(page_index)
    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(int(page_index))

    '''
    共n页
    第1页：1 2 3 4 5
    第2页：1 2 3 4 5
    第3页：1 2 3 4 5
        range[pindex-2,pindex+3]
    第4页：2 3 4 5 6
    ...
    第p页(p=n-2)：满足公式
    第p页(p=n-1)：n-4 n-3 n-2 n-1 n
    第p页(p=n)：n-4 n-3 n-2 n-1 n
    '''

    plist = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= paginator.num_pages - 1:
            plist = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            plist = range(page_index - 2, page_index + 3)

    context = {
        'title': '列表页', 'cart': 1,
        'type': typeinfo, 'page': page, 'pindex_list': plist,
        'order_by': order_by, 'list_new': list_new
    }
    return render(request, 'tt_goods/list.html', context)


def detail(request, gid):
    try:
        goods = GoodsInfo.objects.get(pk=gid)
        # 维护人气信息
        goods.gclick += 1
        goods.save()
        # 最新商品
        list_new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

        context = {'title': '详细页', 'cart': '1', 'goods': goods, 'list_new': list_new}
        response= render(request, 'tt_goods/detail.html', context)
        #最近浏览，数据存储格式如id1,id2,id3,id4,id5
        goods_ids=request.COOKIES.get('goods_ids','')
        #判断是否存在gid，如果存在则删除，然后再加到第一个，否则，直接加到第一个
        if len(goods_ids)==0:
            goods_ids2=[gid]
        else:
            goods_ids2=goods_ids.split(',')
            if gid in goods_ids2:
                goods_ids2.remove(gid)
            else:
                if len(goods_ids2)==5:
                    goods_ids2.pop()
            goods_ids2.insert(0, gid)
        response.set_cookie('goods_ids',','.join(goods_ids2))

        return response
    except:
        return render(request, '404.html')


from haystack.generic_views import SearchView

class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['title']='搜索结果'
        context['cart']='1'
        context['isleft']='0'
        return context