var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        schoolIcon: './go/icon-school.png',
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        list: [],
        reply: {
            id: "",
            content: ""
        }
    },
    methods: {
        showReply(id) {
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['52vw', 'auto'],
                //shade: true,
                title: "回复", //不显示标题
                content: $('#replyDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                , yes: function () {
                    console.log(id);
                    app.reply.id = id;
                    replyFeedback(app.reply, app);
                }, cancel: function () {

                }
            });
        },
        markFeedback(id) {
            markFeedback(id);
        },
        deleteFeedback(id) {
            //询问框
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteFeedback(id);
            }, function () {

            });

        },
        logout() {
            logout();
        },
    }
});

$(function () {
    getFeedbackList(app);


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

//标记已读反馈
function deleteFeedback(id) {
    $.ajax({
        url: baseUrl + "/feedback.html/delete?id=" + id,
        method: "POST",
        //data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK("操作成功！");
                    getFeedbackList(app);
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

//标记已读反馈
function markFeedback(id) {
    $.ajax({
        url: baseUrl + "/feedback.html/mark?id=" + id,
        method: "POST",
        //data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK("操作成功！");
                    getFeedbackList(app);
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


//回复反馈
function replyFeedback(data, app) {
    $.ajax({
        url: baseUrl + "/feedback.html/reply",
        method: "POST",
        data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    layer.closeAll();
                    showOK("操作成功！");
                    app.reply.content = "";
                    app.reply.id = "";
                    getFeedbackList(app);
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

//查询反馈列表
function getFeedbackList(app) {
    $.ajax({
        url: baseUrl + "/feedback.html/getall",
        //data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    app.list = res.data.list;
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