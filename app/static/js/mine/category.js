var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        schoolIcon: './go/icon-school.png',
        user: getSession("user") ? JSON.parse(getSession('user')) : {},
        categoryList: [],
        category: {
            name: "",
            about: ""
        }
    },
    methods: {
        deleteCategory(name) {
            console.log(name);
            //询问框
            layer.confirm('确定要删除码？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteCategory(name);
            }, function () {

            });

        },
        showAbout(index){
            showInfo(this.categoryList[index].about || this.categoryList[index].name);
        },
        submit() {
            console.log(this.category);
            addCategory(this.category, this);
        },
        logout() {
            //询问框
            layer.confirm('确定要退出吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                // deleteSession("user");
                // window.location.replace("/logout");
                    $.ajax({
        url: baseUrl + "/logout" ,
        //data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success){
                 console.log(res);
                window.location=baseUrl+'/login';
            }
        }
    });}, function () {

            });
        },
    }
});
//删除类别
function deleteCategory(name) {
    $.ajax({
        url: baseUrl + "/category.html/delete?name=" + name,
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK();
                    getCategory();
                } else {
                    showAlertError(res.msg)
                }
            } else {
                console.log(res);
                alert(res)
            }
        }
    });
}

//新增类别
function addCategory(data, app) {
    $.ajax({
        url: baseUrl + "/category.html/add",
        method: "POST",
        data: JSON.stringify(data),
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK("操作成功！")
                    app.category = {
                        name: "",
                        about: ""
                    }
                    getCategory();

                } else {
                    showAlertError(res.msg)
                }
            } else {
                console.log(res);
                alert(res)
            }
        }
    });
}

//获取物品类别list
function getCategory() {
    $.ajax({
        url: baseUrl + "/category.html/getall",
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    app.categoryList = res.data.list
                } else {
                    showAlertError(res.msg)
                }
            } else {
                console.log(res);
                alert(res)
            }
        }
    });
}

$(function () {
    getCategory();

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