var app = new Vue({
    el: "#app",
    data: {
        showMenu: false,
        tabIndex: 0,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        category: getCategory() || [],
        userIcon: "http://localhost/static/icon/user_icon.png",
        api: 'https://api.uomg.com/api/qq.talk?qq=',
        imgPrefix: staticUrl,
        tab: [
            {
                search: {//tab0
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": "",
                    "pageNum": 0,
                    "pageSize": 10
                },
                totalPage: 0,
                total: 0,
                list: []
            },
            {
                search: {//tab1
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": "",
                    "pageNum": 0,
                    "pageSize": 15
                },
                totalPage: 0,
                total: 0,
                list: []
            },
            {
                search: {//tab2
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": (getLocal("user") ? JSON.parse(getLocal("user")) : {}).studentNum,
                    "pageNum": 0,
                    "pageSize": 15
                },
                totalPage: 0,
                total: 0,
                list: [],
            },
            {},
        ],
        tab3: [],
        imgTotal: 3,//最多3张图片
        tab4: {
            applyKind: 0,
            categoryIndex: -1,
            categoryId: 13,
            title: " ",
            about: " ",
            location: " ",
            images: [],//srcList
            info: ""
        },
        notice: [
            {
                id: "1",
                title: "使用须知（必看）",
                content: "本程序使用时会采集部分个人信息，所私密信息都加密处理，请放心使用!",
                time: "2020-01-23 18:45",
                fixTop: 1,
            }
        ],
        noticeAll: false,
        feedback: {
            subject: "",
            content: "",
        },
        icon: "https://ae01.alicdn.com/kf/U89b7be7d8d234a38b9a4b0d4258de362X.jpg",
        password: {
            oldPassword: "",
            newPassword: "",
            confirmPassword: ""
        }
    },
    methods: {
        share() {
            //捕获页
            layer.open({
                type: 1,
                //shade: true,
                title: "<h4>微信扫一扫分享</h4>", //不显示标题
                content: $('#shareDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
            });
        },
        showAllNotice(b) {
            this.noticeAll = b;
        },
        seeNotice(index) {
            let t = app.notice[index];
            layer.open({
                title: t.time + "  " + t.title || "",
                content: t.content || ""
            });

        },
        changeTab(index) {
            //console.log(index);
            this.tabIndex = index;
            if (index == 0) {
                pageLostFound(app.tab[0].search, app.tab[0], true);
            } else if (index == 1) {

            } else if (index == 2) {
                console.log(this.tab[2].search.username);
                pageLostFound(this.tab[2].search, this.tab[2], false);
            } else if (index == 3) {//我的消息
                getMessages(this);
            } else if (index == 4) {
            }
        },
        search() {
            this.tab[1].search.pageNum = 0;
            this.tab[1].totalPage = 0;
            this.tab[1].total = 0;
            pageLostFound(this.tab[1].search, this.tab[1], false);
        },
        changeTab0Kind(index) {
            this.tab[0].search.pageNum = 0;
            // this.tab[0].list = [];
            this.tab[0].search.kind = index;
            pageLostFound(this.tab[0].search, this.tab[0], false);
            console.log(this.tab[0].search, this.tab[0]);
        },
        changeTab0Category(index) {
            this.tab[0].search.pageNum = 0;
            // this.tab[0].list = [];
            if (index < 0) {
                this.tab[0].search.category = "";
            } else {
                this.tab[0].search.category = this.category[index].name;
            }
            pageLostFound(this.tab[0].search, this.tab[0], false);
            console.log(this.tab[0].search, this.tab[0]);
        },
        nextPage(tabIndex) {
            this.tab[tabIndex].search.pageNum++;
            pageLostFound(app.tab[0].search, app.tab[0], true);
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
        logout() {
            logout();
        },
        removeComment(id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                removeComment(id);
                layer.close();
            }, function () {
            });
        },
        changeTab4EventKind(index) {
            console.log(index);
            this.tab4.applyKind = index;
        },
        changeTab4CategoryIndex(index) {
            this.tab4.categoryIndex = index;
        },
        submitPub() {

            if (this.tab4.categoryIndex < 0) {
                showAlertError("请选择物品类别！")
                return;
            }
            if (this.tab4.title == " ") {
                showAlertError('请输入标题!');
                return;
            }
            if (this.tab4.about == " ") {
                showAlertError('请输入详情!');
                return;
            }
            let data = this.tab4;
            if (this.tab4.applyKind == 1) {
                let temp = this.category[data.categoryIndex < 0 ? 0 : data.categoryIndex]
                data.categoryId = temp.categoryId;
                if (this.tab4.info == "") {
                    var regName = /(身份证)$/;
                    var regNum = /(校园卡|学生证)$/;
                    if (regName.test(temp.name)) {
                        showAlertError("分类 " + temp.name + " 需要在附加信息中填入姓名");
                        return;
                    } else if (regNum.test(temp.name)) {
                        showAlertError("分类 " + temp.name + " 需要在附加信息中填入学号");
                        return;
                    }
                } else {
                    var reg1 = /^\d+$/;
                    var reg2 = /^[\u4E00-\u9FA5\uf900-\ufa2d·s]{2,20}$/;
                    if (reg1.test(this.tab4.info)) {
                    } else if (reg2.test(this.tab4.info)) {

                    } else {
                        showAlertError("附加信息只填写学号或姓名中的一项,请不要同时填写,如有学号，请优先填写学号");
                        return;
                    }
                }
            } else {
                let temp = this.category[data.categoryIndex < 0 ? 0 : data.categoryIndex]
                data.categoryId = temp.categoryId;
            }
            if (this.tab4.images.length != 0) {
                layer.confirm('检测到您上传有图片,如有隐私信息请注意打码哦！', {
                    btn: ['已打码', '取消'] //按钮
                }, function () {
                    pubLostFound(data);
                    $("button[type='submit']").attr('disabled', 'disabled');
                }, function () {
                });
            } else {
                pubLostFound(data);
                $("button[type='submit']").attr('disabled', 'disabled');
            }
            console.log(data);
            //console.log(this.tab4);
        },
        changeImg() {
            console.log('change div');
            $("#imgInput").click();//模拟点击
        },
        removeImg(index) {
            console.log('remove img' + index);
            this.tab4.images.splice(index, 1);
        },
        jumpDetail(id) {
            //跳转详情页面
            window.open(baseUrl + "/detail.html?id=" + id, "_self");
        },
        showFeedback() {
            app.showMenu = false;
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['50vw', 'auto'],
                //shade: true,
                title: "反馈", //不显示标题
                content: $('#editorDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                , yes: function () {
                    console.log(app.feedback);
                    if (app.feedback.subject == " " || app.feedback.content == " ") {
                        showAlertError('请填写全部内容!');
                        return;
                    }
                    pubFeedback(app.feedback);
                }, cancel: function () {

                }
            });
        },
        setPassword() {
            app.showMenu = false;
            layer.open({
                btn: ['确定'],
                type: 1,
                area: ['300px', 'auto'],
                //shade: true,
                title: "修改密吗", //不显示标题
                content: $('#pwdDiv'),  //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                yes: function () {
                    console.log(app.password);
                    let pwd = app.password;
                    var reg = /^[a-zA-Z0-9]{6,15}$/;
                    if (pwd.newPassword == '' || pwd.newPassword.length < 6) {
                        showAlertError('密吗至少是6位');
                        return false;
                    } else if (!reg.test(app.newPassword)) {
                        showAlertError('密码必须包为字母或数字！');
                        return false;
                    } else if (pwd.newPassword != pwd.confirmPassword) {
                        showAlertError("两次密码不一致！");
                        return;
                    }
                    setPassword(app.password);
                },
                cancel: function () {
                    app.password = {
                        oldPassword: "",
                        newPassword: "",
                        confirmPassword: ""
                    }
                }
            });
        },
        setQQ() {
            app.showMenu = false;
            layer.prompt({title: '请输入新的QQ：'}, function (qq, index) {
                if (qq == '') {
                    showAlertError('QQ号不可为空！');
                    return false;
                } else {
                    var reg = /^[1-9][0-9]{4,14}$/;
                    ;
                    if (!reg.test(qq)) {
                        showAlertError('QQ号格式错误！');
                        return false;
                    }
                }
                //layer.close(index);
                setQQ(qq);
            });
        },
        setIcon() {
            app.showMenu = false;
            $("#iconInput").click();
        },
        showAbout() {
            app.showMenu = false;
            showAlert("CTGU失物招领系统", "关于");
        }
    }
});

$(function () {
    pageLostFound(app.tab[0].search, app.tab[0], true);
    getNoticeList(app);
});


//设置QQ号
function setQQ(qq) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/user.html/setQQ?qq=" + qq,
        //data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    app.user.QQ = res.data.qq;
                    saveSession("user", app.user);
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

//新增反馈
function pubFeedback(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/feedback.html/add",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    layer.closeAll();
                    showOK();
                    app.feedback = {
                        subject: "",
                        content: ""
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

//修改密码
function setPassword(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/user.html/setPassword",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);

            if (res.success) {
                layer.closeAll();
                showOK();
                app.password = {
                    oldPassword: "",
                    newPassword: "",
                    confirmPassword: ""
                }
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
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

//删除招领信息
function deletePub(id) {
    $.ajax({
        url: baseUrl + "/found.html/delete?id=" + id,
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK(res.msg);
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

//查询通知列表
function getNoticeList(app) {
    $.ajax({
        url: baseUrl + "/notice.html/getall",
        //data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            // showAlertError(res)
            // alert(status)
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    app.notice = res.data.list;
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

//删除消息（评论）
function removeComment(id) {
    console.log("我是要删除的ID:" + id);
    $.ajax({
        url: baseUrl + "/comment/delete?id=" + id,
        method: "POST",
        success: function (res) {
            console.log(res);
            if (res.success) {
                showOK(res.msg);
                getMessages(app);
            } else {
                showAlertError(res.msg)
            }
        }
    });

}

//我的消息(与我发布的信息相关的评论）
function getMessages(app) {
    $.ajax({
        url: baseUrl + "/user.html/messages",
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    app.tab3 = res.data.list;
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


function setIcon(icon) {
    $.ajax({
        url: baseUrl + "/user.html/setIcon",
        data: {icon: icon},
        contentType: "application/x-www-form-urlencoded",
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    layer.closeAll();
                    showOK();
                    app.user.icon = res.data.icon;
                    saveSession("user", app.user);
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

//选择上传图片
function changeInput(obj) {
    console.log('change img')
    console.log(obj);
    let file = obj.files[0];

    //console.log(file);
    console.log("file.size = " + file.size);  //file.size 单位为byte
    var size = file.size / 1024;

    if (size > 2000) {
        showAlertError('您上传的图片大小超过2M，请尝试压缩图片，或上传所拍照片的截图');
        return;
    }

    let reader = new FileReader();

    reader.onload = function (e) {
        app.tab4.images.push(e.target.result);
    }

    reader.readAsDataURL(file)
}

//发布启事
function pubLostFound(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/user.html/pub",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK("发布成功！");
                    app.tab4 = {
                        applyKind: 0,
                        categoryIndex: -1,
                        title: "",
                        about: "",
                        location: null,
                        images: [],//srcList
                    };
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

//发布启事
function pubLostFound(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/found.html/pub",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    // showOK("发布成功！");
                    app.tab4 = {
                        applyKind: 0,
                        categoryIndex: -1,
                        categoryId: 13,
                        title: "",
                        about: "",
                        location: null,
                        images: [],//srcList
                    };
                    window.location.href = baseUrl
                    // changeTab(0);
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

//获取物品类别list
function getCategory() {
    $.ajax({
        url: baseUrl + "/category.html/getall",
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    app.category = res.data.list
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

$('.ui.radio.checkbox')
    .checkbox()
;
$('select.dropdown')
    .dropdown()
;
//滚动到底部触发事件
// $(window).scroll(function(){
//     var scrollTop = $(this).scrollTop();
//     var scrollHeight = $(document).height();
//     var windowHeight = $(this).height();
//     if(scrollTop + windowHeight == scrollHeight){
//         alert("you are in the bottom");
//     }
// });

$(function () {
    let id = getUrlParam("id");
    if (!id) {
        // showAlertError("缺少请求参数！");
    } else {
        getDetail(id, app);
    }
    // var qrcode = new QRCode(document.getElementById("imgDiv"), location.href);
});


