from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Users
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.decorators import permission_required

# Create your views here.

# ajax文件上传
def ajaxupload(request):

    import time,random

    myfile = request.FILES.get('pic',None)
    # 判断是否有文件上传
    if not myfile:
        return JsonResponse({'code':1,'msg':'没有文件上传'})

    # 执行文件上传
    # 自定义文件名 时间戳+随机数+.jpg
    filename = str(time.time())+str(random.randrange(10000,99999))

    # 获取当前上传文件的后缀名
    hzm = myfile.name.split('.').pop()
    # 允许上传的文件类型
    arr = ['png','jpg','gif','jpeg','bmp','icon']
    # 如果上传的文件类型不正确
    if hzm not in arr:
        return JsonResponse({'code':2,'msg':'上传的文件类型错误'})

    # 打开文件
    file = open('./static/pics/'+filename+'.'+hzm,'wb+')
    # 分块写入文件  
    for chunk in myfile.chunks():      
           file.write(chunk)  
    # 关闭文件
    file.close()

    # 返回文件的url路径
    return JsonResponse({'code':0,'msg':'上传成功','url':'/static/pics/'+filename+'.'+hzm})
    


    return HttpResponse('ajaxupload')

# 后台首页
def index(request):

    return render(request,'admin/index.html')

# session的使用
def test(request):


    # 设置session
        # request.session['a'] = 'abc'
        # request.session['b'] = ['b1','b2','b3']
        # request.session['c'] = {'name':'ccc','age':20}
        # request.session['d'] = [{'name':'ccc1','age':20},{'name':'ccc2','age':20},{'name':'ccc3','age':20}]

    # 获取session
        # res1 = request.session['b']
        # res2 = request.session.get('c','123')

        # print(res1)
        # print(res2)

    # 修改
        # res = request.session['b']
        # res[2] = 'c3'
        # request.session['b'] = res
        # print(request.session['b'])

    # 删除单个key
        # del request.session['b']
   

    # 清除当前会话中的所有key
        # request.session.clear() 

        # print(request.session.get('a'))
        # print(request.session.get('b'))
        # print(request.session.get('c'))
        # print(request.session.get('d'))

    # 删除当前的会话数据
    # request.session.flush()


    # 应用场景   登录,注册   购物车  


    return HttpResponse('session的使用')


@permission_required('myadmin.insert_users',raise_exception = True)
# 显示用户添加页面
def useradd(request):

    return render(request,'admin/user/add.html')

# 执行添加
@permission_required('myadmin.insert_users',raise_exception = True)
def userinsert(request):
    # 执行文件上传
    pic = uploads(request)
    if not pic:
        return HttpResponse('<script>alert("上传的文件类型不正确,只能上传图片类型");location.href="/admin/user/add/"</script>')
    
    try:

        # 接收用户数据,执行添加
        ob = Users()
        ob.username = request.POST.get('username')
        # 进行密码加密
        ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.picurl = pic
        ob.save()
        
        return HttpResponse('<script>alert("添加成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/user/add/"</script>')

# 用户列表页

@permission_required('myadmin.show_users',raise_exception = True)
def userlist(request):

    # 搜索条件
    types = request.GET.get('type',None)
    # 搜索参数
    keywords = request.GET.get('keywords','')

    # 状态搜索的定义
    statuslist = {'正常':0,'禁用':1}

    # 判断是否有搜索条件
    if types:
        # 有搜索条件
        # 如果搜索类型为all 则为多字段单参数
        if types == 'all':
            from django.db.models import Q
            data = Users.objects.filter(Q(username__contains=keywords)|Q(email__contains=keywords)|Q(phone__contains=keywords)|Q(age__contains=keywords)|Q(sex__contains=keywords)|Q(status__contains=statuslist.get(keywords,'aa'))).exclude(status=3)
        
        elif types == 'username':
            data = Users.objects.filter(username__contains=keywords).exclude(status=3)
        
        elif types == 'email':
            data = Users.objects.filter(email__contains=keywords).exclude(status=3)
        
        elif types == 'phone':
            data = Users.objects.filter(phone__contains=keywords).exclude(status=3)
        
        elif types == 'age':
            data = Users.objects.filter(age__contains=keywords).exclude(status=3)
        
        elif types == 'sex':
            data = Users.objects.filter(sex__contains=keywords).exclude(status=3)
        
        elif types == 'status':
            data = Users.objects.filter(status__contains=statuslist.get(keywords,'aaa')).exclude(status=3)
    else:
        # 没有搜索条件,获取全部
        data = Users.objects.exclude(status=3)


    # 数据分页类
    from django.core.paginator import Paginator
    # 实例化分页类  参数1 查询的数据,参数2 每页要显示的数据
    paginator = Paginator(data,5)

    # 当前页码
    p = int(request.GET.get('p',1))

    # 根据当前页码获取当前页应该显示的数据
    userlist = paginator.page(p)

    # 获取当前页的页码数 (1,177)
    # num = paginator.page_range




    # 分配数据
    context = {'ulist':userlist}
    # 加载模板
    return render(request,'admin/user/list.html',context)

# 执行用户删除
@permission_required('myadmin.del_users',raise_exception = True)
def userdel(request):
    try:
        uid = request.GET.get('uid')
        # 逻辑删除
        ob = Users.objects.get(id=uid)
        # 修改状态
        ob.status = 3
        # 执行修改
        ob.save()
        
        return HttpResponse('0')
    except:
        return HttpResponse('1')

# 用户编辑
@permission_required('myadmin.edit_users',raise_exception = True)
def useredit(request,uid):
    # 查询用户信息
    ob = Users.objects.get(id=uid)

    context = {'uinfo':ob}

    return render(request,'admin/user/edit.html',context)

# 执行修改
@permission_required('myadmin.edit_users',raise_exception = True)
def userupdate(request):
    try:
        # 根据id获取用户对象
        ob = Users.objects.get(id=request.POST['id'])
        ob.username = request.POST.get('username')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')

        # 判断是否有文件上传
        if request.FILES.get('pic'):
            # 判断是否使用的默认图
            if ob.picurl != '/static/pics/default/default.jpg':
                import os
                #不是默认头像,则执行删除
                os.remove('.'+ob.picurl) 
            # 上传新的头像
            ob.picurl = uploads(request)

        # 执行更新
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/user/edit/'+str(ob.id)+'"</script>')

# 修改状态
def userstatus(request):

    # 执行状态修改
    ob = Users.objects.get(id=request.GET['uid'])
    ob.status = int(request.GET['status'])
    ob.save()

    return HttpResponse('')


def uploads(request):
    
    import time,random

    myfile = request.FILES.get('pic',None)
    # 判断是否有文件上传
    if not myfile:
        return '/static/pics/default/default.jpg'

    # 执行文件上传
    # 自定义文件名 时间戳+随机数+.jpg
    filename = str(time.time())+str(random.randrange(10000,99999))

    # 获取当前上传文件的后缀名
    hzm = myfile.name.split('.').pop()
    # 允许上传的文件类型
    arr = ['png','jpg','gif','jpeg','bmp','icon']

    if hzm not in arr:
        return False

    # 打开文件
    file = open('./static/pics/'+filename+'.'+hzm,'wb+')
    # 分块写入文件  
    for chunk in myfile.chunks():      
           file.write(chunk)  
    # 关闭文件
    file.close()

    # 返回文件的url路径
    return '/static/pics/'+filename+'.'+hzm


def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')