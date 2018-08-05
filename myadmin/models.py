from django.db import models

# Create your models here.


# 会员模型
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=77)
    email = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=11,null=True)
    sex = models.CharField(max_length=1,null=True)
    age = models.IntegerField(null=True)
    picurl = models.CharField(max_length=100,default='/static/pics/default/default.jpg')
    # 0 正常 1 禁用  3删除  2管理员
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_users", "查看会员管理"),
            ("insert_users", "添加会员"),
            ("edit_users", "修改会员"),
            ("del_users", "删除会员"),
        )


# 商品分类模型
class Types(models.Model):
    name = models.CharField(max_length=50)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)


    def __str__(self):
        return '<Types: Types '+self.name+'>'

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_types", "查看商品分类管理"),
            ("insert_types", "添加商品分类"),
            ("edit_types", "修改商品分类"),
            ("del_types", "删除商品分类"),
        )




# 商品模型
class Goods(models.Model):
    # 商品所属分类
    typeid = models.ForeignKey(to="Types", to_field="id")
    # 商品标题
    title = models.CharField(max_length=255)
    # 商品价格
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # 商品库存
    storage = models.IntegerField()
    # 商品图片
    pic = models.CharField(max_length=50)
    # 商品详情
    info = models.TextField()
    # 购买数量
    num  =  models.IntegerField(default=0)
    # 点击次数
    clicknum =  models.IntegerField(default=0)
    # 商品状态 1：新品、2：热销、3：下架
    status = models.IntegerField(default=1)
    # 商品添加时间
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_goods", "查看商品管理"),
            ("insert_goods", "添加商品"),
            ("edit_goods", "修改商品"),
            ("del_goods", "删除商品"),
        )

# 会员收货地址 模型

class Address(models.Model):
    # 用户id
    uid = models.ForeignKey(to="Users", to_field="id")
    # 收货人
    aname = models.CharField(max_length=20)
    # 收货地址
    aads = models.CharField(max_length=255)
    # 收货电话
    aphone = models.CharField(max_length=11)
    # 是否为默认 1 默认,
    status = models.IntegerField(default=0)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_address", "查看地址管理"),
            ("insert_address", "添加地址"),
            ("edit_address", "修改地址"),
            ("del_address", "删除地址"),
        )


# 订单表
class Order(models.Model):
    uid = models.ForeignKey('Users',to_field="id")
    address = models.ForeignKey('Address',to_field='id')
    totalprice = models.FloatField()
    totalnum = models.IntegerField()
    # 1 未付款 2已付款,待发货,3已发货,待收货,4已完成,5已取消
    status = models.IntegerField()
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_order", "查看订单管理"),
            ("insert_order", "添加订单"),
            ("edit_order", "修改订单"),
            ("del_order", "删除订单"),
        )


# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey('Order',to_field="id")
    gid =  models.ForeignKey('Goods',to_field="id")
    num = models.IntegerField()
    price = models.FloatField()

