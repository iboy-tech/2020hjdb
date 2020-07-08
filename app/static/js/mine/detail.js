var app = new Vue({
    el: "#app",
    created() {
        let id = getPostId();
        this.getDetail(id);
    },
    data: {
        wxReward: "",
        mailApi: "https://mail.qq.com/cgi-bin/qm_share?t=qm_mailme&email=",
        qqApi: "https://wpa.qq.com/msgrd?v=3&site=qq&menu=yes&uin=",
        imgPrefix: staticUrl,
        userIcon: "https://ae01.alicdn.com/kf/U89b7be7d8d234a38b9a4b0d4258de362X.jpg",
        comment: "",//发布评论
        //从相关页面进入
        isRelate: getSession("toIndex") ? JSON.parse(getSession("toIndex")) : true,
        images: {
            "title": "", //相册标题
            "id": "", //相册id
            "start": 0, //初始显示的图片序号，默认0
            "data": [   //相册包含的图片，数组格式
                /* {
                     "alt": "图片名",
                     "pid": 666, //图片id
                     "src": "", //原图地址
                     "thumb": "" //缩略图地址
                 }*/
            ]
        },
        report: {
            id: "",
            content: "",
        },
        item: {
            id: null,
            icon: "https://ae01.alicdn.com/kf/U89b7be7d8d234a38b9a4b0d4258de362X.jpg",
            kind: 1,
            username: "",
            userId: "",
            time: "",
            location: "",
            title: "",
            about: "",
            images: [],
            category: "",
            lookCount: 12,
            status: 1,
            dealTime: null,
            isSelf: false,
            isAdmin: false,
            email: "",
            QQ: "",
        },
        comments: "",
        page: {
            search: {//tab1
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
        feedback: {
            "subject": "违规信息举报",
            "content": ""
        }
    },
    methods: {
        loadJS: function () {//加载js
            let loadScript = document.createElement("script");
            loadScript.type = "text/javascript";
            loadScript.src = "../static/js/share/js/social-share.js";
            document.head.appendChild(loadScript);
        },
        share: function () {
            //捕获页
            layer.open({
                type: 1,
                area: "auto",
                //shade: true,
                scrollbar: false, // 父页面 滚动条 禁止
                title: "<h4 style='text-align: center !important;'>微信扫一扫分享</h4>", //不显示标题
                content: $('#shareDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
            });
        },
        reward: function () {
            if (app.wxReward == "") {
                showInfo("用户暂未设置赞赏码，快去提醒他(她)设置吧！");
            } else {
                layer.open({
                    type: 1,
                    area: "auto",
                    scrollbar: false, // 父页面 滚动条 禁止
                    // shade: true,
                    title: "<h4 style='text-align: center !important;'>微信扫一扫，打赏</h4>", //不显示标题
                    content: $('#rewardDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                });

                $("#reward-div").empty();
                new QRCode("reward-div", {
                    text: app.wxReward,
                    width: 150,
                    height: 150,
                });
                // new QRCode(document.getElementById("reward-div"), app.wxReward);  // 设置要生成二维码的链接
            }
        },
        pubComment: function (id) {
            console.log(this.comment);
            let data = {
                "targetId": id,
                "content": this.comment
            };
            console.log(data);
            pubComment(data, this);
        },
        deletePub: function (id) {
            console.log(id);
            layer.confirm('确定要删除吗？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deletePub(id);
            }, function () {

            });
        },
        showFeedback: function () {
            layer.open({
                btn: ['确定', '取消'],
                type: 1,
                area: ['70%', 'auto'],
                //shade: true,
                title: "违规信息举报", //不显示标题
                content: $('#editorDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
                , yes: function () {
                    console.log(app.feedback);
                    if (app.feedback.content == "") {
                        showAlertError('请填写举报理由!');
                        return;
                    }
                    let obj = {
                        "subject": "违规信息举报",
                        "content": app.feedback.content
                    };
                    pubFeedback(obj);
                }, cancel: function () {

                }
            });
        },
        //获得启事详情
        getDetail: function (id) {
            console.log('这是帖子的ID:' + id);
            $.ajax({
                url: baseUrl + "/detail/" + id + ".html",
                // data:id,
                method: "POST",
                // async : false,
                success: function (res) {
                    console.log(res);
                    if (res.success) {
                        //console.log(result.item);
                        app.item = res.data.item;
                        //console.log(result.item);
                        app.page.search.category = $("#search-category").text();
                        console.log(app.page.search);
                        if (getLocal("user")) {
                            getComments(id, app);
                            pageLostFound(app.page.search, app.page);
                        }
                    } else {
                        showAlertError(res.msg)
                    }
                }
            });
        },
        jumpDetail: function (id) {
            console.log("执行相关函数");
            //从相关启示进去，出来直接返回主页面
            app.isRelate = true;
            saveSession("toIndex", true);
            saveSession("category", "");
            saveSession("kind", -1);
            // deleteSession("data");
            saveLocal("isBack", false);
            // sessionStorage.clear();
            //跳转详情页面
            location.href = baseUrl + "/detail/" + id + ".html";
        },
        claim: function (flag, id) {
            if (flag == 1) {
                layer.confirm("物品是您的吗？", {
                    btn: ["是的", "不是"]
                }, function () {
                    claimID(id);
                }, function () {
                });
            } else {
                layer.confirm("您找到失物了吗？", {
                    btn: ["是的", "不是"]
                }, function () {
                    claimID(id);
                }, function () {
                });
            }
        }

    },
    mounted() {
        // console.log("挂载完成",this.isRelate);
        this.loadJS();//页面渲染完成后加载分享组件
        deleteLocal("isRelate");
    }
});

//新增反馈
function pubReport(data) {
    console.log(data);
    $.ajax({
        url: baseUrl + "/detail/report",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            if (res.success) {
                layer.closeAll();
                showOK(res.msg);
                app.report = {
                    id: "",
                    content: ""
                }
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
                saveSession("category", "");
                saveSession("kind", -1);
                saveSession("tabIndex", 0);
                saveLocal("isBack", false);
                location.href = baseUrl;
            } else {
                showAlertError(res.msg)
            }
        }
    });

}

//查询相关类别
function pageLostFound(data, result) {
    $.ajax({
        url: baseUrl + "/found.html/getall",
        data: JSON.stringify(data),
        method: "POST",
        beforeSend: function () {
        },
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    result.search.pageNum = res.data.page.pageNum;
                    result.search.pageSize = res.data.page.pageSize;
                    result.totalPage = res.data.page.totalPage;
                    result.total = res.data.page.total;
                    result.list = res.data.page.list;
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

//发布评论
function pubComment(data, app) {
    $.ajax({
        url: baseUrl + "/comments/" + getPostId(),
        data: JSON.stringify(data),
        method: "POST",
        success: function (res) {
            console.log(res);
            console.log(res);
            console.log(typeof (res.ext), res.ext, res.ext == null);
            if (res.success) {
                showOK(res.msg);
                app.comment = "";
                // location.reload();
                console.log('把评论框清空')
                console.log('我是传给详情的ID:' + app.item.id)
                console.log("" + data.targetId)
                app.getDetail(getPostId());
                console.log('评论完成之后刷新')
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

//获得启事评论列表
function getComments(data, app) {
    console.log("评论有BUG：", data);
    $.ajax({
        url: baseUrl + "/comments/" + getPostId(),
        method: "POST",
        success: function (res) {
            if (res.success) {
                //console.log(result.item);
                app.comments = res.data.comments;
                app.wxReward = res.data.wxReward;
            } else {
                showAlertError(res.msg)
            }
        }
    });
}

//新增反馈
function pubFeedback(data) {
    data.content = data.content.concat(" (详情链接：" + location.href + ")");
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

function viewImages1(index) {
    console.log('我是相册下标' + index)
    //相册层
    // this.images.data = [];
    var images = [];
    var start = index;
    // let i = 0;
    // let t = $("#share-images img").length;
    // for (; i < t; i++) {
    //     let src = app.imgPrefix+this.item.images[i];
    //     let d = {"src":src};
    //     this.images.data.push(d);
    // }
    $("#share-images img").each(function () {
        var url = $(this).attr("src");
        images.push(url);
    });
    app.images.data = images;
    console.log(images);
    layer.photos({
        photos: images,//格式见API文档手册页
        anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机
    });
}

function viewImages(index) {
    //相册层
    app.images.data = [];
    app.images.start = index;
    $("#share-images img").each(function () {
        var url = $(this).attr("src").replace("thumb", "upload");
        let d = {"src": url}
        app.images.data.push(d);
    });
    console.log(app.images);
    layer.photos({
        photos: app.images,//格式见API文档手册页
        anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机
    });
}


//认领物品
function claimID(id) {
    $.ajax({
        url: baseUrl + "/user.html/claim?id=" + id,
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    showOK(res.msg);
                    if (res.msg.indexOf("认领") != -1) {
                        $("#claim").empty();
                        res = "<button class=\"ui green small button\">已认领</button>";
                        $("#claim").append(res);
                    } else {
                        $("#report").empty();
                        res = "<button class=\"ui green small button\">已找到</button>";
                        $("#report").append(res);
                    }

                }
            } else {
                console.log(res);
                showAlertError(res)
            }
        }
    });
}
