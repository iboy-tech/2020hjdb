var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        schoolIcon: './go/icon-school.png',
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        notice: {
            title: "",
            content: "",
            fixTop: false,
            pusher: false,//是否微信群发推送
        },
        list: []
    },
    methods: {
        showAdd:function() {
            //捕获页
            layer.open({
                type: 1,
                title: false,
                skin: 'layui-layer-rim', //加上边框
                area: ['auto', 'auto'], //宽高
                content: $('#addDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
            });
        },
        submit:function() {
            if (app.notice.pusher) {
                layer.confirm('微信群发用来发送重要通知，仅超级管理员可用，你确定要群发吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    addNotice(app.notice);
                }, function () {
                });
            } else {
                addNotice(app.notice);
            }

        },
        switchFix:function(id, index) {
            let ask;
            if (this.list[index].fixTop == 1) {
                ask = "确定要取消置顶吗？";
            } else {
                ask = "确定要设置为置顶吗？";
            }
            layer.confirm(ask, {
                btn: ['确定', '取消'] //按钮
            }, function () {
                switchFix(id);
            }, function () {

            });
        },
        deleteNotice:function(id) {
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteNotice(id);
            }, function () {

            });
        },
        logout:function() {
            logout();
        },
    }
});

function switchFix(id) {
    $.ajax({
        url: baseUrl + "/notices/" + id,
        //data: JSON.stringify(data),
        method: "PUT",
        success: function (res) {
                if (res.success) {
                    showOK();
                    getNoticeList(app);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//删除通知
function deleteNotice(id) {
    $.ajax({
        url: baseUrl + "/notices/" + id,
        //data: JSON.stringify(data),
        method: "DELETE",
        success: function (res) {
                if (res.success) {
                    showOK();
                    getNoticeList(app);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//新增通知
function addNotice(notice) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/notices",
        method: "POST",
        data: JSON.stringify(notice),
        success: function (res) {
            if (res.success) {
                showOK(res.msg);
                layer.closeAll(); //疯狂模式，关闭所有层
                app.notice = {
                    title: "",
                    content: "",
                    fixTop: false,
                    pusher: false,
                };
                getNoticeList(app);
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

//查询通知列表
function getNoticeList(app) {
    $.ajax({
        url: baseUrl + "/notices",
        method: "GET",
        success: function (res) {
                if (res.success) {
                    app.list = res.data.list;
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

$(function () {
    getNoticeList(app);

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