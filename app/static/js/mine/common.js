//请求前缀
// const baseUrl = "http://127.0.0.1:8888";
// const staticUrl = "http://127.0.0.1:8888/static/thumb/";
const baseUrl = "http://iboy.f3322.net:8888";
const staticUrl = "http://iboy.f3322.net:8888/static/thumb/";
//全局设置ajax
$.ajaxSetup({
    dataType: "json",
    contentType: "application/json;charset=UTF-8",
    xhrFields: {"withCredentials": true},//携带cookie
    beforeSend: function () {
        // showLoading();
    },
    error: function (req, status, e) {
        hideLoading();
        console.log("ajax error --------------------------- start");
        console.log(this);
        console.log(req);
        console.log(status);
        console.log(e);
        console.log("ajax error ----------------------------- end");
        // alert("请求发生错误：\n" + this.url);
    },
    complete: function () {
    }
});

//将对象的value置为空串，key为忽略项
function cleanObj(obj, key) {
    for (let k in obj) {
        if (key && key === k) {
            continue;
        }
        obj[k] = "";
    }
}

function isAnonymous() {
    if (getLocal("user") == null) {
        showAlertError('登录状态已失效，请重新登录');
        setTimeout(function () {
            window.location = baseUrl + '/login';
        }, 3000);  //5秒后将会调用执行remind()函数
    }
}

//是否可用LocalStorage
function canUseLocal() {
    if (!window.localStorage) {
        console.log('浏览器不支持localStorage');
        alert("浏览器不支持localStorage");
        return false;
    } else {
        return true;
    }
}

//存入都是String
function saveLocal(key, value) {
    if (canUseLocal()) {
        let storage = window.localStorage;
        if (typeof value == "object") {
            storage.setItem(key, JSON.stringify(value));
            return;
        }
        storage.setItem(key, value);
    }
}

//返回时String，如果是json要转换，没有则是undefined
function getLocal(key) {
    if (canUseLocal()) {
        let storage = window.localStorage;
        return storage.getItem(key);
    }
    return null;
}

function deleteLocal(key) {
    let storage = window.localStorage;
    storage.removeItem(key);
}

function canUseSession() {
    if (sessionStorage) {
        return true;
    } else {
        console.log("can not user sessionStorage");
        alert("浏览器不支持sessionStorage");
        return false;
    }
}

function logout() {
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
                    deleteLocal("user");
                    window.location = baseUrl + '/login';
                }
            }
        });
    }, function () {
    });
}

function saveSession(key, value) {
    if (canUseSession()) {
        if (typeof value == "object") {
            sessionStorage.setItem(key, JSON.stringify(value));
            return;
        }
        sessionStorage.setItem(key, value)
    }
}

function getSession(key) {
    if (canUseSession()) {
        return sessionStorage.getItem(key);
    }
    return null;
}

function deleteSession(key) {
    sessionStorage.removeItem(key);
}

//paraName 等找参数的名称
function getUrlParam(paramName) {
    let url = document.location.toString();
    let arrObj = url.split("?");

    if (arrObj.length > 1) {
        let arrPara = arrObj[1].split("&");
        let arr;

        for (let i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");

            if (arr != null && arr[0] == paramName) {
                return arr[1];
            }
        }
        return "";
    } else {
        return "";
    }
}

//paraName 等找参数的名称
function getPostId() {
    let url = document.location.toString();
    let id=url.match("/detail/(.*).html")[0].match("\\d+")[0]
    return parseInt(id);
}

//显示loading
function showLoading(title) {
    //加载层-风格4
    layer.msg(title || '加载中', {
        icon: 16,
        shade: 0.4,
        time:500
    });
}

//隐藏loading
function hideLoading() {
    layer.closeAll('loading');
}

//无icon消息弹出框
function showAlert(msg, title) {
    layer.open({
        title: title || '消息'
        , content: msg
    });
}

//红色叉叉消息弹出框
function showAlertError(msg, title) {
    layer.open({
        title: title || '消息',
        content: msg,
        icon: 2
    });
}

//吐司一下
function showToast(msg) {
    layer.msg(msg, {icon: -1});
}

//橙色叹号
function showInfo(msg) {
    layer.msg(msg, {icon: 0});
}

//绿色的勾
function showOK(msg) {
    layer.msg(msg || "操作成功！", {icon: 1});
}

//红色叉叉
function showError(msg) {
    layer.msg(msg, {icon: 2});
}

//黄色问号
function showAsk(msg) {
    layer.msg(msg, {icon: 3});
}

//4灰色锁，5红色瘪嘴表情，6绿色笑脸

//百度统计
var hm = document.createElement("script");
$(function () {
  hm.src = "https://hm.baidu.com/hm.js?cadc146ea11d785cac889d32e36f336b";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})

