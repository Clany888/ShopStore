from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Types

from django.contrib.auth.decorators import permission_required


# 商品分类添加页面
@permission_required('myadmin.insert_types',raise_exception = True)

def typesadd(request):

    context = {'tlist':GetTypesAll()}    
    return render(request,'admin/types/add.html',context)

# 执行商品分的添加
@permission_required('myadmin.insert_types',raise_exception = True)
def typesinsert(request):
    try:
        # 创建模型对象
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        if ob.pid == '0':
            ob.path = '0,'
        else:
            # 如果不是添加的顶级分类,需要获取父类的path路径,拼接上 pid ,
            p = Types.objects.get(id=ob.pid)
            ob.path = p.path+str(ob.pid)+','
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="/admin/types/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/types/add/"</script>')


# 分类列表

@permission_required('myadmin.show_types',raise_exception = True)

def typeslist(request):
    # 判断是否有搜索条件
    if request.GET.get('keywords',None):
        data = Types.objects.filter(name__contains=request.GET.get('keywords'))
        for x in data:
            if x.pid == 0:
                x.pname = '顶级分类'
            else:
                p = Types.objects.get(id=x.pid)
                x.pname = p.name
    else:
        # 获取全部
        data = GetTypesAll()

    # 分页
    # 数据分页类
    from django.core.paginator import Paginator
    # 实例化分页类  参数1 查询的数据,参数2 每页要显示的数据
    paginator = Paginator(data,10)

    # 当前页码
    p = int(request.GET.get('p',1))

    # 根据当前页码获取当前页应该显示的数据
    tlist = paginator.page(p)


    # 分配数据
    context = {'tlist':tlist}
    # 加载模板 
    return render(request,'admin/types/list.html',context)

# 获取所有分类 排序
def GetTypesAll():

    # 获取所有的商品分类
    # ob = Types.objects.all()
    # select *,concat(path,id) as paths from myadmin_types order by paths;
    ob = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    for x in ob:
        # 控制当前对象的 缩进
        # p = x.path.split(',')
        n =  int(len(x.path) / 2)-1
        x.name = (n*'|----')+x.name
        # 给当前对象 添加一个所属父类的属性
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            obj = Types.objects.get(id=x.pid)
            x.pname = obj.name

    return ob



# 编辑
@permission_required('myadmin.edit_types',raise_exception = True)

def typesedit(request,tid):

    # 根据tid获取当前数据对象
    ob = Types.objects.get(id=tid)

    #
    context = {'tinfo':ob,'tlist':GetTypesAll()}

    return render(request,'admin/types/edit.html',context) 
    

#执行修改
@permission_required('myadmin.edit_types',raise_exception = True)

def typesupdate(request):

    try:

        # 获取当前对象,执行修改
        ob = Types.objects.get(id=request.POST['tid'])
        ob.name = request.POST['name']
        ob.save()
    
        return HttpResponse('<script>alert("修改成功");location.href="/admin/types/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/types/edit/'+request.POST['tid']+'/"</script>')


# 执行删除
@permission_required('myadmin.del_types',raise_exception = True)
def typesdel(request):
    # 查询当前类下是否还有子类
    num = Types.objects.filter(pid=request.GET['tid']).count()


    # 判断是否还子类
    if num :
        # 还有子类
        return JsonResponse({'status':1,'msg':'当前类下还有子类,不能删除'})

    # 没有子类
    ob = Types.objects.get(id = request.GET['tid'])
    ob.delete()

    return JsonResponse({'status':0,'msg':'可以删除'})
