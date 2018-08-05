from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from myadmin.models import Users,Types,Goods,Address,Order,OrderInfo
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

from django.views.decorators.cache import cache_page
import datetime



# 缓存测试
@cache_page(10)
def cache1(request):
    
    t =  datetime.datetime.now()

    return HttpResponse(t)



from django.core.cache import cache

def cachediy(request):

    # 先从缓存中获取数据
    data = cache.get('my_key')
    t = cache.get('my_time')

    # 判断缓存中如果没有数据
    if not data:

        data = Users.objects.all()
        t =  datetime.datetime.now()

        print('没有缓存数据')

        cache.set('my_key',data)
        cache.set('my_time',t)


    print(data)
    print(t)




    return HttpResponse(datetime.datetime.now())

# 获取导航分类
def gettype():
    
    # 获取所有的二级分类 
    data = Types.objects.exclude(pid=0)
    return data

# 首页
def index(request):
    # data = [
    #     {
    #         'name':'服装',
    #         'sub':[
    #             {'name':'男装','sub':[{'title':''},{},{}]},
    #             {'name':'女装','sub':[{'title':''},{},{}]}
    #         ]
    #     }
    #     {
    #         'name':'数码',
    #         'sub':[{'name':'电视','sub':[{},{}]},{'name':'相机','sub':[{},{}]}]
    #     }
    # ]

    # 获取所有的顶级分类
    data = Types.objects.filter(pid=0)

    for x in data:
        x.sub = Types.objects.filter(pid=x.id)
        for v in x.sub:
            v.sub = Goods.objects.filter(typeid=v.id)[:6]


    # print(data[0].sub[0].sub)




    context = {'typelist':gettype(),'navlist':data}
    return render(request,'home/index.html',context)    


# 列表页
def list(request,tid):

    # 根据id获取当前分类的信息
    tod = Types.objects.get(id=tid)
    if tod.pid == 0:
        # 顶级分类
        data = tod
        # 获取子类 [{},{}]
        data.sub = Types.objects.filter(pid=tod.id)
        ids = []
        for x in data.sub:
            ids.append(x.id)
        
        data.goods = Goods.objects.filter(typeid__in=ids)

        # {'name':'服装','sub':[{'name':'男装'},{'name':'女装'}],'goods':[{},{},{},{}]}

    else:
        # {'name':'服装','sub':[{'name':'男装'},{'name':'女装'}],'goods':[{},{}],'obj':{'name':'男装'}}
        
        # 先获取父级对象
        data = Types.objects.get(id=tod.pid)
        # 获取当前子类的商品信息
        data.goods = Goods.objects.filter(typeid=tod.id)
        # 获取所有的同级信息,包括当前类
        data.sub = Types.objects.filter(pid=tod.pid)
        # 给data数据追加了一个obj对象
        data.obj = tod



    context = {'typelist':gettype(),'data':data}
    return render(request,'home/list.html',context)    

# 详情页
def info(request,gid):
    
    # 根据id获取商品的信息
    ginfo = Goods.objects.get(id=gid)

    context = {'typelist':gettype(),'ginfo':ginfo}
    return render(request,'home/info.html',context)    


# 加入购物车
def cartadd(request):
    try:
        # 接收商品id
        gid = request.GET['gid']
        # 加入购物车的数量
        num = int(request.GET['num'])

        # 获取购物车数据
        data = request.session.get('cart',{})
        
        # 判断商品是否已经存在与购物车中
        # {1:{},2:{}}
        if gid in data:
            # 如果已经存在,找到商品,修改数量
            data[gid]['num'] += num
        else:
            # 获取商品信息
            goods = Goods.objects.get(id=gid)
            # 把新的商品信息,追加到data数据中
            data[gid] = {'id':goods.id,'title':goods.title,'price':str(goods.price),'pic':goods.pic,'num':num}


        # 加入到session {1:{},2:{}}
        request.session['cart'] = data


        return JsonResponse({'code':0,'msg':'加入购物车成功'})
    except:
        return JsonResponse({'code':1,'msg':'加入购物车失败'})


# 购物车列表
def cartlist(request):


    context = {'typelist':gettype()}
    return render(request,'home/cartlist.html',context)


# 清空购物车
def cartclear(request):

    request.session['cart'] = {}

    return HttpResponse('<script>location.href="/cart/list/"</script>')


# 修改购物车商品数量
def cartedit(request):
    gid = request.GET.get('gid')
    num = int(request.GET.get('num'))


    # 读取购物车
    data = request.session['cart']

    # 修改数量
    data[gid]['num'] = num

    # 把数据加载到session中
    request.session['cart'] = data


 
    return HttpResponse('<script>location.href="/cart/list/"</script>')


# 购物车商品删除
def cartdel(request):
    gid = request.GET['gid']
    # 读取购物车数据
    data = request.session['cart']
    # 执行删除
    del data[gid]
    # 将购物车数据,放入session中
    request.session['cart']=data

    return HttpResponse('aa')



# 确认订单
def orderconfirm(request):

    

    if request.method == 'GET':

        # 获取用户选择的商品
        ids = request.GET['ids'].split(',')
        
        # 从session中读取购物车信息
        cartdata = request.session['cart']
        orderdata = {}

        for x in cartdata:
            if x in ids:
                orderdata[x] = cartdata[x]

        # 把用户选择购买的商品存入session
        request.session['order'] = orderdata

        # 需要让用户确认收货地址 获取当前用户的所有地址信息
        address = Address.objects.filter(uid=request.session['VipUser']['uid'])

        context = {'typelist':gettype(),'address':address}
        return render(request,'home/orderconfirm.html',context)

    elif request.method == 'POST':

        # 执行地址的添加
        ob = Address()
        ob.uid = Users.objects.get(id=request.session['VipUser']['uid'])
        ob.aname = request.POST['aname']
        ob.aphone = request.POST['aphone']
        ob.aads = request.POST['aads']

        # 状态修改
        s = request.POST.get('status',0)
        # 判断当前如果设置为默认值,
        if s == '1':
            # 把其它的地址修改状态 0 
            obs = Address.objects.filter(status=1)
            for x in obs:
                x.status = 0
                x.save()

        ob.status = s
        ob.save()
        return HttpResponse('<script>alert("地址添加成功");location.href="/order/confirm/?ids='+request.GET['ids']+'"</script>')


# 生成订单
def ordercreate(request):

    # 在session获取订单数据
    data = request.session['order']
    totalprice = 0
    totalnum = 0

    for x in data:
        n = float(data[x]['price']) * data[x]['num']
        totalprice += n
        totalnum += data[x]['num']


    # 创建订单
    order = Order()
    order.uid = Users.objects.get(id=request.session['VipUser']['uid'])
    order.address = Address.objects.get(id=request.POST['addressid'])
    order.totalprice = totalprice
    order.totalnum = totalnum
    order.status = 1
    order.save()
    
    # 读取购物车数据
    cart = request.session['cart']

    # 创建订单详情
    for x in data:
        orderinfo  = OrderInfo()
        # 订单号
        orderinfo.orderid = order
        # 获取当前购买的商品对象
        goods = Goods.objects.get(id=x)

        orderinfo.gid = goods
        orderinfo.num = data[x]['num']
        orderinfo.price = data[x]['price']
        orderinfo.save()
        # 清楚购物车的商品数据
        del cart[x]

        # 修改商品的购买数量
        goods.num +=  data[x]['num']
        goods.storage -= data[x]['num']
        goods.save()

        
    # 清空session中的订单数据
    request.session['order'] = {}
    # 更新购物车
    request.session['cart']= cart

    # 跳转到付款页面
    return HttpResponse('<script>alert("订单创建成功,请立即支付");location.href="/order/buy/?orderid='+str(order.id)+'"</script>')



# 付款页面
def orderbuy(request):
    orderid = request.GET.get('orderid',None)
    if orderid:
        # 通过订单id获取订单信息,并展示
        order = Order.objects.get(id=orderid)
        context = {'order':order}
        return render(request,'home/buy.html',context)


# 我的订单
def myorder(request):

    # 获取当前登录用户的所有订单信息
    orders = Order.objects.filter(uid=request.session['VipUser']['uid'])

    context = {'orders':orders}
    return render(request,'home/myorder.html',context)


# 注册
def register(request):
    # 判断当前请求方式
    if request.method == 'GET':
        return render(request,'home/register.html')
    elif request.method == 'POST':
        # 执行注册
        # 判断用户名是否存在
        res = Users.objects.filter(username=request.POST['username']).exists()
        if res :
            return HttpResponse('<script>alert("用户名已存在");location.href="/register"</script>')
        else:

            ob = Users()
            ob.username = request.POST['username']
            ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
            ob.save()
            # 把用户信息存储到session
            request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}

            return HttpResponse('<script>alert("注册成功,欢迎登录");location.href="/"</script>')


# 登录
def login(request):
    if request.method == 'GET':
        return render(request,'home/login.html')
    elif request.method == 'POST':
        # 查询用户名
        # 判断验证码是否正确
        if request.POST['code'].lower() != request.session['verifycode'].lower():
            return HttpResponse('<script>alert("验证码错误");location.href="/login/"</script>')
        # 判断用户,和密码
        ob = Users.objects.filter(username=request.POST['username'])
        if ob:
            ob = ob[0]
            # 判断密码
            if check_password(request.POST['password'],ob.password):
                # 密码正确
                # 进行登录
                request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}

                return HttpResponse('<script>alert("登录成功");location.href="/"</script>')



        return HttpResponse('<script>alert("用户名或密码错误");location.href="/login/"</script>')


# 退出登录
def loginout(request):
    
    del request.session['VipUser']

    return HttpResponse('<script>location.href="/"</script>')
