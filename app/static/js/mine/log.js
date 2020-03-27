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
        delete(type) {
            layer.confirm('日志30天后自动删除,你需要手动清空吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                            $.ajax({
                url: "/log.html/delete?type="+type,
                method: "POST",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        getLogs(app, type,false);
                    } else {
                        showError(res.msg)
                    }
                }
            });
            }, function () {
            });
        },
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

});

function getLogs(app,type ,append) {
    $.ajax({
        url: baseUrl + "/log.html/getall?type="+type,
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