var app = new Vue({
    el: "#app",
    created(){
        this.getData();
    },
    data: {
        imgPrefix: staticUrl,
        user: getLocal("user") ? JSON.parse(getLocal('user')) : {},
        //数据总览
        //今日和总计
        // count:[[1,20],[2,10],[10,100]],
        lost:[1,20],
        found:[2,10],
        solve:[10,100],
        newCount:1,
        //近期数据
        /*            item:[
                        {
                            labels: ["前端04/11", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
                            // labels: [],
                            //柱状图
                            data: [[10, 70, 55, 20, 45, 0, 60],[65, 59, 90, 81, 56, 0, 40],[65, 1, 90, 81, 56, 1, 1]]
                        },
                        //面积图
                        {
                            labels: ["Jan", "Feb", "March", "April", "May", "June", "July"],
                            data: [[22, 31, 2, 40, 555, 65, 68],[1, 31, 2, 40, 55, 0, 68],[1, 1, 39, 1, 55, 65, 68]]
                        },
                        //饼状图
                        {
                            //拾取，丢失，找到
                            data:[10,20,88]
                        },
                        //用户数量变化图
                        {
                            labels:["04/13", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
                            data:[1, 31, 39, 100, 55, 65, 1]
                        },
                        //用户活跃量
                        {
                            lables:["Jan", "Feb", "March", "April", "May", "June", "July"],
                            data:[[22, 31, 39, 40, 55, 65, 68],[12, 15, 23, 34, 36, 44, 51]]
                        },
                        //性别比例
                        {
                            data:[100,12]
                        }
                    ]*/

        item:[
            ["04/11", "04/14", "04/15", "04/16", "04/17", "04/18", "04/13"],
            // labels: [],
            //柱状图
            [[10, 70, 55, 20, 45, 0, 60],[65, 59, 90, 81, 56, 0, 40],[65, 1, 90, 81, 56, 1, 1]]
            ,
            //面积图

            //饼状图

            //拾取，丢失，找到
            // [10,20,88]

            //用户数量变化图

            [1, 31, 39, 100, 55, 65, 1]
            ,
            //用户活跃量

            [[22, 31, 39, 40, 55, 65, 68],[12, 15, 23, 34, 36, 44, 51]]
            ,
            //性别比例

            [100,12]

        ]

    },
    methods: {
        logout() {
           logout()
        },
        getData:function(){
            let self=this;
            $.ajax({
                url:baseUrl+'/chart.html',
                method:'POST',
                async:false,
                success:function(res) {
                    if(res.success){
                        self.newCount=res.data.newCount;
                        self.lost=res.data.lost;
                        self.found=res.data.found;
                        self.solve=res.data.solve;
                        self.item=res.data.item;
                        // self.lables=res.data.lables;
                        /*
                         self.item=res.data.item;*/
                    }
                    else {
                        showAlertError(res.msg);
                    }
                }
            });
        },
    },
    mounted(){
        drawChart(this);
    }
});

function disableOther(button) {
    if (button !== 'showLeftPush') {
        classie.toggle(showLeftPush, 'disabled');
    }
}
function drawChart(app){

//近期数据
//失物、招领、寻回三种占比
    var barChartData1 = {
        labels:app.item[0],
        datasets: [
            {
                fillColor: "#4F52BA",
                strokeColor: "#4F52BA",
                highlightFill: "#4F52BA",
                highlightStroke: "#4F52BA",
                data: app.item[1][0],
            },
            {
                fillColor: "#e94e02",
                strokeColor: "#e94e02",
                highlightFill: "#e94e02",
                highlightStroke: "#e94e02",
                data: app.item[1][1],
            },
            {
                fillColor: "#3dab53",
                strokeColor: "#3dab53",
                highlightFill: "#3dab53",
                highlightStroke: "#3dab53",
                data: app.item[1][2],
            }
        ]

    };
//近期趋势
//失物，招领，寻回占比
    var lineChartData1 = {
        labels: app.item[0],
        datasets: [
            {
                fillColor: "rgba(79, 82, 186, 0.9)",
                strokeColor: "rgba(79, 82, 186, 0.9)",
                pointColor: "rgba(79, 82, 186, 0.9)",
                pointStrokeColor: "#fff",
                data: app.item[1][0],

            },
            {
                fillColor: "rgba(233, 78, 2, 0.9)",
                strokeColor: "rgba(233, 78, 2, 0.9)",
                pointColor: "rgba(233, 78, 2, 0.9)",
                pointStrokeColor: "#9358ac",
                data: app.item[1][1],

            },
            {
                fillColor: "#3dab53",
                strokeColor: "#3dab53",
                pointColor: "#3dab53",
                pointStrokeColor: "#9358ac",
                data: app.item[1][2],
            }
        ]

    };
//失物，拾取，解决占比

    var pieData1 = [
        {
            value: app.lost[1],
            color: "#4F52BA",
            label: "失物",
            percentageInnerCutout: 50
        },
        {
            value:app.found[1],
            color: "#e94e02",
            label: "拾物",
            percentageInnerCutout: 50
        },
        {
            value: app.solve[1],
            color: "#3dab53",
            label: "寻回",
            percentageInnerCutout: 50
        }
    ];

    var line1 = new Chart(document.getElementById("line1").getContext("2d")).Line(lineChartData1, {pointDot: true});
    new Chart(document.getElementById("bar1").getContext("2d")).Bar(barChartData1);
    new Chart(document.getElementById("pie1").getContext("2d")).Pie(pieData1, {percentageInnerCutout: 50});

/////////////////////////

//用户数量
    var lineChartData2 = {
        labels: app.item[0],
        datasets: [
            {
                fillColor: "#2673ec",
                strokeColor: "rgba(79, 82, 186, 0.9)",
                pointColor: "rgba(79, 82, 186, 0.9)",
                pointStrokeColor: "#fff",
                data: app.item[2]
            }
        ]
    };
//活跃用户
    var lineChartData3 = {
        labels: app.item[0],
        datasets: [
            {
                fillColor: "#00b5ad",
                strokeColor: "rgba(79, 82, 186, 0.9)",
                pointColor: "#00b5ad",
                pointStrokeColor: "#fff",
                data: app.item[3][0]
            },
            {
                fillColor: "#e03997",
                strokeColor: "rgba(233, 78, 2, 0.9)",
                pointColor: "#e03997",
                pointStrokeColor: "#9358ac",
                data: app.item[3][1]
            }
        ]
    };

//性别比例
    var pieData2 = [
        {
            value: app.item[4][0],
            color: "#00b5ad",
            label: "男",
            percentageInnerCutout: 50
        },
        {
            value: app.item[4][1],
            color: "#e03997",
            label: "女",
            percentageInnerCutout: 50
        }
    ];

    new Chart(document.getElementById("line2").getContext("2d")).Line(lineChartData2, {pointDot: true});
    new Chart(document.getElementById("line3").getContext("2d")).Line(lineChartData3, {pointDot: true});
    new Chart(document.getElementById("pie2").getContext("2d")).Pie(pieData2, {percentageInnerCutout: 50});

    let menuLeft = document.getElementById('cbp-spmenu-s1'),
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
}
