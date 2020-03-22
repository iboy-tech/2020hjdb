var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        schoolIcon: './go/icon-school.png',
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
        freezeUser(userId, flag) {
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
        seeInfo(userId) {
            console.log(userId);
            getUserInfo(userId, this);
        },
        checkAll() {
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
        deleteAll() {
            let data=this.checkedList;
            layer.confirm('你确定要批量删除 '+data.length+' 条数据吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                $.ajax({
                    url: baseUrl + "/found.html/deleteAll",
                    method: "POST",
                    data: JSON.stringify(data),
                    success: function (res) {
                        console.log(res);
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
        submit() {
            let pgNum = $('#pgNum').val() - 1;
            this.result.search.pageNum = pgNum < 0 ? 0 : pgNum;
            pageLostFound(app.result.search, app.result, false);
        },
        deletePub(id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deletePub(id);
            }, function () {
            });

        },
        changePage(e) {
            console.log(e);
        },
        toPage(pageNum) {
            toPage(pageNum);
        },
        jumpDetail(id) {
            saveSession("toIndex",true);
            saveSession("tabIndex", 0);
            //跳转详情页面
            window.open("./detail.html?id=" + id, "_blank");
        },
        logout() {
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
        url: baseUrl + "/userlist.html/freeze?userId=" + userId,
        method: "POST",
        //data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK("操作成功！")
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

//查询用户信息
function getUserInfo(userId, app) {
    $.ajax({
        url: baseUrl + "/userlist.html/userInfo?userId=" + userId,
        method: "POST",
        //data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
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
            } else {
                console.log(res);
                showAlertError(res)
            }
        }
    });
}

//删除招领信息
function deletePub(id) {
    $.ajax({
        url: baseUrl + "/found.html/delete?id=" + id,
        method: "POST",
        // data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK(res.msg);
                    pageLostFound(app.result.search, app.result, false);
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

//分页查寻启事列表
function pageLostFound(data, result, append) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/found.html/getall",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
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
            } else {
                console.log(res);
                showAlertError(res)
            }
        }
    });
}