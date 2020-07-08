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
    created(){
        this.getKeys(this, false);
    },
    methods: {
        logout:function() {
            logout();
        },

getKeys:function (app, append) {
    $.ajax({
        url: baseUrl + "/tools",
        method: "GET",
        success: function (res) {
            if (res.success) {
                if (append) {
                    for (let v in res.data.list) {
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
},
        addKey:function() {
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
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                            $.ajax({
                url: "/tools/" + key,
                method: "DELETE",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        app.getKeys(app, false);
                    } else {
                        showError(res.msg)
                    }

                }
            });
            }, function () {
            });
        },
        compress: function () {
            $.ajax({
                url: "/tools/compress",
                // data: JSON.stringify(key),
                method: "GET",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                    } else {
                        showError(res.msg)
                    }
                }
            });
        },
        importKeys: function () {
            $.ajax({
                url: "/tools/import",
                method: "GET",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        app.getKeys(app, false);
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
        url: baseUrl + "/tools/" + key,
        method: "POST",
        success: function (res) {
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    app.getKeys(app, false);
                } else {
                    showAlertError(res.msg)
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
});


$('select.dropdown')
    .dropdown()
;