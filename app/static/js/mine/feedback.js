var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        list: [],
        reply: {
            id: "",
            content: ""
        }
    },
    methods: {
        showReply:function(id) {
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['52vw', 'auto'],
                //shade: true,
                title: "回复", //不显示标题
                content: $('#replyDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                , yes: function () {
                    app.reply.id = id;
                    replyFeedback(app.reply, app);
                }, cancel: function () {

                }
            });
        },
        markFeedback:function(id) {
            markFeedback(id);
        },
        deleteFeedback:function(id) {
            //询问框
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteFeedback(id);
            }, function () {

            });

        },
        logout:function() {
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
        url: baseUrl + "/feedbacks/" + id,
        method: "DELETE",
        success: function (res) {
                if (res.success) {
                    showOK(res.msg);
                    getFeedbackList(app);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//标记已读反馈
function markFeedback(id) {
    $.ajax({
        url: baseUrl + "/feedbacks/" + id,
        method: "PUT",
        success: function (res) {
                if (res.success) {
                    showOK(res.msg);
                    getFeedbackList(app);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}


//回复反馈
function replyFeedback(data, app) {
    $.ajax({
        url: baseUrl + "/feedbacks/reply",
        method: "POST",
        data: JSON.stringify(data),
        success: function (res) {
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    app.reply.content = "";
                    app.reply.id = "";
                    getFeedbackList(app);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//查询反馈列表
function getFeedbackList(app) {
    $.ajax({
        url: baseUrl + "/feedbacks",
        //data: JSON.stringify(data),
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