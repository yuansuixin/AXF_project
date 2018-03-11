function check() {

    var password = $('#password').val();
    password = password.trim()//切除空格
    if (password.length==0){
        return true
    }

    if (password.length < 6 | password.length > 16) ;
    return false;

    var repassword = $('#password_confirm').val();
    if (password != repassword) {
        return false
    }

    var newpassword = md5(password);
    $('#password_confirm').val(newpassword)
    return true
}

$(function () {
    $('#password').change(function () {
        var password = $(this).val();
        password = password.trim()

        if (password.length == 0) {
            console.log('不想改变密码了')
        }else if(password.length < 6 | password.length > 16){
            console.log('密码不符合规范')
        }else {
            console.log('密码符合')
        }
        //            错误提示

    })
    $('#password_confirm').change(function () {
        var password = $('#password').val()
        var password_confirm = $(this).val();
        if (password == password_confirm) {
            //    错误提示
        } else {

        }

    })
})
