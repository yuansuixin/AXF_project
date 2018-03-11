from django.conf.urls import url

from app import views

urlpatterns = [
    #首页
    url(r'^home/$', views.home, name='home'),
    # 极速购买
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<sortrule>\d+)/', views.marketWithParams,
        name='marketwithparams'),
    # 购物车
    url(r'^cart/$', views.cart, name='cart'),
    # 我的
    url(r'^mine/$', views.mine, name='mine'),

    #注册
    url(r'^register/$',views.register,name='register'),
    # 检验用户名是否存在,使用的是异步ajax
    url(r'^checkuser/$',views.checkuser,name='checkuser'),
    # 登录,退出
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^login/$',views.login,name='login'),
    # 用户信息修改
    url(r'^userinfo/$',views.userinfo,name='userinfo'),

    # 添加到购物车
    url(r'^addtocart/$',views.addtocart,name='addtocart'),
    url(r'^subtocart/$',views.subtocart,name='subtocart'),


    #购物车的商品列表里的商品数量的加减
    url(r'^subcartgoods/$',views.subcartgoods,name='subcartgoods'),
    url(r'^addcartgoods/$',views.addcartgoods,name='addcartgoods'),

    # 购物车里的商品是否选中
    url(r'^changecheck/$',views.changecheck,name='changecheck'),
    url(r'^generateorder/$',views.generateorder,name='generateorder'),
    url(r'^orderdetail/$',views.orderdetail,name='orderdetail'),
    url(r'^pay/$',views.pay,name='pay'),
    url(r'^notpaylist/$',views.notpaylist,name='notpaylist'),
    url(r'^notreceivelist/$',views.notreceivelist,name='notreceivelist'),

]
