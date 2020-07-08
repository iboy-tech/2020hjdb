var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        search: {
            keyword: "",
            pageNum: 0,
            pageSize: 120
        },
        result: {
            totalPage: 0,
            total: 0,
            list: []
        },
        checkedList: [],
        checked: false,
        api: 'https://wpa.qq.com/msgrd?v=3&site=qq&menu=yes&uin=',
    },
    computed: {
        currentPage: function () {
            return this.search.pageNum + 1;
        }
    },
    methods: {
        toPage: function (pageNum) {
            console.log(pageNum);
            if (pageNum < 0 || pageNum >= this.result.totalPage) {
                return;
            }
            this.search.pageNum = pageNum;
            getUserList(app.search, app, false);
        },
        checkAll: function () {
            if (this.checked == false) {
                this.checkedList = [];//清空数据
            } else {
                this.result.list.forEach((item) => {
                    if (this.checkedList.indexOf(item.userId) == -1) {
                        this.checkedList.push(item.userId);
                    }
                })
            }
        },
        deleteAll: function () {
            let data = this.checkedList;
            layer.confirm('你确定要批量删除 ' + data.length + ' 条数据吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                $.ajax({
                    url: baseUrl + "/users",
                    method: "DELETE",
                    data: JSON.stringify(data),
                    success: function (res) {
                        if (res.success) {
                            app.checked = false;
                            app.checkedList = [];
                            showOK(res.msg);
                            //数据置空
                            getUserList(app.search, app, false);
                        } else {
                            showAlertError(res.msg)
                        }
                    }
                });
            }, function () {
            });
        },
        submit: function () {
            let pgNum = $('#pgNum').val() - 1;
            this.search.pageNum = pgNum < 0 ? 0 : pgNum;
            getUserList(app.search, app, false);
        },
        // 重发认证邮件
        reSend: function (id) {
            $.ajax({
                url: baseUrl + "/users/resend/" + id,
                method: "GET",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg)
                    } else {
                        showError(res.msg);
                    }
                }
            });
        },

        freezeUser: function (userId) {
            layer.confirm('冻结后该用户将无法再登录系统，确定要冻结吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                freezeUser(userId)
            }, function () {
            });
        },
        unfreezeUser: function (userId) {
            layer.confirm('解冻后用户可正常登录并发布信息，确定要解冻吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                unfreezeUser(userId)
            }, function () {
            });
        },
        setAsManager: function (userId, flag) {
            if (flag == 1) {
                layer.confirm('设置为管理员的账号可登录后台，请谨慎操作，确定要将其设置为管理员吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    setAsAdmin(userId);
                }, function () {
                });
            } else {
                layer.confirm('你确定要取消管理员吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    setAsAdmin(userId);
                }, function () {
                });
            }

        },
        logout: function () {
            logout();
        },
        deleteUser: function (userId) {
            //询问框
            layer.confirm('危险操作，你确定要这样做吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteUser(userId);
            }, function () {
            });
        },
        resetPassword: function (userId) {
            //询问框
            layer.confirm('确定吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                resetPassword(userId);
            }, function () {
            });
        }
    }
});


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

    getUserList(app.search, app, false);
});

//获取用户列表
function getUserList(data, app, append) {
    $.ajax({
        url: baseUrl + "/users",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                app.search.pageNum = res.data.page.pageNum;
                app.search.pageSize = res.data.page.pageSize;
                app.result.totalPage = res.data.page.totalPage;
                app.result.total = res.data.page.total;
                if (append) {
                    for (let v in res.data.page.list) {
                        //console.log(v);
                        app.result.list.push(res.data.page.list[v]);
                    }
                } else {
                    app.result.list = res.data.page.list;
                }
            }
        }
    });
}

//重置密吗
function resetPassword(userId) {
    $.ajax({
        url: baseUrl + "/users/password/"+userId,
        method: "GET",
        beforeSend: function () {
            showLoading();
        },
        success: function (res, status) {
            console.log('我是res' + res);
            if (status == "success") {
                if (res.success) {
                    showOK();
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

//设置/取消用户为管理员
function setAsAdmin(userId) {
    $.ajax({
        url: baseUrl + "/users/admin/" + userId,
        method: "GET",
        //data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK();
                    getUserList(app.search, app, false);
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

//冻结用户
function freezeUser(userId) {
    $.ajax({
        url: baseUrl + "/users/freeze/" + userId,
        method: "GET",
        beforeSend: function () {
            showLoading();
        },
        success: function (res) {
                if (res.success) {
                    showOK();
                    getUserList(app.search, app, false);
                } else {
                    showAlertError(res.msg)
                }
        },
        complete: function () {
            hideLoading();
        }
    });
}

//删除用户
function deleteUser(userId) {
    $.ajax({
        url: baseUrl + "/users/delete/" + userId,
        method: "DELETE",
        success: function (res) {
            if (res.success) {
                showOK();
                getUserList(app.search, app, false);
            } else {
                showAlertError(res.msg);
            }
        },
    });
}

//解冻用户
function unfreezeUser(userId) {
    $.ajax({
        url: baseUrl + "/users/freeze/" + userId,
        method: "GET",
        beforeSend: function () {
            showLoading();
        },
        success: function (res) {
                if (res.success) {
                    showOK();
                    getUserList(app.search, app, false);
                } else {
                    showAlertError(res.msg)
                }
        },
        complete: function () {
            hideLoading();
        }
    });
}