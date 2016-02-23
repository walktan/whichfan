
    $('#from_time').datetimepicker({minDate:new Date(2016, 2 - 1, 4),maxDate: '+0d'}).attr('readonly','readonly');
    $('#to_time').datetimepicker({minDate:new Date(2016, 2 - 1, 4),maxDate: '+1d'}).attr('readonly','readonly');

function dashboard(id, fData){
    var barColor = '#5da67f';
    function segColor(c){ return {Swallows:"#44487e", Giants:"#ff8e11", Dragons:"#1135a9", Carp:"#ff1111", Baystars:"#275bc1" ,Tiggers:"#eeee11"}[c]; }

    // compute total for each state.
    fData.forEach(function(d){d.total=d.freq.Carp+d.freq.Giants+d.freq.Dragons+d.freq.Tiggers+d.freq.Baystars+d.freq.Swallows;});

    // function to handle histogram.
    function histoGram(fD){
        var hG={},    hGDim = {t: 40, r: 0, b: 80, l: 0};
        hGDim.w = 900
        hGDim.h = 320

        //create svg for histogram.
        var hGsvg = d3.select(id).append("svg").attr('class','histogram')
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

        // create function for x-axis mapping.
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function(d) { return d[0]; }));

        // Add x-axis to the histogram svg.
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0,346)")
            .call(d3.svg.axis().scale(x).orient("bottom").tickSize(0,0)).attr("verticalAlign","top");

        // Create function for y-axis map.
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");

        //create the rectangles.
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor)
            .on("mouseover",mouseover)// mouseover is defined below.
            .on("mouseout",mouseout);// mouseout is defined below.

        //Create the frequency labels above the rectangles.
        bars.append("text").text(function(d){ return d3.format(",")(d[1])})
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("text-anchor", "middle");

        function mouseover(d){  // utility function to be called on mouseover.
            // filter for selected state.
            var st = fData.filter(function(s){ return s.State == d[0];})[0],
                nD = d3.keys(st.freq).map(function(s){ return {type:s, freq:st.freq[s]};});

            // call update functions of pie-chart and legend.
            pC.update(nD);
            leg.update(nD);
            stTerm.text(st.State);
            vec.text('');
            enTerm.text('');

        }

        function mouseout(d){    // utility function to be called on mouseout.
            // reset the pie-chart and legend.
            pC.update(tF);
            leg.update(tF);
            stTerm.text(sF[0][0]);
            vec.text('>>');
            enTerm.text(sF[sF.length - 1][0]);

        }

        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(nD, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);

            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);

            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });
        }
        return hG;
    }

    // function to handle pieChart.
    function pieChart(pD){
        var pC ={},    pieDim ={w:240, h: 240};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

        // create svg for pie chart.
        var piesvg = d3.select(id).append("svg").attr('class','piechart')
            .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
            .attr("transform", "translate("+pieDim.w/2+","+pieDim.h/2+")");

        // create function to draw the arcs of the pie slices.
        var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

        // create a function to compute the pie slice angles.
        var pie = d3.layout.pie().sort(null).value(function(d) { return d.freq; });

        // Draw the pie slices.
        piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
            .each(function(d) { this._current = d; })
            .style("fill", function(d) { return segColor(d.data.type); })
            .on("mouseover",mouseover).on("mouseout",mouseout);

        // create function to update pie-chart. This will be used by histogram.
        pC.update = function(nD){
            piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                .attrTween("d", arcTween);
        }
        // Utility function to be called on mouseover a pie slice.
        function mouseover(d){
            // call the update function of histogram with new data.
            hG.update(fData.map(function(v){
                return [v.State,v.freq[d.data.type]];}),segColor(d.data.type));
            team.text(d.data.type);
        }

        //Utility function to be called on mouseout a pie slice.
        function mouseout(d){
            // call the update function of histogram with all data.
            hG.update(fData.map(function(v){
                return [v.State,v.total];}), barColor);
            team.text('');
        }
        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t));    };
        }
        return pC;
    }

    // function to handle legend.
    function legend(lD){
        var leg = {};

        // create table for legend.
        var legend = d3.select(id).append("table").attr('class','legend');

        // create one row per segment.
        var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
			.attr("fill",function(d){ return segColor(d.type); });

        // create the second column for each segment.
        tr.append("td").text(function(d){ return d.type;});

        // create the third column for each segment.
        tr.append("td").attr("class",'legendFreq')
            .text(function(d){ return d3.format(",")(d.freq);});

        // create the fourth column for each segment.
        tr.append("td").attr("class",'legendPerc')
            .text(function(d){ return getLegend(d,lD);});

        // Utility function to be used to update the legend.
        leg.update = function(nD){
            // update the data attached to the row elements.
            var l = legend.select("tbody").selectAll("tr").data(nD);

            // update the frequencies.
            l.select(".legendFreq").text(function(d){ return d3.format(",")(d.freq);});

            // update the percentage column.
            l.select(".legendPerc").text(function(d){ return getLegend(d,nD);});
        }

        function getLegend(d,aD){ // Utility function to compute percentage.
            return d3.format("%")(d.freq/d3.sum(aD.map(function(v){ return v.freq; })));
        }

        return leg;
    }


    // calculate total frequency by segment for all state.
    var tF = ['Swallows','Giants','Dragons','Carp','Baystars','Tiggers'].map(function(d){
        return {type:d, freq: d3.sum(fData.map(function(t){ return t.freq[d];}))};
    });

    // calculate total frequency by state for all segment.
    var sF = fData.map(function(d){return [d.State,d.total];});

    var stTerm = d3.select(id).append("text").text(sF[0][0]).attr('class','stTerm');
        vec = d3.select(id).append("text").text('>>').attr('class','vec');
        enTerm = d3.select(id).append("text").text(sF[sF.length - 1][0]).attr('class','enTerm');
        team = d3.select(id).append("text").text("").attr('class','team');
        leg= legend(tF),  // create the legend.
        pC = pieChart(tF), // create the pie-chart.
        hG = histoGram(sF); // create the histogram.
}


var freqData=[];
var ajaxSending = false;

function go_ajax(){
try{
   if(!ajaxSending){
   ajaxSending = true;
   $('#dashboard').empty();
   dispLoading("Loading...");
   $.ajax({
         'url':$('form#surprise_fm').attr('action'),
         'type':'POST',
         'data':{
            'from_time':$('#from_time').val(),
            'to_time':$('#to_time').val(),
            'frequency':$("input[name='frequency']:checked").val(),
          },
         'dataType':'json',
         'success':function(response){  // 通信が成功したら動く処理で、引数には返ってきたレスポンスが入る
            freqData = response
                 console.log('SUCCESS!さいしょ');
                 freqData = response
             },
         'complete': function(jqXHR, statusText){
            ajaxSending = false;
            removeLoading();
            dashboard('#dashboard',freqData);
            },
         });
         return false;
   }else{
   }
}catch(e){
  ajaxSending = false;
}
}


$(document).ready(function(){
go_ajax();
});


console.log("ページ読み込んだんちゃう？")
$(document).ready(function(){
   console.log("jsはじまったんちゃう？")



   $('#surprise_fm').submit(function() {  // ボタンクリックでAJAX
      go_ajax()
      return false;
    });

    $( 'input[name="frequency"]:radio' ).change( function() {
      go_ajax()
      return false;
    });

});

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
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});