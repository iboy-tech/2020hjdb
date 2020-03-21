var app = new Vue({
    el: "#app",
    created() {
        console.log("appcreated()方法");
    },
    data: {
        showMenu: false,
        tabIndex: 0,
        isSearched: getSession("isSearched") ? JSON.parse(getSession("isSearched")) : false,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
        category: getCategory() || [],
        userIcon: "https://ae01.alicdn.com/kf/H26181ae0390643b6850ad4c46341f8bcV.png",
        api: 'https://api.uomg.com/api/qq.talk?qq=',
        imgPrefix: staticUrl,
        tab: [
            {//主页
                search: {//tab0
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": "",
                    "pageNum": 0,
                    "pageSize": 8
                },
                totalPage: 0,
                total: 0,
                list: []
            },
            {//搜索
                search: {//tab1
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": "",
                    "pageNum": 0,
                    "pageSize": 30,
                    "isSearch": "",
                },
                totalPage: 0,
                total: 0,
                list: []
            },
            {//我的
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
            {},//消息
        ],
        tab3: [],
        imgTotal: 3,//最多3张图片
        tab4: {
            applyKind: 0,
            categoryIndex: -1,
            categoryId: 13,
            title: "",
            about: "",
            location: "",
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
            console.log(index);
            if (index != 1) {
                app.isSearched = false;
            }
            app.tabIndex = index;
            saveSession("tabIndex", index);
            console.log("删除缓存");
            deleteSession("data");
            console.log("搜索状态置空");
            saveSession("isSearched", false);
            console.log("--------------------------------------------");
            console.log("我是 changeTab(index)");
            console.log("getSession", getSession("scroll"));
            console.log("getLocal(isBack)", getLocal("isBack"));
            console.log("getSession(isSearched)", getSession("isSearched"));
            console.log("getSession(tabIndex)", getSession("tabIndex"));
            console.log("getSession(data)", getSession("data"));
            console.log("--------------------------------------------");
            if (index == 0) {//主页
                console.log(app.tab[0].list.length)
                app.nextPage(0);
                // pageLostFound(app.tab[0].search, app.tab[0], true);
            } else if (index == 1) {//搜索
                console.log(app.tab[1].list.length)
            } else if (index == 2) {//我发布的
                console.log(app.tab[2].list.length)
                console.log(this.tab[2].search.username);
                pageLostFound(this.tab[2].search, this.tab[2], true);
            } else if (index == 3) {//我的消息
                getMessages(this);
            } else if (index == 4) {
            } else if (index == 5) {
                // 常见问题
            } else if (index == 6) {
                // 关于我们
            }
        },
        search() {
            //用户开始搜索
            app.isSearched = true;
            saveSession("isSearched", true);
            saveSession("keyword", this.tab[1].search['keyword']);
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
            console.log("当前tabIndex",tabIndex)
            if (tabIndex == 0 || tabIndex == 2) {//这有主页，和我的需要无限滚动
                pageLostFound(app.tab[tabIndex].search, app.tab[tabIndex], true);
                app.tab[tabIndex].search.pageNum++;
                console.log("当前的页数app.tab[tabIndex].search.pageNum",app.tab[tabIndex].search.pageNum);
            }
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
            if (this.tab4.title == "") {
                showAlertError('请输入标题!');
                return;
            }
            if (this.tab4.about == "") {
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
                console.log("删除缓存");
                deleteSession("data");
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
            saveLocal("isBack", true);
            // 记住当前数据
            saveSession("pageNum",app.tab[app.tabIndex].search.pageNum);
            saveSession("data", app.tab[app.tabIndex].list);
            if (app.tabIndex == 0) {
                saveSession("category", app.tab[0].search.category);
                saveSession("kind", app.tab[0].search.kind)
            }
            //记住当前位置
            saveSession("scroll", $(window).scrollTop());
            saveSession("tabIndex", app.tabIndex);
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
                    if (app.feedback.subject == "" || app.feedback.content == "") {
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
                title: "修改密码", //不显示标题
                content: $('#pwdDiv'),  //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                yes: function () {
                    console.log(app.password);
                    let pwd = app.password;
                    var reg = /^[a-zA-Z0-9]{6,15}$/;
                    if (pwd.newPassword == '' || pwd.newPassword.length < 6) {
                        showAlertError('密码至少是6位');
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
        },
        titleAlert(title) {
            console.log(title);
            alert(title)
        },
    },
    mounted() {
        // console.log("我是监控的mounted", app.tabIndex);
        var io = new IntersectionObserver((entries) => {
            console.log("我是监控的mounted", app.tabIndex);
            if (app.tabIndex == 1) {
                let mysearch = getSession("isSearched");
                if (mysearch != "false") {
                    saveSession("isSearched", true);
                    // app.nextPage(app.tabIndex);
                    // 搜索页面没有滚动加载
                }
            } else if (app.tabIndex == 0 || app.tabIndex == 2) {
                 console.log("需要请求下一页", getSession("tabIndex"));
                 app.nextPage(app.tabIndex);
            }
            console.log("--------------------------------------------");
            console.log("我是mouted()");
            console.log("getSession", getSession("scroll"));
            console.log("getLocal(isBack)", getLocal("isBack"));
            console.log("getSession(isSearched)", getSession("isSearched"));
            console.log("getSession(tabIndex)", getSession("tabIndex"));
            console.log("getSession(data)", getSession("data"));
            console.log("--------------------------------------------");
            // 存储数据，还没去详情页
            if (getLocal("isBack") == null) {
                console.log($(window).scrollTop());
                // var scroll_top=$(window).scrollTop()
                mylist = JSON.parse(getSession("data"))
                console.log(mylist, typeof (mylist));
            }
        });
        // this.$nextTick(() => {
            io.observe(document.getElementById('flag'));
            /* code */
        // });

    },

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
                    saveLocal("user", app.user);
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
                    showOK(res.msg);
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
                            deleteLocal("user");
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
        success: function (res) {
            console.log(res);
            if (res.success) {
                showOK(res.msg);
                // saveSession("category", "");
                // saveSession("kind", -1);
                saveSession("tabIndex", 2);
                // saveLocal("isBack",false);
                // location.reload();
                pageLostFound(app.tab[2].search, app.tab[2], false);
            } else {
                showAlertError(res.msg)
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
                    saveLocal("user", app.user);
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

    if (size > 400) {
        showAlertError('图片大小超过400KB，请将拍摄的图片进行屏幕截图并裁剪多余部分之后重新上传');
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
                    console.log("删除缓存");
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
                    showOK("发布成功！");
                    saveSession("category", "");
                    saveSession("kind", -1);
                    saveSession("tabIndex", 0);
                    app.tab4 = {
                        applyKind: 0,
                        categoryIndex: -1,
                        categoryId: 13,
                        title: "",
                        about: "",
                        location: null,
                        images: [],//srcList
                    };
                    location.reload();
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
        success: function (res) {
            console.log(res);
                if (res.success) {

                    // result.search.pageNum = res.data.page.pageNum;
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

$(function () {
    getNoticeList(app);
    //从详情页返回
    if (getLocal("isBack") == "true") {
        app.tabIndex = JSON.parse(getSession("tabIndex"));
        console.log("我是现在的tab", app.tabIndex);
        if (app.tabIndex == 1) {
            //搜索的关键字
            app.tab[app.tabIndex].search["keyword"] = getSession("keyword");
            deleteSession("keyword");
        }
        if (app.tabIndex == 0) {
            //主页的搜索数据
            app.tab[0].search.pageNum=JSON.parse(getSession("pageNum"));
            app.tab[0].search.category = getSession("category");
            app.tab[0].search.kind = JSON.parse(getSession("kind"));
        }
        if(app.tabIndex==2){
            app.tab[2].search.pageNum=JSON.parse(getSession("pageNum"));
        }
        app.tab[app.tabIndex].list = JSON.parse(getSession("data"));
        $("html,body").scrollTop(JSON.parse(getSession("scroll")))
        deleteLocal("isBack");
        deleteSession("data");
        // app.notice=JSON.parse(getSession("notice"));
    } else {
        if ((app.tabIndex == 0 || app.tabIndex == 2 )) {
            console.log("我是正常加载，不进入详情",getLocal("isBack"));
            // app.nextPage(app.tabIndex);
            // pageLostFound(app.tab[app.tabIndex].search, app.tab[app.tabIndex], true);
        }
        else if(app.tabIndex == 3){
             getMessages(app);
        }
        // saveSession("notice",getNoticeList(app)["data"]["list"]);
    }
    console.log("--------------------------------------------");
    console.log("我一定是最先加载的");
    console.log("getSession", getSession("scroll"));
    console.log("getLocal(isBack)", getLocal("isBack"));
    console.log("getSession(isSearched)", getSession("isSearched"));
    console.log("getSession(tabIndex)", getSession("tabIndex"));
    console.log("getSession(data)", getSession("data"));
    console.log("getSession(category)", getSession("category"));
    console.log("getSession(kind)", getSession("kind"));
    console.log("--------------------------------------------");
    let sessionIndex = getSession("tabIndex");
    if (sessionIndex != null) {
        app.tabIndex = JSON.parse(sessionIndex);
    } else {
        console.log("saveSession丢失了$(function () ");
        saveSession("tabIndex", 0);
        app.tabIndex = 0;
    }
});
$('.ui.radio.checkbox')
    .checkbox()
;
$('select.dropdown')
    .dropdown()
;

