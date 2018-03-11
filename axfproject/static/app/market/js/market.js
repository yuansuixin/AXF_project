$(function () {
    //全部类型
    $("#type_toggle").click(function () {
        //符号的改变
        $(this).find('#all_type_icon').removeClass('glyphicon-menu-down').addClass('glyphicon-menu-up')
        // siblings 查找每个元素的所有同胞元素
        $('#sort_icon').removeClass('glyphicon-menu-up').addClass('glyphicon-menu-down')
        $('#typeid').show();
        $('#sortdid').hide();
    })
    //显示类型具体分类
    $('#typeid').click(function () {
        $(this).hide();
    })
    //综合排序
    $('#sort_toggle').click(function () {
        $(this).find("#sort_icon").removeClass("glyphicon-menu-down").addClass("glyphicon-menu-up");
        $("#all_type_icon").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
        $('#sortdid').show();
        $('#typeid').hide();
    })
    //显示排序的类型
    $('#sortdid').click(function () {
        $("#sort_icon").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
        $(this).hide();
    })

//    对加减号添加点击,将商品添加到购物车或者减少
    $('.addgoods').click(function () {

        //    添加商品到购物车 商品的唯一标识id
        //    prop获取的设置的都是系统中自带的属性，
        //    attr可以获取任意属性
        //     var goodsid = $(this).prop('goodsid')
        //     console.log('prop'+goodsid)
        var goodsid = $(this).parents('section').attr('goodsid');
        var goods = $(this);
        $.getJSON('/app/addtocart/', {'goodsid': goodsid}, function (data) {
            if (data['status'] == '302') {
                //bom的对象
                window.open('/app/login/', target = '_self')
            } else if (data['status'] == '200') {
                // console.log(data['c_num']);
                //将页面的购物车的地方将数量更新
                goods.prev('span').html(data['c_num']);
            }
        })
    })
    //减商品数量
    $('.subgoods').click(function () {
        var subgoods = $(this);
        var goodsid = subgoods.parents('section').attr('goodsid');
        // console.log(goodsid)
        var goods_num = subgoods.next('span');
        // console.log(goods_num)
        if (goods_num.html() != 0) {
            $.getJSON('/app/subtocart/', {'goodsid': goodsid}, function (data) {
                if (data['status'] == '302') {
                    //bom的对象
                    window.open('/app/login/', target = '_self')
                } else if (data['status'] == '302') {
                    goods_num.html(data['num'])
                } else if (data['status'] == '202') {
                    console.log('操作数据不存在')
                }
            })
        } else {
            //不进行ajax请求
            console.log('操作无效')
        }
    })
})