var margin_c3 = { top: 50, right: 0, bottom: 45, left: 30 },
    width_c3 = 960 - margin_c3.left - margin_c3.right,
    height_c3 = 200 - margin_c3.top - margin_c3.bottom,
    gridSize_c3 = Math.floor(width_c3 / 24),
    legendElementWidth_c3 = gridSize_c3*2,
    buckets_c3 = 9,
    colors_c3 = ['#fff5eb','#fee6ce','#fdd0a2','#fdae6b','#fd8d3c','#f16913','#d94801','#a63603','#7f2704'], // thanks http://colorbrewer2.org/
    days_c3 = ["Sa", "Su"],
    times_c3 = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];
    datasets_c3 = ["data/wkenddata.tsv"];

var chart3 = d3.select("#weekendtilechart").append("svg")
    .attr("width", width_c3 + margin_c3.left + margin_c3.right)
    .attr("height", height_c3 + margin_c3.top + margin_c3.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_c3.left + "," + margin_c3.top + ")");

var dayLabels_c3 = chart3.selectAll(".dayLabel")
    .data(days_c3)
    .enter().append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return i * gridSize_c3; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + gridSize_c3 / 1.5 + ")")
      .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

var timeLabels_c3 = chart3.selectAll(".timeLabel")
    .data(times_c3)
    .enter().append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize_c3; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize_c3 / 2 + ", -6)")
      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

var heatmapChart_c3 = function(tsvFile) {
  d3.tsv(tsvFile,
  function(d) {
    return {
      day: +d.day,
      hour: +d.hour,
      value: +d.value
    };
  },
  function(error, data) {
    var colorScale_c3 = d3.scale.quantile()
        .domain([1, d3.max(data, function (d) { return d.value; })])
        .range(colors_c3);
    
    var cards_c3 = chart3.selectAll(".hour")
        .data(data, function(d) {return d.day+':'+d.hour;});

    cards_c3.append("title");

    cards_c3.enter().append("rect")
        .attr("x", function(d) { return (d.hour - 1) * gridSize_c3; })
        .attr("y", function(d) { return (d.day - 6) * gridSize_c3; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize_c3)
        .attr("height", gridSize_c3)
        .style("fill", colors_c3[0]);

    cards_c3.transition().duration(1000)
        .style("fill", function(d) { return colorScale_c3(d.value); });

    cards_c3.select("title").text(function(d) { return d.value; });
    
    cards_c3.exit().remove();

    var legend_c3 = chart3.selectAll(".legend")
        .data([1].concat(colorScale_c3.quantiles()), function(d) { return d; });

    legend_c3.enter().append("g")
        .attr("class", "legend");

    legend_c3.append("rect")
      .attr("x", function(d, i) { return legendElementWidth_c3 * i; })
      .attr("y", height_c3)
      .attr("width", legendElementWidth_c3)
      .attr("height", gridSize_c3 / 2)
      .style("fill", function(d, i) { return colors_c3[i]; });
    
    legend_c3.append("text")
      .attr("class", "mono")
      .text(function(d) { return "≥ " + +d.toFixed(2); })
      .attr("x", function(d, i) { return legendElementWidth_c3 * i; })
      .attr("y", height_c3 + gridSize_c3);

    legend_c3.exit().remove();

  });  
};

heatmapChart_c3(datasets_c3[0]);

// var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
//   .data(datasets);

// datasetpicker.enter()
//   .append("input")
//   .attr("value", function(d){ return "Dataset " + d })
//   .attr("type", "button")
//   .attr("class", "dataset-button")
//   .on("click", function(d) {
//     heatmapChart(d);
//   });