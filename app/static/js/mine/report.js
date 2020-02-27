/**
 @File    : report.py
 @Time    : 2020/2/27 15:57
 @Author  : iBoy
 @Email   : iboy@iboy.tech
 @Description : 报表导出
 @Software: PyCharm
 */
var app = new Vue({
    el: '#day',
    data: {
        api:"https://view.officeapps.live.com/op/view.aspx?src=",
        user: getSession("user") ? JSON.parse(getSession('user')) : {},
        time: moment(new Date()).format("YYYY-MM-DD"),
        startTime: moment(new Date()).format("YYYY-MM-DD"),
        endTime: moment(new Date()).format("YYYY-MM-DD"),
        choice: [{id: "1", name: "失物报表"}, {id: "2", name: "招领报表"}],
        condition: {
            start: "2020-02-27",
            end: "2020-02-28",
            type: 1
        },
        result: {
            list: []
        }
    },
    methods: {
        execute() {
            this.condition.start=this.startTime,
            this.condition.end=this.endTime,

            addFile(app,app.condition)
        },
        logout() {
            //询问框
            layer.confirm('确定要退出吗？', {
                    btn: ['确定', '取消'] //按钮
                }, function () {
                    // deleteSession("user");
                    // window.location.replace("/logout");
                    $.ajax({
                        url: baseUrl + "/logout",
                        //data: JSON.stringify(data),
                        method: "POST",
                        success: function (res) {
                            if (res.success) {
                                console.log(res);
                                window.location = baseUrl + '/login';
                            }
                        }
                    });
                }, function () {
                }
            );
        },
        confrim: function (startTime, endTime) {
            console.log(startTime);
            console.log(endTime);
        }
    }
});
$(function () {
    getFile();
});

function getFile(app,append) {
    $.ajax({
        url: baseUrl + "/report.html/getall",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            if (res.success) {
                if (append) {
                    for (let v in res.data.list) {
                        //console.log(v);
                        app.result.list.push(res.data.list[v]);
                    }
                } else {
                    app.result.list = res.data.list;
                }
            } else {
                showAlertError(res.msg)
            }
        }
    });
}
function addFile(app,data) {
        $.ajax({
        url: baseUrl + "/report.html/add",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            // alert('我是userlist'+res)
            if (res.success) {
                showOK(res.msg);
                getFile(app,);
            } else {
                showAlertError(res.msg)
            }
        }
    });
}