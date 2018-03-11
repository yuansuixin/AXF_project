$(function () {
    //对用户名和密码做的校验,使用的是ajax
    $('#username').change(function () {
        var username = $(this).val();
        $.get("/app/checkuser/", {'username': username}, function (data) {
            console.log(data);
            if (data['status'] == '888') {
                $('#username_info').html(data['msg']).css('color', 'green');
            } else {
                $('#username_info').html(data['msg']).css('color', 'red');
            }
        })


        $('#password').change(function () {
            var password = $(this).val();
            if (password.length < 6 | password.length > 16) {
                $('#password_info').html('密码长度不符合规范').css('color','red');
            } else {
                $('#password_info').html('密码长度符合规范').css('color','green');
            }
        })


        $('#password_confirm').change(function () {
            var passwordConfig = $(this).val();
            var password = $('#password').val();
            if (password == passwordConfig) {
                $('#repsw_info').html('密码一致').css('color','green');
            } else {
                $('#repsw_info').html('密码不一致').css('color','red');
            }
        })
    })


})
//提交表单的时候进行摘要，信息更安全
function check() {
    var password = $('#password').val();
    var passwordconfirm = $('#password_confirm').val();
    if (password != passwordconfirm) {
        return false
    }
    var newpassword = md5(password);
    //最后将密码设置为密文
    $('#password').val(newpassword);
    return true;
}










