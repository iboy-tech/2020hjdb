var app = new Vue({
    el: "#app",
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal("user")) : {},
    },
    methods: {
        logout() {
            logout();
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