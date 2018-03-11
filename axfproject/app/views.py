import hashlib

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainInfo, MarketFood, MarketGoods, User, Cart, Order


# 首页
def home(request):
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuy = MainMustBuy.objects.all()
    shoplist = MainShop.objects.all()
    # print(shoplist)
    # 切取需要显示的信息,使信息显示在特定的位置
    shop1 = shoplist[0]
    shop2 = shoplist[1:3]
    shop3 = shoplist[3:7]
    shop4 = shoplist[7:11]

    mainInfo = MainInfo.objects.all()

    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        'mustbuy': mustbuy,
        'shop1': shop1,
        'shop2': shop2,
        'shop3': shop3,
        'shop4': shop4,
        'mainlist': mainInfo,
    }
    return render(request, 'app/home/home.html', context=data)


# 极速购物的页面,因为这里使三级联动,做到增量开发,我们使用了重定向
def market(request):
    return redirect(reverse("app:marketwithparams", kwargs={'typeid': '104749', 'childcid': '0', 'sortrule': '0'}))


# 接受参数的购物页面
def marketWithParams(request, typeid, childcid, sortrule):
    # 左边的全部分类
    leftSlide = MarketFood.objects.all()
    # 商品详情
    goodsList = MarketGoods.objects.filter(categoryid=typeid)
    # 获取商品的分类具体的信息,
    foodtype = leftSlide.filter(typeid=typeid).first()
    # print(foodtype)
    # 通过切片,切取到每个分类对应的子分类
    childtypesTran = []
    childtypes = foodtype.childtypenames.split('#')
    for item in childtypes:
        itemchild = item.split(":")
        childtypesTran.append(itemchild)
    # [['全部分类', '0'], ['饮用水', '103550'], ['茶饮/咖啡', '103554'], ['功能饮料', '103553'], ['酒类', '103555'], ['果汁饮料', '103551'],
    # ['碳酸饮料', '103552'], ['整箱购', '104503'], ['植物蛋白', '104489'], ['进口饮料', '103556']]
    print(childtypesTran)

    # 从数据库中过滤出相匹配的数据,默认使用的使0
    if childcid != '0':
        goodsList = goodsList.filter(childcid=childcid)

    '''
    1,综合排序
    2，销量降序
    3，销量升序
    '''
    if sortrule == '1':
        goodsList = goodsList.order_by('productnum')
    elif sortrule == '2':
        goodsList = goodsList.order_by('-productnum')
    elif sortrule == '3':
        goodsList = goodsList.order_by('-price')
    elif sortrule == '4':
        goodsList = goodsList.order_by('price')

    data = {
        "title": "闪购",
        'leftSlide': leftSlide,
        'productlist': goodsList,
        'childtypetran': childtypesTran,
        'typeid': typeid,
        'childcid': childcid,
    }
    return render(request, 'app/market/market.html', context=data)

# 购物车页面
def cart(request):
    # 这里是判断当前用户有没有登录
    username = request.session.get('username')
    if not username:
        return redirect(reverse('app:login'))

    users = User.objects.filter(u_name=username)
    if users.exists():
        user = users.first()
    # user = User() 筛选出属于购物车的商品列表，取出外键关联的表的信息
        goodsList = user.cart_set.filter(c_belong=False)
    else:
        # 重定向到注册页面
        return redirect(reverse('app:register'))

    data = {
        "title": "购物车",
        'goodsList':goodsList,
    }
    return render(request, 'app/cart/cart.html', context=data)


def mine(request):
    username = request.session.get('username')

    data = {
        "title": "我的",
    }
    if username:
        user = User.objects.get(u_name=username)
        # 获取到头像
        data['icon'] = user.u_icon.url
        data['username'] = username
        # 判断是否登录使用
        data['islogin'] = 'login'

        not_pay_num = Order.objects.filter(o_user=user).filter(o_status=0).count()
        not_receive_num = Order.objects.filter(o_user=user).filter(o_status=1).count()
        data['not_pay'] = not_pay_num
        data['not_receive'] = not_receive_num


    return render(request, 'app/mine/mine.html', context=data)

# 注册
def register(request):
    # 这里使用的是聚合，通过表单的method方法的值来区分是否是来自与表单的提交
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES['icon']
        print(password)
        #     需要再次判断
        #     信息安全
        password = password2md5(password)
        user = User()
        user.u_name = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon
        user.save()
        response = redirect(reverse('app:mine'))
        request.session['username'] = username
        return response
    elif request.method == "GET":
        return render(request, 'app/mine/user/register.html')


# 检验用户名,这里使用的是异步请求,ajax
def checkuser(request):
    username = request.GET.get('username')
    users = User.objects.filter(u_name=username)
    data = {
        'msg': '用户名可用',
        'status': '888',
    }
    if users.exists():
        data['msg'] = '用户名已存在'
        data['status'] = '900'
    print(JsonResponse(data))
    return JsonResponse(data)


# md5摘要
def password2md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

# 退出登录
def logout(request):
    # 同时删除cookie和session
    request.session.flush()
    return redirect(reverse('app:mine'))

# 登录
def login(request):
    # 聚合,低耦合高内聚
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # 判断是否有该用户
        users = User.objects.filter(isDelete=False).filter(u_name=username)
        if users.exists():
            user = users.first()
            u_password = user.u_password
            password = password2md5(password)
            if u_password == password:
                print('********密码一致********')
                request.session['username'] = username
                return redirect(reverse('app:mine'))
        return render(request, 'app/mine/user/login.html', {'psd_info': '用户名或密码错误'})
        # return HttpResponse('用户名或密码错误')
    elif request.method == 'GET':
        return render(request, 'app/mine/user/login.html')


# 修改用户信息
def userinfo(request):
    if request.method == 'POST':
        username = request.session.get('username')
        users = User.objects.filter(u_name=username)
        if users.exists():
            user = users.first()
            password = request.POST.get('password')
            if password:
                user.u_password = password2md5(password)
            #     这里最好使用get方法获取，如果使用【】的那种形式，当值为空的时候，就会崩
            icon = request.FILES.get('icon')
            if icon:# 没有
                user.u_icon = icon
            user.save()
            return redirect(reverse('app:mine'))
    elif request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.filter(u_name=username).first()
        email = user.u_email
        data = {
            'username': username,
            'email': email,
        }
        # print(username,email,icon)
        return render(request, 'app/mine/user/userinfo.html',context=data)

# 添加到购物车
def addtocart(request):
    username = request.session.get('username')
    data={
        'status':'200',
        'msg':'ok'
    }
    # ajax请求的，则返回的也是返回到ajax，判断用户是否登录
    if not username:
        data['status'] = '302'
        data['msg'] = '用户未登录'
        return JsonResponse(data)
    # 获取到商品的id
    goodsid = request.GET.get('goodsid')
    # 找到对应的商品
    goods = MarketGoods.objects.filter(pk=goodsid).first()
    user = User.objects.filter(u_name=username).first()
    # 从购物车里检索这个商品，如果有的话，数量加1，如果没有就新建一个
    cart_item = Cart.objects.filter(c_user=user).filter(c_goods=goods).filter(c_belong=False).first()
    if not cart_item:
        cart_item = Cart()
    else:
        cart_item.c_num = cart_item.c_num+1
    cart_item.c_goods = goods
    cart_item.c_user = user
    cart_item.save()
    data['c_num'] = cart_item.c_num
    return JsonResponse(data)

# 减少商品
def subtocart(request):
    '''
    状态码：
    302：用户未登录
    202：购物车里不存在这个商品
    200：减少商品成功
    :param request:
    :return:
    '''
    username = request.session.get('username')
    data = {
        'status':'200',
        'msg':'ok',
    }
    if not username:
        data['status'] = '302'
        data['msg'] = '用户未登录'
        return JsonResponse(data)

    user = User.objects.filter(u_name=username).first()
    goodsid = request.GET.get('goodsid')
    goods = MarketGoods.objects.filter(pk=goodsid).first()
    carts = Cart.objects.filter(c_belong=False).filter(c_user=user).filter(c_goods=goods)
    if carts.exists():
        cart_item = carts.first()
        if cart_item.c_num == 1:
            cart_item.delete()
            data['num'] = 0
        else:
            cart_item.c_num = cart_item.c_num-1
            cart_item.save()
            data['num'] = cart_item.c_num
    else:
        data['status'] = '202'
        data['msg'] = '操作的数据不存在'
    return JsonResponse(data)

# 购物车里的商品是否选中
def changecheck(request):
    cartid  = request.GET.get('cartid')
    cart_item = Cart.objects.get(pk=cartid)
    cart_item.c_select = not cart_item.c_select
    cart_item.save()
    data={
        'status':'200',
        'msg':'ok',
        'is_select':cart_item.c_select,
    }
    return JsonResponse(data)

#减少购物车里的商品的数量
def subcartgoods(request):
    cartid = request.GET.get('cartid')
    print(cartid)
    carts = Cart.objects.filter(pk=cartid)
    # print(cart_item,cart_item.c_num)
    # print(carts,'***********')
    data={
        'status':'200',
        'msg':'ok',
    }
    if carts.exists():
        cart_item = carts.first()
        # 商品数量为1时删除
        if cart_item.c_num == 1:
            cart_item.delete()
            data['num'] = 0
        else:
            cart_item.c_num = cart_item.c_num-1
            cart_item.save()
            data['num'] = cart_item.c_num
    else:
        data["status"] = "202"
        data["msg"] = "操作数据不存在"
    return JsonResponse(data)

#添加购物车里
def addcartgoods(request):
    cartid = request.GET.get('cartid')
    carts = Cart.objects.filter(pk=cartid)
    data = {
        'status': '200',
        'msg': 'ok',
    }
    if carts.exists():
        cart_item = carts.first()
        cart_item.c_num = cart_item.c_num+1
        cart_item.save()
        data['num'] = cart_item.c_num
    else:
        data["status"] = "202"
        data["msg"] = "操作数据不存在"
    return JsonResponse(data)


def generateorder(request):

    selects = request.GET.get('selects')
    select_list = selects.split('#')
    print(select_list)
    data={
        'status':'200',
        'msg':'ok',
    }
    username = request.session.get('username')
    user = User.objects.get(u_name=username)
    order = Order()
    order.o_user = user
    order.save()
    for item in select_list:
        cart_item = Cart.objects.get(pk=item)
        cart_item.c_belong = True
        cart_item.c_order = order
        cart_item.save()

    data['order_num'] = order.id

    return JsonResponse(data)


def orderdetail(request):
    username = request.session.get('username')
    user = User.objects.get(u_name=username)

    orderid = request.GET.get('orderid')

    order = Order.objects.get(pk=orderid)
    goodsinfos = order.cart_set.all()



    data = {
        'user':user,
        'goodsinfos':goodsinfos,
        'orderid':orderid,
    }

    return render(request,'app/market/order/order_detail.html',context=data)


def pay(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)
    order.o_status = 1
    order.save()
    data = {
        'status':'200',
        'msg':'ok',
    }
    return JsonResponse(data)


def notpaylist(request):
    username = request.session.get('username')
    data = getOrders(0,username)
    return render(request,'app/market/order/order_list.html',data)


def notreceivelist(request):
    username = request.session.get('username')
    data = getOrders(1,username)
    return render(request,'app/market/order/order_list_not_receive.html',data)

def getOrders(status,username):
    if not username:
        return redirect(reverse('app:login'))
    user = User.objects.get(u_name=username).first()
    orderlist = Order.objects.filter(o_user=user).filter(o_status=0)
    data = {
        'orderlist': orderlist,
    }
    return data

