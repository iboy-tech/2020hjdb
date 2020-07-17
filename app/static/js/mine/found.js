var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        result: {
            search: {//tab0
                "kind": -1,
                "category": "",
                "keyword": "",
                "username": "",
                "pageNum": 0,
                "pageSize": 15,
                "flag": 1,
            },
            totalPage: 0,
            total: 0,
            list: []
        },
        checkedList: [],
        checked: false,
        userInfo: {
            userId: "001",
            name: "iBoy",
            username: "201811128",
            gender: "male",
            qq: "547142436",
            classNum: "1521805",
            major: "soft making",
            academy: "soft academy",
            lastLogin: "2020-02-20 13:00",
            status: 2
        }
    },
    computed: {
        currentPage: function () {
            return this.result.search.pageNum + 1;
        }
    },

    methods: {
        freezeUser:function(userId, flag) {
            if (flag == 1) {
                layer.confirm('冻结后该用户将无法再登录系统，确定要冻结吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    freezeUser(userId, flag)
                }, function () {
                });
            } else {
                layer.confirm('取消冻结后用户可正常登录系统，你确定要取消吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    freezeUser(userId, flag)
                }, function () {
                });
            }
        },
        seeInfo:function(userId) {
            console.log(userId);
            getUserInfo(userId, this);
        },
        checkAll:function() {
            if (this.checked == false) {
                this.checkedList = [];//清空数据
            } else {
                this.result.list.forEach((item) => {
                    if (this.checkedList.indexOf(item.id) == -1) {
                        this.checkedList.push(item.id)
                    }
                })
            }
        },
        deleteAll:function() {
            let data=this.checkedList;
            layer.confirm('你确定要批量删除 '+data.length+' 条数据吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                $.ajax({
                    url: baseUrl + "/lostfounds",
                    method: "DELETE",
                    data: JSON.stringify(data),
                    success: function (res) {
                            if (res.success) {
                                //数据置空
                                app.checked=false;
                                app.checkedList=[];
                                showOK(res.msg);
                                pageLostFound(app.result.search, app.result, false);
                            } else {
                                showAlertError(res.msg)
                            }
                    }
                });
            }, function () {
            });
        },
         resend:function(id) {
            layer.confirm('你确定要重新发布吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                $.ajax({
                    url: baseUrl + "/lostfounds/resend/"+id,
                    method: "GET",
                    success: function (res) {
                            if (res.success) {
                                showOK(res.msg);
                            } else {
                                showAlertError(res.msg)
                            }
                    }
                });
            }, function () {
            });
        },
        submit:function() {
            let pgNum = $('#pgNum').val() - 1;
            this.result.search.pageNum = pgNum < 0 ? 0 : pgNum;
            pageLostFound(app.result.search, app.result, false);
        },
        deletePub:function(id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deletePub(id);
            }, function () {
            });

        },
        changePage:function(e) {
            console.log(e);
        },
        toPage:function(pageNum) {
            toPage(pageNum);
        },
        jumpDetail:function(id) {
            saveSession("toIndex",true);
            saveSession("tabIndex", 0);
            //跳转详情页面
            window.open("/detail/" + id+'.html', "_blank");
        },
        logout:function() {
            logout();
        },
    }
});
function toPage(pageNum){
    console.log(pageNum);
            if (pageNum < 0 || pageNum >= app.result.totalPage) {
                return;
            }
            app.result.search.pageNum = pageNum;
            pageLostFound(app.result.search, app.result, false);
}
$(function () {
    //console.log('index');
    //console.log(app.user);
    pageLostFound(app.result.search, app.result, false);

    let menuLeft = document.getElementById('cbp-spmenu-s1'),
        showLeftPush = document.getElementById('showLeftPush'),
        body = document.body;

    showLeftPush.onclick = function () {
        //console.log('close');
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

//冻结用户
function freezeUser(userId, flag) {
    $.ajax({
        url: baseUrl + "/users/freeze/" + userId,
        method: "GET",
        success: function (res) {
                if (res.success) {
                    showOK("操作成功！")
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//查询用户信息
function getUserInfo(userId, app) {
    $.ajax({
        url: baseUrl + "/users/info/" + userId,
        method: "GET",
        success: function (res) {
            console.log(res);
                if (res.success) {
                    app.userInfo = res.data.user;
                    //$("#infoDiv").show(1000);
                    //页面层
                    layer.open({
                        type: 1,
                        skin: 'layui-layer-rim', //加上边框
                        area: ['400px', 'auto'], //宽高
                        content: $("#infoDiv")
                    });
                    //$("#infoDiv").hide();
                    //console.log(app.userInfo);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//删除招领信息
function deletePub(id) {
    $.ajax({
        url: baseUrl + "/lostfounds/delete/" + id,
        method: "DELETE",
        success: function (res) {
                if (res.success) {
                    showOK(res.msg);
                    pageLostFound(app.result.search, app.result, false);
                } else {
                    showAlertError(res.msg)
                }
        }
    });

}

//分页查寻启事列表
function pageLostFound(data, result, append) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/lostfounds/page",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
                if (res.success) {
                    result.search.pageNum = res.data.page.pageNum;
                    result.search.pageSize = res.data.page.pageSize;
                    result.totalPage = res.data.page.totalPage;
                    result.total = res.data.page.total;
                    if (append) {
                        for (let v in res.data.page.list) {
                            //console.log(v);
                            result.list.push(res.data.page.list[v]);
                        }
                    } else {
                        result.list = res.data.page.list;
                    }
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}