from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Goods,Types

from django.contrib.auth.decorators import permission_required


# 商品添加页面
@permission_required('myadmin.insert_goods',raise_exception = True)
def goodsadd(request):
    from . typeviews import GetTypesAll
    
    context = {'tlist':GetTypesAll()}    
    return render(request,'admin/goods/add.html',context)

# 商品执行添加
@permission_required('myadmin.insert_goods',raise_exception = True)
def goodsinsert(request):
    # 导入图片上传函数
    from . views import uploads

    # 判断是否上传了商品图片
    if not request.FILES.get('pic',None):
        return HttpResponse('<script>alert("请选择上传的商品图片");location.href="/admin/goods/add/"</script>')
    try:
        # 接收数据,执行添加
        ob = Goods()
        ob.typeid = Types.objects.get(id=request.POST['typeid'])
        ob.title = request.POST['title']
        ob.price = request.POST['price']
        ob.storage = request.POST['storage']
        ob.info = request.POST['info']
        ob.pic = uploads(request)
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="/admin/goods/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/goods/add/"</script>')

# 商品列表
@permission_required('myadmin.show_goods',raise_exception = True)
def goodslist(request):

    types = int(request.GET.get('types',0))
    goodstype = request.GET.get('goodstype',None)
    keywords = request.GET.get('keywords',None)

     # 状态搜索的定义 1：新品、2：热销、3：下架
    statuslist = {'新品':1,'热销':2,'下架':3}

    # 判断是否有搜索条件
    if goodstype:
        # 判断商品的搜索条件
        if goodstype == 'all':
            from django.db.models import Q
            data = Goods.objects.filter(Q(title__contains=keywords)|Q(price__contains=keywords)|Q(status__contains=statuslist.get(keywords,'aa')))
        elif goodstype == 'title':
            data = Goods.objects.filter(title__contains=keywords)
        
        elif goodstype == 'price':
            data = Goods.objects.filter(price__contains=keywords)
        
        elif goodstype == 'status':
            data = Goods.objects.filter(status__contains=statuslist.get(keywords,'aaa'))

        # 判断是否存在分类条件
        if types:
            data = data.filter(typeid_id=types)

    else:
         # 获取所有的商品信息
        data = Goods.objects.all()
    

    from . typeviews import GetTypesAll
    context = {'glist':data,'tlist':GetTypesAll()}

    return render(request,'admin/goods/list.html',context)

