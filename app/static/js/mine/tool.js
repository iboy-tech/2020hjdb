/**
 @File    : tool.py
 @Time    : 2020/3/12 23:26
 @Author  : iBoy
 @Email   : iboy@iboy.tech
 @Description :
 @Software: PyCharm
 */
var app = new Vue({
    el: "#app",
    data: {
        list: [],
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
    },
    methods: {
        logout() {
            logout();
        },
        addKey() {
            // alert("执行了");
            app.showMenu = false;
            layer.prompt({title: '请输入秘钥：'}, function (key, index) {
                if (key == '') {
                    showAlertError('Key不可为空！');
                    return false;
                }
                //layer.close(index);
                addKey(key);
            });
        },
        deleteKey: function (key) {
            $.ajax({
                url: "/tool.html/deleteKey?key=" + key,
                // data: JSON.stringify(key),
                method: "POST",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        getKeys(app, false);
                    } else {
                        showError(res.msg)
                    }

                }
            });
        },
        compress: function () {
            $.ajax({
                url: "/tool.html/compress",
                // data: JSON.stringify(key),
                method: "POST",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                    } else {
                        showError(res.msg)
                    }
                }
            });
        },
        importKeys:function () {
            $.ajax({
                url: "/tool.html/import",
                method: "POST",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        getKeys(app, false);
                    } else {
                        showError(res.msg)
                    }
                }
            });
        }
    }
});

//设置QQ号
function addKey(key) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/tool.html/addKey?key=" + key,
        //data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    getKeys(app, false);
                } else {
                    showAlertError(res.msg)
                }
            } else {
                console.log(res);
                showAlertError(res)
            }
        }
    });
}

$(function () {
    var menuLeft = document.getElementById('cbp-spmenu-s1'),
        showLeftPush = document.getElementById('showLeftPush'),
        body = document.body;
    showLeftPush.onclick = function () {
        classie.toggle(this, 'active');
        classie.toggle(body, 'cbp-spmenu-push-toright');
        classie.toggle(menuLeft, 'cbp-spmenu-open');
        disableOther('showLeftPush');
    };

    function disableOther(button) {
        if (button !== 'showLeftPush') {
            classie.toggle(showLeftPush, 'disabled');
        }
    }

    getKeys(app, false);
});

function getKeys(app, append) {
    $.ajax({
        url: baseUrl + "/tool.html/getall",
        // data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            if (res.success) {
                if (append) {
                    for (let v in res.data.list) {
                        //console.log(v);
                        app.list.push(res.data.list[v]);
                    }
                } else {
                    app.list = res.data.list;
                }
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

$('select.dropdown')
    .dropdown()
;