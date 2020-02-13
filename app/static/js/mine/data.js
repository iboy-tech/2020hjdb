var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        schoolIcon: './go/icon-school.png',
        user: getSession("user") ? JSON.parse(getSession('user')) : {},
        lost:[1,20],
        found:[2,10],
        solve:[10,100],
        //数据总览
        //今日和总计
        /**
        item:{
        //近期数据
        labels1: ["01/10", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
        //柱状图
        data1: [[1, 70, 55, 20, 45, 0, 60], [65, 59, 90, 81, 56, 0, 40], [65, 1, 90, 81, 56, 1, 1]],
        labels2: ["Jan", "Feb", "March", "April", "May", "June", "July"],
        data2: [[22, 31, 2, 40, 555, 65, 68], [1, 31, 2, 40, 55, 0, 68], [1, 1, 39, 1, 55, 65, 68]],
         //饼状图
        //拾取，丢失，找到
        data3: [10, 20, 88],
        //用户数量变化图
        labels4: ["11/13", "04/14", "04/15", "04/17", "04/17", "04/18", "04/13"],
        data4: [1, 31, 39, 100, 55, 65, 1],
        //用户活跃量
        lables5: ["Jan", "Feb", "March", "April", "May", "June", "July"],
        data5: [[22, 31, 39, 40, 55, 65, 68], [12, 15, 23, 34, 36, 44, 51]],
        //性别比例
        data6: [10000,10000]
        }
         */
    },
    methods: {
        logout() {
            //询问框
            layer.confirm('确定要退出码？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteSession("user");
                window.location.replace("/logout");
            }, function () {
            });
        },
    }
});
$(function () {
    //console.log('index');
    //console.log(app.user);
    var menuLeft = document.getElementById('cbp-spmenu-s1'),
        showLeftPush = document.getElementById('showLeftPush'),
        body = document.body;

    showLeftPush.onclick = function () {
        classie.toggle(this, 'active');
        classie.toggle(body, 'cbp-spmenu-push-toright');
        classie.toggle(menuLeft, 'cbp-spmenu-open');
        disableOther('showLeftPush');
        $("#bar1").css("width", "100%");
        $("#line1").css("width", "100%");
        $("#pie1").css("width", "100%");
        $("#line2").css("width", "100%");
        $("#line3").css("width", "100%");
        $("#pie2").css("width", "100%");
    };

    function disableOther(button) {
        if (button !== 'showLeftPush') {
            classie.toggle(showLeftPush, 'disabled');
        }
    }
});
