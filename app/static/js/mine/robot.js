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
        group: {
            num: "",
            name: "",
            key: "",
        }
    },
    methods: {
        logout: function () {
            logout();
        },
        addKey: function () {
            app.showMenu = false;
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['300px', 'auto'],
                //shade: true,
                title: "添加记录", //不显示标题
                content: $('#pwdDiv'),  //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                yes: function () {
                    if (app.group.num == "" || app.group.name == "" || app.group.key == "") {
                        showAlertError('信息填写不完整');
                        return false;
                    }
                    addKey(app.group);
                },
                cancel: function () {
                    app.group = {
                        num: "",
                        name: "",
                        key: "",
                    }
                }
            });
        },
        deleteKey: function (id) {
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                $.ajax({
                    url: "/robot.html/" + id,
                    method: "DELETE",
                    success: function (res) {
                        if (res.success) {
                            showOK(res.msg);
                            getKeys(app, false);
                        } else {
                            showError(res.msg)
                        }

                    }
                });
            }, function () {
            });
        }
    }
});

//设置QQ号
function addKey(data) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/robot.html/add",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                layer.closeAll();
                showOK(res.msg);
                getKeys(app, false);
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

    getKeys(app, false);
});

function getKeys(app, append) {
    $.ajax({
        url: baseUrl + "/robot.html/getall",
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