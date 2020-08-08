var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        categoryList: [],
        category: {
            name: "",
            about: ""
        }
    },
    methods: {
        deleteCategory:function(name) {
            //询问框
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deleteCategory(name);
            }, function () {

            });

        },
        showAbout:function(index){
            showInfo(this.categoryList[index].about || this.categoryList[index].name);
        },
        submit:function() {
            addCategory(this.category, this);
        },
        logout:function() {
            logout();
        }
    }
});
//删除类别
function deleteCategory(categoryId) {
    $.ajax({
        url: baseUrl + "/categories/" +categoryId,
        method: "DELETE",
        success: function (res) {
                if (res.success) {
                    showOK(res.msg);
                    getCategory();
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//新增类别
function addCategory(data, app) {
    $.ajax({
        url: baseUrl + "/categories",
        method: "POST",
        data: JSON.stringify(data),
        success: function (res) {
                if (res.success) {
                    showOK(res.msg)
                    app.category = {
                        name: "",
                        about: ""
                    }
                    getCategory();
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//获取物品类别list
function getCategory() {
    $.ajax({
        url: baseUrl + "/categories",
        method: "GET",
        success: function (res) {
                if (res.success) {
                    app.categoryList = res.data.list
                } else {
                    showAlertError(res.msg)
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