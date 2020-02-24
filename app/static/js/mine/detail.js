var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        userIcon: "https://ae01.alicdn.com/kf/U89b7be7d8d234a38b9a4b0d4258de362X.jpg",
        comment: "",//发布评论
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
                email: "",
                QQ: "",
        },
        comments: [],
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
    },
    methods: {
        share(){
            //捕获页
            layer.open({
                type: 1,
                //shade: true,
                title: "<h4>微信扫一扫分享</h4>", //不显示标题
                content: $('#shareDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
            });
        },
/*        share(){
            console.log(location.href);
            //捕获页
            layer.open({
                type: 1,
                //shade: true,
                title: "微信扫一扫：分享", //不显示标题
                content: $('#shareDiv') //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响
            });
        },*/
        viewImages(index) {
            //相册层
            this.images.data = [];
            this.images.start = index;
            let i = 0;
            let t = this.item.images.length;
            for (; i < t; i++) {
                let src = app.imgPrefix+this.item.images[i];
                let d = {"src":src};
                this.images.data.push(d);
            }
            console.log(this.images);

            layer.photos({
                photos: this.images,//格式见API文档手册页
                anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机
            });
        },
        pubComment() {
            console.log(this.comment);
            let data = {
                "targetId": this.item.id,
                "content": this.comment
            };
            console.log(data);
            pubComment(data, this);
        },
        deletePub(id) {
            console.log(id);
            layer.confirm('确定要删除码？', {
                btn: ['确定', '取消'] //按钮
            }, function () {
                deletePub(id);
            }, function () {

            });

        },
        jumpDetail(id) {
            //跳转详情页面
            window.open(baseUrl+"/detail.html?id=" + id, "_self");
        },
        claim(flag,id){
            if(flag==1){
                 layer.confirm("物品是您的吗？" , {
                     btn:["是的","不是"]
                },function () {
                    claimID(id);
                 },function () {
            });
            }
            else{
                layer.confirm("您找到失物了吗？" , {
                     btn:["是的","不是"]
                },function () {
                    claimID(id);
                 },function () {
                });
            }
        }

    }
});

$(function () {
    let id = getUrlParam("id");
    if (!id) {
        showAlertError("缺少请求参数！");
    } else {
        getDetail(id, app);
    }
    // var qrcode = new QRCode(document.getElementById("imgDiv"), location.href);
});

//删除招领信息
function deletePub(id) {
    $.ajax({
        url: baseUrl + "/found.html/delete?id="+id,
        method: "POST",
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    // showOK(res.msg);
                    window.location.href=baseUrl+'/user.html';
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
                alert(res)
            }
        }
    });
}

//发布评论
function pubComment(data, app) {
    $.ajax({
        url: baseUrl + "/comment",
        data: JSON.stringify(data),
        method: "POST",
        success: function (res, status) {
            console.log(res);
            console.log(res);
            console.log(typeof(res.ext),res.ext,res.ext==null);
            if (status == "success") {
                if (res.success) {
                    showOK("发布成功！");
                    app.comment = "";
                    // location.reload();
                    console.log('把评论框清空')
                    console.log('我是传给详情的ID:'+app.item.id)
                    console.log(""+data.targetId )
                    getDetail(app.item.id, app);
                    console.log('评论完成之后刷新')
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

//获得启事评论列表
function getComments(id, app) {
    //console.log(data);
    $.ajax({
        url: baseUrl + "/comment?id=" + id,
        method: "POST",
        success: function (res, status) {

            if (status == "success") {
                if (res.success) {
                    //console.log(result.item);
                    app.comments = res.data.comments;
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

//获得启事详情
function getDetail(id, result) {
    console.log('这是帖子的ID:'+id);
    $.ajax({
        url: baseUrl + "/detail.html?id="+id,
        // data:id,
        method: "POST",
        // async : false,
        success: function (res, status) {
            console.log(res);
            if (status == "success") {
                if (res.success) {
                    //console.log(result.item);
                    result.item = res.data.item;
                    //console.log(result.item);
                    app.page.search.category = res.data.item.category;
                    console.log(app.page.search);
                    if (getSession('user')) {
                        getComments(result.item.id, app);
                        pageLostFound(app.page.search, app.page);
                    }
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
                    getDetail(id, app);
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
