from django.db import models


# 由于好几个模型都用到了这几个属性，我们变将它抽象为父类
class BaseMain(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=200)
    trackid = models.CharField(max_length=32)

    # 一定要设置好抽象，就不用创建父类的数据表
    class Meta:
        abstract = True


# 主页的轮播图
class MainWheel(BaseMain):
    class Meta:
        db_table = 'axf_wheel'


# 首页的导航
class MainNav(BaseMain):
    class Meta:
        db_table = 'axf_nav'


# 必买的
class MainMustBuy(BaseMain):
    class Meta:
        db_table = 'axf_mustbuy'


# 主页的商品购买
class MainShop(BaseMain):
    class Meta:
        db_table = 'axf_shop'


# 主要的商品展示
class MainInfo(BaseMain):
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)
    # 一个商品的各种信息
    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'axf_mainshow'


# 分类模型
class MarketFood(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=150)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'


# 商品详情
class MarketGoods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=150)
    # 商品名称
    productname = models.CharField(max_length=50)
    # 商品长名称
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.NullBooleanField(default=False)
    # 是否买一赠一
    pmdesc = models.CharField(max_length=10)
    # 规格
    specifics = models.CharField(max_length=20)
    # 价格
    price = models.CharField(max_length=10)
    # 超市价格
    marketprice = models.CharField(max_length=10)
    # 组id
    categoryid = models.CharField(max_length=10)
    # 子类组id
    childcid = models.CharField(max_length=10)
    # 子类组名称
    childcidname = models.CharField(max_length=10)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'

# 用户
class User(models.Model):
    # 用户账号，要唯一
    # userAccount = models.CharField(max_length=20,unique=True)
    # 密码
    u_password = models.CharField(max_length=32)
    # 昵称
    u_name = models.CharField(max_length=20)
    # 手机号
    # userPhone   = models.CharField(max_length=20)
    # 地址
    u_email = models.CharField(max_length=100)
    # 头像路径
    u_icon = models.ImageField(upload_to='icons')
    # 等级
    # userRank    = models.IntegerField()
    # touken验证值，每次登陆之后都会更新
    # userToken   = models.CharField(max_length=50)
    isDelete = models.BooleanField(default=False)
    # @classmethod
    # def createuser(cls,account,passwd,name,phone,address,img,rank,token):
    #     u = cls(userAccount = account,userPasswd = passwd,userName=name,userPhone=phone,userAdderss=address,userImg=img,userRank=rank,userToken=token)
    #     return u


# 订单表
class Order(models.Model):
    o_create_time = models.DateTimeField(auto_created=True,auto_now=True)
    #  0 订单刚生成米有支付
    # 1 订单支付但未发货
    # 2 订单支付且已发货
    # 3 订单已发货且已收货
    # 4 订单已收货但未评价
    #  5 已收货已评价
    # 6 已收货又退货
    # 7 售后
    o_status = models.IntegerField(default=0)
    o_user = models.ForeignKey(User)

# 购物车的商品
class Cart(models.Model):
    c_num = models.IntegerField(default=1)
    # 购物车的某商品是否选中，默认是选中的
    c_select = models.BooleanField(default=True)
    # false 代表属于购物车，true代表属于订单表
    c_belong = models.BooleanField(default=False)
    c_order = models.ForeignKey(Order,null=True,default=None)
    c_user = models.ForeignKey(User)
    c_goods = models.ForeignKey(MarketGoods)



























