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
            id: "",
            num: "",
            name: "",
            key: "",
        },
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
                        id:"",
                        num: "",
                        name: "",
                        key: "",
                    }
                }
            });
        },
        updateKey: function (item) {
            this.group.id = item.Id;
            this.group.name = item.groupName;
            this.group.num = item.groupNum;
            this.group.key = item.Key;
            app.showMenu = false;
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['300px', 'auto'],
                //shade: true,
                title: "修改记录", //不显示标题
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
                        id:1,
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
                    url: "/robots/" + id,
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
        url: baseUrl + "/robots",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                layer.closeAll();
                showOK(res.msg);
                getKeys(app, false);
                app.group = {
                        id:"",
                        num: "",
                        name: "",
                        key: "",
                    }
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
        url: baseUrl + "/robots",
        method: "GET",
        success: function (res) {
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