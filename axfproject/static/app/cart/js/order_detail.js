$(function () {

    $('#alipay').click(function () {

        var orderid = $(this).attr('orderid');
        $.getJSON('/app/pay/',{'orderid':orderid},function (data) {
            console.log(data);
            if (data['status']=='200'){
                window.open('/app/mine/',target='_self')
            }else {
                console.log('支付失败')
            }

        })

    })
})