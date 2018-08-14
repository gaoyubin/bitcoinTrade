function  createTable(id,data,title){

    id.children("table").remove()


    console.log(data)

    var table = $('<table  border="1"  class="table table-responsive table-condensed table-bordered table-hover  " role="grid" style="margin:0px ;font-size:18px; border: 1px solid #2A91D8;" >');

    table.appendTo(id);


    var caption=$("<caption style='text-align: center;font-size: 24px;font-weight: bold;color:black;padding-bottom: 10px' >"+title+"</caption>")
    caption.appendTo(table)

    tableHead=new Array("订单类型","成交时间","成交数量","成交手续费","成交价格")
    var tr = $("<thead></thead>");
    tr.appendTo(table);
    for(var i=0;i<tableHead.length;i++)
    {
        var td = $("<th  style='text-align: center;background-color: rgba(117, 192, 255, 0.52)' >"+tableHead[i]+"</th>");
        td.appendTo(tr);
    }


   for(var i=0;i<data.length;i++){
        var tr=$("<tr></tr>");
         tr.appendTo(table);
         for(var j=0;j<data[i].length;j++){
              var td = $("<td  style='text-align: center;'>" + data[i][j] + "</td>");
              td.appendTo(tr);
         }
   }

    id.append("</table>");

}

function createECharts(data){
    var myChart = echarts.init(document.getElementById('main'));
    option = {
    title : {
        text: '比特币趋势以及购买情况'
    },
    tooltip : {
        trigger: 'axis',
        formatter: function (params) {
            var res = params[0].seriesName + ' ' + params[0].name;
            res += '<br/>  开盘 : ' + params[0].value[0] + '  最高 : ' + params[0].value[3];
            res += '<br/>  收盘 : ' + params[0].value[1] + '  最低 : ' + params[0].value[2];
            return res;
        }
    },
    legend: {
        data:['上证指数','买','卖']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataZoom : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    dataZoom : {
        show : true,
        realtime: true,
        start : 50,
        end : 100
    },
    xAxis : [
        {
            type : 'category',
            boundaryGap : true,
            axisTick: {onGap:false},
            splitLine: {show:false},
            data : data["times"]
        }
    ],
    yAxis : [
        {
            type : 'value',
            scale:true,
            boundaryGap: [0.01, 0.01]
        },
         {
            type : 'value',
            name : '投资情况'

        }
    ],
    series : [
        {
            name:'上证指数',
            type:'k',
            // 开盘，收盘，最低，最高
            data:data["klines"]
        },
        {
               name:'买',
            type:'bar',
            yAxisIndex: 1,
            data:data["buy-limit"]
        },
        {
               name:'卖',
            type:'bar',
            yAxisIndex: 1,
            data:data["sell-limit"]
        }



    ],
    color: ['rgb(239,219,200)','rgb(137,246,100)','rgb(155,314,203)','rgb(155,155,146)','rgb(111,222,100)']
};

    myChart.setOption(option);

}
$(function () {




    $('#checkBtn').click(function () {
        console.log("btn")

        if($('#klineType').val()=="30min")
            size=parseInt($('#dates').val())*24*2
        else if($('#klineType').val()=="60min")
            size=parseInt($('#dates').val())*24
        else if($('#klineType').val()=="1day")
            size=parseInt($('#dates').val())

            var data = {"symbol": $('#coinType').val(),
        "period": $('#klineType').val(),
        "size": size}
        console.log(data)
         $.ajax(
        {
            type: 'GET',
            url: '/api/check/getkline',
            dataType: 'json',//希望服务器返回json格式的数据
            data: data,
            success: function (data) {
                console.log(data)
                createECharts(data)
                createTable($('#matcheTable'),data["matchRecords"])
            },

            async: false,
        }
    );
    })
    $('#checkBtn').click()
    $.ajax({
         type: 'GET',
            url: '/api/check/getBalance',
            dataType: 'json',//希望服务器返回json格式的数据

            success: function (data) {
                console.log(data)
                $('#tradeBalance').html(data["tradeBalance"])
                $('#frozenBalance').html(data["frozenBalance"])
            },

            async: false,
    })


});
