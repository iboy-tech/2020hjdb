/**
 @File    : report.py
 @Time    : 2020/2/27 15:57
 @Author  : iBoy
 @Email   : iboy@iboy.tech
 @Description : 报表导出
 @Software: PyCharm
 */
var app = new Vue({
    el: '#app',
    data: {
        path: window.location.protocol + "//" + window.location.host + "/static/file/",
        api: "https://view.officeapps.live.com/op/view.aspx?src=",
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        time: moment(new Date()).format("YYYY-MM-DD"),
        startTime: moment(new Date()).format("YYYY-MM-DD"),
        endTime: moment(new Date()).format("YYYY-MM-DD"),
        choice: [{value: "1", name: "失物登记表"}, {value: "2", name: "失物统计表"}],
        flag: -1,
        condition: {
            start: "2020-02-27",
            end: "2020-02-28",
            type: 1
        },
        list: []
    },
    methods: {
        execute:function() {
            this.condition.start = this.startTime;
            this.condition.end = this.endTime;
            this.condition.type = this.flag;
            if (this.flag == -1) {
                showInfo("请选择报表类型");
                return;
            } else {
                addFile(app, app.condition);
            }
        },
        logout:function() {
            logout();
        },
        deleteFile: function (id) {
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                            $.ajax({
                url: "/reports/"+id,
                method: "DELETE",
                success: function (res) {
                    if (res.success) {
                        showOK(res.msg);
                        getFile(app,false);
                    }
                    else {
                        showError(res.msg)
                    }

                }
            });
            }, function () {
            });
        },
        confrim: function (startTime, endTime) {
            console.log(startTime);
            console.log(endTime);
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

    getFile(app, false);
});

function getFile(app, append) {
    $.ajax({
        url: baseUrl + "/reports",
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

function addFile(app, data) {
    $.ajax({
        url: baseUrl + "/reports",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                showOK(res.msg);
                getFile(app, false);
            } else {
                showAlertError(res.msg)
            }
        }
    });
}