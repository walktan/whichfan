
//初期処理
$(document).ready(function(){
  // 時間入力窓の入力補助設定
  $('#fromTime').datetimepicker({minDate:new Date(2016, 2 - 1, 4),maxDate: '+0d'}).attr('readonly','readonly');
  $('#toTime').datetimepicker({minDate:new Date(2016, 2 - 1, 4),maxDate: '+1d'}).attr('readonly','readonly');

  // グラフ描画
  drawGraph();

  // 期間変更ボタン押下時処理
  $('#termFm').submit(function() {
      if(checkInput()){
      drawGraph()
      }
      return false;
  });

  // daily,hourly切り替え時処理
  $( 'input[name="frequency"]:radio' ).change( function() {
    if(checkInput()){
    drawGraph()
    }
    return false;
  });

  // 入力値チェック
  //両方ブランクの場合はデフォルト表示にするのでOKとする
  function checkInput(){
     target = document.getElementById("alertMsg")
     if((($('#fromTime').val() == "") && ($('#toTime').val() != "")) || (($('#fromTime').val() != "") && ($('#toTime').val() == ""))){
     target.innerHTML = "期間を設定してください";
     return false
  }else if($('#fromTime').val() > $('#toTime').val()){
     target.innerHTML = "期間に誤りがあります";
     return false
  }else{
     target.innerHTML = "";
  return true
  }
  }
});


// graph全体の描画
function graph(id, fData){

    // 円グラフおよび棒グラフの色設定
    var barColor = '#5da67f';
    function segColor(c){ return {Swallows:"#44487e", Giants:"#ff8e11", Dragons:"#1135a9", Carp:"#ff1111", BayStars:"#275bc1" ,Tigers:"#eeee11"}[c]; }

    // トータル件数の取得
    fData.forEach(function(d){d.total=d.twicnt.Carp+d.twicnt.Giants+d.twicnt.Dragons+d.twicnt.Tigers+d.twicnt.BayStars+d.twicnt.Swallows;});

    // 棒グラフの描画
    function histoGram(fD){
        var hG={},    hGDim = {t: 40, r: 0, b: 80, l: 0};
        hGDim.w = 900
        hGDim.h = 320

        // バー作成
        var hGsvg = d3.select(id).append("svg").attr('class','histogram')
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

        // x-axisマッピング
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function(d) { return d[0]; }));

        // x-axis作成
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0,346)")
            .call(d3.svg.axis().scale(x).orient("bottom").tickSize(0,0)).attr("verticalAlign","top");

        // y-axisマッピング
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // 棒グラフ作成
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");

        // 長方形作成
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor)
            .on("mouseover",mouseover)
            .on("mouseout",mouseout);

        // ラベル作成
        bars.append("text").text(function(d){ return d3.format(",")(d[1])})
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("text-anchor", "middle");

        // バーへのマウスオーバ時
        function mouseover(d){
            var st = fData.filter(function(s){ return s.Team == d[0];})[0],
                nD = d3.keys(st.twicnt).map(function(s){ return {type:s, twicnt:st.twicnt[s]};});

            // 円グラフ、凡例、テキストの更新
            pC.update(nD);
            leg.update(nD);
            stTerm.text('');
            vec.text(st.Team);
            enTerm.text('');

        }

        // バーへのマウスアウト時処理
        function mouseout(d){
            pC.update(tF);
            leg.update(tF);
            stTerm.text(sF[0][0]);
            vec.text('>>');
            enTerm.text(sF[sF.length - 1][0]);

        }

        // バーの更新
        hG.update = function(nD, color){
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);

            var bars = hGsvg.selectAll(".bar").data(nD);

            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });
        }
        return hG;
    }

    // 円グラフの描画
    function pieChart(pD){
        var pC ={},    pieDim ={w:240, h: 240};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

        // 円グラフ用svg作成
        var piesvg = d3.select(id).append("svg").attr('class','piechart')
            .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
            .attr("transform", "translate("+pieDim.w/2+","+pieDim.h/2+")");

        // 円弧作成
        var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

        // Team毎のtwit数取得
        var pie = d3.layout.pie().sort(null).value(function(d) { return d.twicnt; });

        // 円グラフ表示
        piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
            .each(function(d) { this._current = d; })
            .style("fill", function(d) { return segColor(d.data.type); })
            .on("mouseover",mouseover).on("mouseout",mouseout);

        // 円グラフの更新
        pC.update = function(nD){
            piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                .attrTween("d", arcTween);
        }
        // 円グラフのマウスオーバ時処理
        function mouseover(d){
            hG.update(fData.map(function(v){
                return [v.Team,v.twicnt[d.data.type]];}),segColor(d.data.type));
            team.text(d.data.type);
        }

        // 円グラフのマウスオーバ時処理
        function mouseout(d){
            hG.update(fData.map(function(v){
                return [v.Team,v.total];}), barColor);
            team.text('All');
        }
        // 円グラフ変化アニメーションの設定
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t));    };
        }
        return pC;
    }

    // 凡例の描画
    function legend(lD){
        var leg = {};

        var legend = d3.select(id).append("table").attr('class','legend');

        var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
			.attr("fill",function(d){ return segColor(d.type); });

        tr.append("td").text(function(d){ return d.type;});

        tr.append("td").attr("class",'legendTwicnt')
            .text(function(d){ return d3.format(",")(d.twicnt);});

        tr.append("td").attr("class",'legendPerc')
            .text(function(d){ return getLegend(d,lD);});

        //凡例の更新
        leg.update = function(nD){
            var l = legend.select("tbody").selectAll("tr").data(nD);

            l.select(".legendTwicnt").text(function(d){ return d3.format(",")(d.twicnt);});

            l.select(".legendPerc").text(function(d){ return getLegend(d,nD);});
        }

        function getLegend(d,aD){
            return d3.format("%")(d.twicnt/d3.sum(aD.map(function(v){ return v.twicnt; })));
        }

        return leg;
    }


    // 全Teamのサマリデータ取得
    var tF = ['Swallows','Giants','Dragons','Carp','BayStars','Tigers'].map(function(d){
        return {type:d, twicnt: d3.sum(fData.map(function(t){ return t.twicnt[d];}))};
    });

    // Team毎のサマリデータ取得
    var sF = fData.map(function(d){return [d.Team,d.total];});

    //表示用オブジェクト
    var leg= legend(tF); //凡例
        pC = pieChart(tF); //円グラフ
        enTerm = d3.select(id).append("text").text(sF[sF.length - 1][0]).attr('class','enTerm'); //開始日_テキスト
        vec = d3.select(id).append("text").text('>>').attr('class','vec'); //ベクトル_テキスト
        stTerm = d3.select(id).append("text").text(sF[0][0]).attr('class','stTerm'); //終了日_テキスト
        team = d3.select(id).append("text").text("All").attr('class','team'); //チーム名_テキスト
        hG = histoGram(sF); //棒グラフ
        }


//グラフ描画用のjson
var twicntData=[];

//ajax実行中flag（ajax連続実行防止のため）
var ajaxSending = false;

//グラフ描画用json取得
function drawGraph(){
  try{
     if(!ajaxSending){
     ajaxSending = true;
     $(":radio").prop("disabled",true); //ラジオボタン無効化
     $('#graph').empty();
     dispLoading("Loading...");
     $.ajax({
           'url':$('form#termFm').attr('action'),
           'type':'POST',
           'data':{
              'fromTime':$('#fromTime').val(),
              'toTime':$('#toTime').val(),
              'frequency':$("input[name='frequency']:checked").val(),
            },
           'dataType':'json',
           'success':function(response){
              twicntData = response
                   twicntData = response
               },
           'complete': function(jqXHR, statusText){
              ajaxSending = false;
              $(":radio").prop("disabled",false); //ラジオボタン有効化
              removeLoading();
              graph('#graph',twicntData);
              },
           });
           return false;
     }else{
     }
  }catch(e){
    ajaxSending = false;
    $(":radio").prop("disabled",false); //ラジオボタン有効化
  }
}


//Loadingイメージの表示
  function dispLoading(msg){
    // 画面表示メッセージ
    var dispMsg = "";

    // 引数が空の場合は画像のみ
    if( msg != "" ){
        dispMsg = "<div class='loadingMsg'>" + msg + "</div>";
    }
    // ローディング画像が表示されていない場合のみ表示
    if($("#loading").size() == 0){
        $("body").append("<div id='loading'>" + dispMsg + "</div>");
    }
}


// Loadingイメージ削除関数
function removeLoading(){
	$("#loading").remove();
}


//CSRF対策
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});