var app = new Vue({
    el: "#app",
    created:function() {
        this.user=getLocal("user") ? JSON.parse(getLocal("user")) :{};
        if (getSession("tabIndex") == "3") {
            getMessages(this);
        }
        this.category=getCategory();
    },
    data: {
        showMenu: false,
        tabIndex: 0,
        isSearched: getSession("isSearched") ? JSON.parse(getSession("isSearched")) : false,
        user:  {},
        category: [],
        api: 'https://wpa.qq.com/msgrd?v=3&site=qq&menu=yes&uin=',
        imgPrefix: staticUrl,
        tab: [
            {//主页
                search: {//tab0
                    "kind": -1,
                    "category": "",
                    "keyword": "",
                    "username": "",
                    "pageNum": 0,
                    "pageSize": 5
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
                    "pageSize": 5
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
                title: "上线啦",
                content: "欢迎使用三峡大学失物招领平台",
                time: "2020-01-23 18:45",
                fixTop: 1,
            }
        ],
        noticeAll: false,
        feedback: {
            subject: "",
            content: "",
        },
        password: {
            oldPassword: "",
            newPassword: "",
            confirmPassword: ""
        },
        wxReward:getLocal("user") ? JSON.parse(getLocal("user")).wxReward : "",
    },
    methods: {
        showAllNotice:function(b) {
            this.noticeAll = b;
        },
        seeNotice:function(index) {
            let t = app.notice[index];
            layer.open({
                title: t.time + "  " + t.title || "",
                btn: ['收到'],
                content: t.content || ""
            });
        },
        changeTab:function(index) {
            console.log(index);
            if (index != 1) {
                app.isSearched = false;
            }
            app.tabIndex = index;
            saveSession("tabIndex", index);
            deleteSession("data");
            saveSession("isSearched", false);
            saveSession("pageNum", 0);
            if (index == 0) {//主页
                app.tab[0].list = [];
                app.tab[0].search.pageNum = 0;
                app.tab[0].search.category = "";
                app.tab[0].search.kind = -1
                app.nextPage(0, false);
            } else if (index == 1) {//搜索
            } else if (index == 2) {//我发布的
                app.tab[2].search.pageNum = 0;
                app.nextPage(2, false);
            } else if (index == 3) {//我的消息
                getMessages(this);
            } else if (index == 4) {
            } else if (index == 5) {
                app.showMenu = false;
                // 常见问题
            } else if (index == 6) {
                app.showMenu = false;
                // 关于我们
            }
        },
        search:function() {
            //用户开始搜索
            app.isSearched = true;
            saveSession("isSearched", true);
            saveSession("keyword", this.tab[1].search['keyword']);
            this.tab[1].search.pageNum = 0;
            this.tab[1].totalPage = 0;
            this.tab[1].total = 0;
            pageLostFound(this.tab[1].search, this.tab[1], false);
        },
        changeTab0Kind:function(index) {
            this.tab[0].search.pageNum = 0;
            this.tab[0].list = [];
            this.tab[0].search.kind = index;
            deleteSession("data");
            app.nextPage(0, false);
            console.log(this.tab[0].search, this.tab[0]);
        },
        changeTab0Category:function(index) {
            this.tab[0].search.pageNum = 0;
            deleteSession("data");
            this.tab[0].list = [];
            if (index < 0) {
                this.tab[0].search.category = "";
            } else {
                this.tab[0].search.category = this.category[index].name;
            }
            app.nextPage(0, false);
            console.log(this.tab[0].search, this.tab[0]);
        },
        nextPage:function(tabIndex, append) {
            console.log("当前tabIndex", tabIndex)
            if (tabIndex == 0 || tabIndex == 2) {//只有主页，和我的需要无限滚动
                pageLostFound(app.tab[tabIndex].search, app.tab[tabIndex], append);
                app.tab[tabIndex].search.pageNum++;
            }
        },

        deletePub:function(id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deletePub(id);
            }, function () {
            });
        },
        logout:function() {
            logout();
        },
        removeComment:function(id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                removeComment(id);
                layer.close();
            }, function () {
            });
        },
        changeTab4EventKind:function(index) {
            console.log(index);
            this.tab4.applyKind = index;
        },
        changeTab4CategoryIndex:function(index) {
            this.tab4.categoryIndex = index;
        },
        submitPub:function() {
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
                deleteSession("data");
                $("button[type='submit']").attr('disabled', 'disabled');
            }
            console.log(data);
            //console.log(this.tab4);
        },
        changeImg:function() {
            // console.log('change div');
            changeInput();
            $("#imgInput").click();//模拟点击
        },
        removeImg:function(index) {
            // console.log('remove img' + index);
            this.tab4.images.splice(index, 1);
        },
        jumpDetail:function(id) {
            //跳转详情页面
            saveLocal("isBack", true);
            // 记住当前数据
            saveSession("pageNum", app.tab[app.tabIndex].search.pageNum);
            saveSession("data", app.tab[app.tabIndex].list);
            saveSession("toIndex", false);
            saveSession("notice", app.notice);
            if (app.tabIndex == 0) {
                saveSession("category", app.tab[0].search.category);
                saveSession("kind", app.tab[0].search.kind)
            }
            //记住当前位置
            saveSession("scroll", $(window).scrollTop());
            saveSession("tabIndex", app.tabIndex);
            window.open(baseUrl + "/detail/" + id+".html", "_self");
        },
        showFeedback:function() {
            app.showMenu = false;
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['70%', 'auto'],
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
        setPassword:function() {
            app.showMenu = false;
            layer.open({
                btn: ['确定', '取消'],
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
        showRewardHelp:function(){
            layer.open({
                title:"收款码地址获取方法",
                content:"将微信收款码保存，然后用QQ扫描，将得到的地址复制粘贴到输入框内保存即可，地址示例[ wxp://f2f0Pihuc-hsXPKrjN4TIU27SSx-w6v2RAUv ]",
            });
        },
        setReward:function(){
            app.showMenu = false;
            layer.open({
                btn: ['保存'],
                type: 1,
                area: ['300px', 'auto'],
                //shade: true,
                title: "请填入您的微信收款码地址：", //不显示标题
                content: $('#rewardDiv'),  //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                yes: function () {
                    let tmp=app.wxReward;
                    app.wxReward = tmp.replace(/\s+/g,"");
                    let reg = /^wxp:\/\/[A-Za-z0-9\-]+/;
                    if (app.wxReward == '') {
                        showAlertError('内容不能为空');
                        return false;
                    } else if (!reg.test(app.wxReward)) {
                        showAlertError('收款码地址格式错误！');
                        return false;
                    }
                    setReward(app.wxReward);
                },
            });
        },
        setQQ:function() {
            app.showMenu = false;
            layer.prompt({title: '请输入新的QQ：'}, function (qq) {
                if (qq == '') {
                    showAlertError('QQ号不可为空！');
                    return false;
                } else {
                    let reg = /^[1-9][0-9]{4,14}$/;
                    if (!reg.test(qq)) {
                        showAlertError('QQ号格式错误！');
                        return false;
                    }
                }
                //layer.close(index);
                setQQ(qq);
            });
        },
        titleAlert:function(title) {
            console.log(title);
            alert(title)
        },
    },
    mounted:function() {
        // console.log("我是监控的mounted", app.tabIndex);
        let io = new IntersectionObserver((entries) => {
            if (app.tabIndex == 1) {
                let mysearch = getSession("isSearched");
                if (mysearch != "false") {
                    saveSession("isSearched", true);
                    // app.nextPage(app.tabIndex);
                    // 搜索页面没有滚动加载
                }
            } else if (app.tabIndex == 0 || app.tabIndex == 2) {
                app.nextPage(app.tabIndex, true);
            }
        });
        io.observe(document.getElementById('flag'));
    },

});

function setReward(data) {
    $.ajax({
        url: baseUrl + "/user/reward",
        data: JSON.stringify({'reward': data}),
        method: "PUT",
        success: function (res) {
            console.log(res);
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    // app.user.wxReward = res.data.reward;
                    // saveLocal("user", app.user);
                } else {
                    showAlertError(res.msg)
                }
    }});
}
//设置QQ号
function setQQ(qq) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/user/qq",
        data: JSON.stringify({'qq': qq}),
        method: "PUT",
        success: function (res) {
            console.log(res);
                if (res.success) {
                    layer.closeAll();
                    showOK(res.msg);
                    app.user.QQ = res.data.qq;
                    saveLocal("user", app.user);
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

//新增反馈
function pubFeedback(data) {
    $.ajax({
        url: baseUrl + "/feedbacks",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
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
        }
    });
}

//修改密码
function setPassword(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/user/password",
        data: JSON.stringify(data),
        method: "PUT",
        success: function (res) {
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
        url: baseUrl + "/lostfounds/delete/" + id,
        method: "DELETE",
        success: function (res) {
            console.log(res);
            if (res.success) {
                showOK(res.msg);
                saveSession("tabIndex", 2);
                app.tab[2].search.pageNum=0;
                $("html,body").scrollTop(0);
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
        url: baseUrl + "/notices",
        method: "GET",
        success: function (res) {
            if (res.success) {
                app.notice = res.data.list;
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

//删除消息（评论）
function removeComment(id) {
    console.log("我是要删除的ID:" + id);
    $.ajax({
        url: baseUrl + "/comments/" + id,
        method: "DELETE",
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
        url: baseUrl + "/user/messages",
        method: "GET",
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

 /**
     * 获得base64
     * @param {Object} obj
     * @param {Number} [obj.width] 图片需要压缩的宽度，高度会跟随调整
     * @param {Number} [obj.quality=0.8] 压缩质量，不压缩为1
     * @param {Function} [obj.before(this, blob, file)] 处理前函数,this指向的是input:file
     * @param {Function} obj.success(obj) 处理后函数
     * @example
     *
     */
    $.fn.localResizeIMG = function (obj) {
        // console.log("压缩函数localResizeIMG内",obj)
        this.on('change', function () {
            var file = this.files[0];
            var URL = window.URL || window.webkitURL;
            var binaryData = [];
            binaryData.push(file);
            var blob=URL.createObjectURL(new Blob(binaryData, {type: "application/zip"}))
            // var blob = URL.createObjectURL(file);

            // 执行前函数
            if ($.isFunction(obj.before)) {
                obj.before(this, blob, file)
            };

            _create(blob, file);
            this.value = ''; // 清空临时数据
        });

        /**
         * 生成base64
         * @param blob 通过file获得的二进制
         */
        function _create(blob) {
            var img = new Image();
            img.src = blob;

            img.onload = function () {
                var that = this;

                //生成比例
                var w = that.width,
                    h = that.height,
                    scale = w / h;
                w = obj.width || w;
                h = w / scale;

                //生成canvas
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                $(canvas).attr({
                    width: w,
                    height: h
                });
                ctx.drawImage(that, 0, 0, w, h);
                /**
                 * 生成base64
                 * 兼容修复移动设备需要引入mobileBUGFix.js
                 */
                var base64 = canvas.toDataURL('image/jpeg', obj.quality || 0.8);

                // 修复IOS
                if (navigator.userAgent.match(/iphone/i)) {
                    var mpImg = new MegaPixImage(img);
                    mpImg.render(canvas, {
                        maxWidth: w,
                        maxHeight: h,
                        quality: obj.quality || 0.8
                    });
                    base64 = canvas.toDataURL('image/jpeg', obj.quality || 0.8);
                }

                // 修复android
                if (navigator.userAgent.match(/Android/i)) {
                    var encoder = new JPEGEncoder();
                    base64 = encoder.encode(ctx.getImageData(0, 0, w, h), obj.quality * 100 || 80);
                }
                // 生成结果
                var result = {
                    base64: base64,
                    clearBase64: base64.substr(base64.indexOf(',') + 1)
                };
                // 执行后函数
                obj.success(result);
            };
        }
    };


//选择上传图片
function changeInput() {
    $("#imgInput").localResizeIMG({
        width: 1000,
        quality: 0.8,
        before: function () {
           showLoading("压缩中...");
        },
        success: function (result) {
            layer.closeAll('loading');
            app.tab4.images.push(result.base64);
        }}
    );
}

//发布启事
function pubLostFound(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/lostfounds",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                showOK(res.msg);
                app.tab4 = {
                    applyKind: 0,
                    categoryIndex: -1,
                    title: "",
                    about: "",
                    location: null,
                    images: [],//srcList
                };
            } else {
                showAlert(res.msg)
            }
        }
    });
}

//发布启事
function pubLostFound(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/lostfounds",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            if (res.success) {
                showOK(res.msg);
                app.tab[0].list = [];
                app.tab[0].search.pageNum = 0;
                app.tab[0].search.category = "";
                app.tab[0].search.kind = -1
                app.tab4 = {
                    applyKind: 0,
                    categoryIndex: -1,
                    categoryId: 13,
                    title: "",
                    about: "",
                    location: null,
                    images: [],//srcList
                };
                app.changeTab(0);
            } else {
                showAlertError(res.msg)
            }

        }
    });
}

//分页查寻启事列表
function pageLostFound(data, result, append) {
    $.ajax({
        url: baseUrl + "/lostfounds/page",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            if (res.success) {
                // result.search.pageNum = res.data.page.pageNum;
                result.search.pageSize = res.data.page.pageSize;
                result.totalPage = res.data.page.totalPage;
                result.total = res.data.page.total;
                if (append) {
                    for (let v in res.data.page.list) {
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
        url: baseUrl + "/categories",
        method: "GET",
        success: function (res) {
                if (res.success) {
                    app.category = res.data.list
                } else {
                    showAlertError(res.msg)
                }
        }
    });
}

$(function () {
    if (getSession("notice") != null) {
        app.notice = JSON.parse(getSession("notice"));
    } else {
        getNoticeList(app);
    }
    //从详情页返回,还要考虑中途退出的情况
    if (getLocal("isBack") == "true" && JSON.parse(getSession("tabIndex"))!=null) {
        app.tabIndex = JSON.parse(getSession("tabIndex"));
        console.log("我是现在的tab", app.tabIndex);
        if (app.tabIndex == 1) {
            //搜索的关键字
            app.tab[app.tabIndex].search["keyword"] = getSession("keyword")?getSession("keyword"):"";
            deleteSession("keyword");
        }
        if (app.tabIndex == 0) {
            //主页的搜索数据
            app.tab[0].search.pageNum =getSession("pageNum")? JSON.parse(getSession("pageNum")):0;
            app.tab[0].search.category = getSession("category")?getSession("category"):"";
            app.tab[0].search.kind = getSession("kind")?JSON.parse(getSession("kind")):-1;
        }
        if (app.tabIndex == 2) {
            app.tab[2].search.pageNum = getSession("pageNum")?JSON.parse(getSession("pageNum")):0;
        }
        app.tab[app.tabIndex].list = getSession("data")?JSON.parse(getSession("data")):[];
        $("html,body").scrollTop(getSession("scroll")?JSON.parse(getSession("scroll")):0)
        deleteLocal("isBack");
        deleteSession("data");
    }
    /**
     else {
        if(app.tabIndex == 3){
            console.log("页面加载的时候获取消息");
             app.changeTab(3);
        }
    }
     */
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

