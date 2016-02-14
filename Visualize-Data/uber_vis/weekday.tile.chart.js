var margin_c2 = { top: 50, right: 0, bottom: 100, left: 30 },
    width_c2 = 960 - margin_c2.left - margin_c2.right,
    height_c2 = 430 - margin_c2.top - margin_c2.bottom,
    gridSize = Math.floor(width_c2 / 24),
    legendElementWidth = gridSize*2,
    buckets = 9,
    colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
    times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];
    datasets = ["data/data.tsv", "data/data2.tsv"];

var chart2 = d3.select("#weekdaytilechart").append("svg")
    .attr("width", width_c2 + margin_c2.left + margin_c2.right)
    .attr("height", height_c2 + margin_c2.top + margin_c2.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_c2.left + "," + margin_c2.top + ")");

var dayLabels = chart2.selectAll(".dayLabel")
    .data(days)
    .enter().append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return i * gridSize; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
      .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

var timeLabels = chart2.selectAll(".timeLabel")
    .data(times)
    .enter().append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize / 2 + ", -6)")
      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

var heatmapChart = function(tsvFile) {
  d3.tsv(tsvFile,
  function(d) {
    return {
      day: +d.day,
      hour: +d.hour,
      value: +d.value
    };
  },
  function(error, data) {
    var colorScale = d3.scale.quantile()
        .domain([1, d3.max(data, function (d) { return d.value; })])
        .range(colors);
    
    var cards = chart2.selectAll(".hour")
        .data(data, function(d) {return d.day+':'+d.hour;});

    cards.append("title");

    cards.enter().append("rect")
        .attr("x", function(d) { return (d.hour - 1) * gridSize; })
        .attr("y", function(d) { return (d.day - 1) * gridSize; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("fill", colors[0]);

    cards.transition().duration(1000)
        .style("fill", function(d) { return colorScale(d.value); });

    cards.select("title").text(function(d) { return d.value; });
    
    cards.exit().remove();

    var legend = chart2.selectAll(".legend")
        .data([1].concat(colorScale.quantiles()), function(d) { return d; });

    legend.enter().append("g")
        .attr("class", "legend");

    legend.append("rect")
      .attr("x", function(d, i) { return legendElementWidth * i; })
      .attr("y", height_c2)
      .attr("width", legendElementWidth)
      .attr("height", gridSize / 2)
      .style("fill", function(d, i) { return colors[i]; });
    
    legend.append("text")
      .attr("class", "mono")
      .text(function(d) { return "≥ " + +d.toFixed(2); })
      .attr("x", function(d, i) { return legendElementWidth * i; })
      .attr("y", height_c2 + gridSize);

    legend.exit().remove();

  });  
};

heatmapChart(datasets[0]);

var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
  .data(datasets);

datasetpicker.enter()
  .append("input")
  .attr("value", function(d){ return "Dataset " + d })
  .attr("type", "button")
  .attr("class", "dataset-button")
  .on("click", function(d) {
    heatmapChart(d);
  });