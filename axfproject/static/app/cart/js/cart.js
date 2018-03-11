$(function () {
    //购物车里的某个商品是否选中
    $('.ischoose').click(function (event) {
        //这里是阻止冒泡
        event.stopPropagation();
        var ischoose = $(this);
        var cartid = ischoose.parents('li').attr('cartid');
        $.getJSON('/app/changecheck/', {'cartid': cartid}, function (data) {
            if (data['is_select']) {
                ischoose.find('span').show();
            } else {
                ischoose.find('span').hide();
            }
        })
    })

    //购物车里减少商品数量
    $('.subgoods').click(function () {
        var clickNode = $(this);
        var cartid = clickNode.parents('li').attr('cartid')
        console.log(cartid)
        $.getJSON('/app/subcartgoods/', {'cartid': cartid}, function (data) {
            if (data['num'] == 0) {
                clickNode.parents('li').hide();
            } else if (data["status"] == "202") {
                console.log("操作数据不存在");
            } else {
                clickNode.next().html(data['num'])
            }
        });
    })
    //购物车里添加一个商品的数量
    $('.addgoods').click(function () {
        var addgoods = $(this);
        var cartid = addgoods.parents('li').attr('cartid')
        console.log(cartid)
        $.getJSON('/app/addcartgoods/', {'cartid': cartid}, function (data) {
            if (data["status"] == "202") {
                console.log("操作数据不存在");
            } else {
                addgoods.prev().html(data['num'])
            }
        });
    })

    //全选
    $('.confirm').click(function () {
        //通过判断选中的数量
        var select_length = $('.select_status').length;
        var select_array = [];
        //没有选中的，全选的时候改变状态
        var unselect_array = [];
        //循环遍历选中的商品
        $('.select_status').each(function (index) {
            var item = $('.select_status').eq(index);
            var cartid = item.parents('li').attr('cartid');
            if (item.css('display') == 'block') {
                select_array.push(cartid);
            } else {
                unselect_array.push(cartid);
            }
        })
        //通过全选框的状态来控制所有的商品是全部选中还是全部不选中
        if (select_array.length == select_length) {
            $('.select_status').css('display', 'none');
            $('.confirm').find('.all_select').css('display', 'none')
        } else {
            $('.select_status').css('display', 'block')
            $('.confirm').find('.all_select').css('display', 'block')
        }
    })

//    下单
    $('.generate_order').click(function () {
        var select_length = $('.select_status').length;
        var select_array = [];
        //没有选中的，全选的时候改变状态
        var unselect_array = [];
        //循环遍历选中的商品
        $('.select_status').each(function (index) {
            var item = $('.select_status').eq(index);
            var cartid = item.parents('li').attr('cartid');
            if (item.css('display') == 'block') {
                select_array.push(cartid);
            } else {
                unselect_array.push(cartid);
            }
        })

        if (select_array.length == 0) {
           alert('请买东西')
            return 'hehe'
        }

        var selects = select_array.join('#')
        $.getJSON('/app/generateorder/',{'selects':selects},function (data) {
            console.log(data);
            if (data['status']=='200'){
                window.open('/app/orderdetail/?orderid='+data['order_num'],target='_self')
            }
        })

    })
})

