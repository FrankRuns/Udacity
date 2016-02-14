var margin_c2 = { top: 50, right: 0, bottom: 160, left: 30 },
    width_c2 = 960 - margin_c2.left - margin_c2.right,
    height_c2 = 430 - margin_c2.top - margin_c2.bottom,
    gridSize_c2 = Math.floor(width_c2 / 24),
    legendElementWidth_c2 = gridSize_c2*2,
    buckets_c2 = 9,
    colors_c2 = ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b'], // thanks http://colorbrewer2.org/
    days_c2 = ["Mo", "Tu", "We", "Th", "Fr"],
    times_c2 = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];
    datasets_c2 = ["data/wkdaydata1.tsv", "data/wkdaydata2.tsv"];

var chart2 = d3.select("#weekdaytilechart").append("svg")
    .attr("width", width_c2 + margin_c2.left + margin_c2.right)
    .attr("height", height_c2 + margin_c2.top + margin_c2.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_c2.left + "," + margin_c2.top + ")");

var dayLabels_c2 = chart2.selectAll(".dayLabel")
    .data(days_c2)
    .enter().append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return i * gridSize_c2; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + gridSize_c2 / 1.5 + ")")
      .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

var timeLabels_c2 = chart2.selectAll(".timeLabel")
    .data(times_c2)
    .enter().append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize_c2; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize_c2 / 2 + ", -6)")
      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

var heatmapChart_c2 = function(tsvFile) {
  d3.tsv(tsvFile,
  function(d) {
    return {
      day: +d.day,
      hour: +d.hour,
      value: +d.value
    };
  },
  function(error, data) {
    var colorScale_c2 = d3.scale.quantile()
        .domain([1, d3.max(data, function (d) { return d.value; })])
        .range(colors_c2);
    
    var cards_c2 = chart2.selectAll(".hour")
        .data(data, function(d) {return d.day+':'+d.hour;});

    cards_c2.append("title");

    cards_c2.enter().append("rect")
        .attr("x", function(d) { return (d.hour - 1) * gridSize_c2; })
        .attr("y", function(d) { return (d.day - 1) * gridSize_c2; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize_c2)
        .attr("height", gridSize_c2)
        .style("fill", colors_c2[0]);

    cards_c2.transition().duration(1000)
        .style("fill", function(d) { return colorScale_c2(d.value); });

    cards_c2.select("title").text(function(d) { return d.value; });
    
    cards_c2.exit().remove();

    var legend_c2 = chart2.selectAll(".legend")
        .data([1].concat(colorScale_c2.quantiles()), function(d) { return d; });

    legend_c2.enter().append("g")
        .attr("class", "legend");

    legend_c2.append("rect")
      .attr("x", function(d, i) { return legendElementWidth_c2 * i; })
      .attr("y", height_c2)
      .attr("width", legendElementWidth_c2)
      .attr("height", gridSize_c2 / 2)
      .style("fill", function(d, i) { return colors_c2[i]; });
    
    legend_c2.append("text")
      .attr("class", "mono")
      .text(function(d) { return "≥ " + +d.toFixed(2); })
      .attr("x", function(d, i) { return legendElementWidth_c2 * i; })
      .attr("y", height_c2 + gridSize_c2);

    legend_c2.exit().remove();

  });  
};

heatmapChart_c2(datasets_c2[0]);

var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
  .data(datasets_c2);

datasetpicker.enter()
  .append("input")
  .attr("value", function(d){ return "Dataset " + d })
  .attr("type", "button")
  .attr("class", "dataset-button")
  .on("click", function(d) {
    heatmapChart_c2(d);
  });