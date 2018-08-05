"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . views import views,typeviews,goodsviews,authviews

urlpatterns = [

    # 后台首页
    url(r'^$',views.index,name='admin_index'),

    # 后台登录
    url(r'^login/$',authviews.mylogin,name='admin_login'),
    # 退出登录
    url(r'^loginout/$',authviews.mylogout,name='admin_loginout'),

    # 验证码 verifycode
    url(r'^getvcode/$',views.verifycode,name='getvcode'),

    # session 会话
    url(r'^test/$',views.test),

    # ajax上传文件
    url(r'^ajax/upload/$',views.ajaxupload,name='admin_ajax_upload'),


    # 后台权限管理

    # 后台用户添加
    url(r'^auth/user/add$',authviews.useradd,name='auth_user_add'),
    # 后台用户列表
    url(r'^auth/user/list$',authviews.userlist,name='auth_user_list'),
    url(r'^auth/user/del/(?P<uid>[0-9]+)$',authviews.userdel,name='auth_user_del'),

    # 后台组添加
    url(r'^auth/group/add$',authviews.groupadd,name='auth_group_add'),
    # 后台组列表
    url(r'^auth/group/list$',authviews.grouplist,name='auth_group_list'),
    url(r'^auth/group/edit/(?P<gid>[0-9]+)$',authviews.groupedit,name='auth_group_edit'),




    # 用户管理

    # 用户添加
    url(r'^user/add/$',views.useradd,name='admin_user_add'),
    # 执行添加
    url(r'^user/insert/$',views.userinsert,name='admin_user_insert'),
    # 用户列表
    url(r'^user/list/$',views.userlist,name='admin_user_list'),
    # 用户删除
    # url(r'^user/del/(?P<uid>[0-9]+)$',views.userdel,name='admin_user_del'),
    url(r'^user/del/$',views.userdel,name='admin_user_del'),
    # 用户编辑
    url(r'^user/edit/(?P<uid>[0-9]+)$',views.useredit,name='admin_user_edit'),
    # 用户修改
    url(r'^user/update/$',views.userupdate,name='admin_user_update'),
    # 用户状态更新
    url(r'^user/status/$',views.userstatus,name='admin_user_status'),


    # 商品分类管理
    url(r'^types/add/$',typeviews.typesadd,name='admin_types_add'),
    url(r'^types/insert/$',typeviews.typesinsert,name='admin_types_insert'),
    url(r'^types/list/$',typeviews.typeslist,name='admin_types_list'),
    url(r'^types/edit/(?P<tid>[0-9]+)$',typeviews.typesedit,name='admin_types_edit'),
    url(r'^types/update/$',typeviews.typesupdate,name='admin_types_update'),
    url(r'^types/del/$',typeviews.typesdel,name='admin_types_del'),


    # 商品管理
    url(r'^goods/add/$',goodsviews.goodsadd,name='admin_goods_add'),
    url(r'^goods/insert/$',goodsviews.goodsinsert,name='admin_goods_insert'),
    url(r'^goods/list/$',goodsviews.goodslist,name='admin_goods_list'),

 
]
