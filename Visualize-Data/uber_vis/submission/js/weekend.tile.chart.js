/* d3 code to create tile chart for average 
hourly weekend surge prices. This is very
similar to weekday tile heatmap, but it's only
for Sat/Sun and there is no dataset change */

// start off with lots of definitions
/* width and height will define size of box on html page and margin 
will tell how far inside box edges visualization should be drawn */
/* color are defined here (as well as how many levels in the heat map 
we want... a fine exercise is dropping buckets to 2 as see what a
surge / not surge heat map looks like ) */
/* the days and hours we want to use are also defined here as well as the
original weekend dataset only*/
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

// setup the svg in which the visualization will live
var chart3 = d3.select("#weekendtilechart").append("svg")
    .attr("width", width_c3 + margin_c3.left + margin_c3.right)
    .attr("height", height_c3 + margin_c3.top + margin_c3.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_c3.left + "," + margin_c3.top + ")");

// before we bring in the tiles, we bring in the labels -- this block is for the day of weekend
var dayLabels_c3 = chart3.selectAll(".dayLabel")
    .data(days_c3)
    .enter().append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return i * gridSize_c3; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + gridSize_c3 / 1.5 + ")")
      .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

// before we bring in the tiles, we bring in the labels -- this block is for the time of day
var timeLabels_c3 = chart3.selectAll(".timeLabel")
    .data(times_c3)
    .enter().append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize_c3; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize_c3 / 2 + ", -6)")
      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

// this function allows us to load the data and draw the tile map
// note that it uses the term card when referring to tiles
var heatmapChart_c3 = function(tsvFile) {
  d3.tsv(tsvFile,
  function(d) {
    return {
      // this makes our input string values into numbers
      day: +d.day,
      hour: +d.hour,
      value: +d.value
    };
  },
  function(error, data) {
    // the data at this point is an array container 48 objects
    // totally logical (24 hours in day, 2 days in weekend (unfortunately))
    // each with a day, hour, and surge value

    // based on the range of surge values we need to map the colors
    // defined above to these values to create a colorScale
    var colorScale_c3 = d3.scale.quantile()
        .domain([1, d3.max(data, function (d) { return d.value; })])
        .range(colors_c3);
    
    // now we draw the tiles based on the same data
    var cards_c3 = chart3.selectAll(".hour")
        .data(data, function(d) {return d.day+':'+d.hour;});

    // the enter helps us really draw the tiles into the html
    // other attibutes are also defined here
    cards_c3.enter().append("rect")
        .attr("x", function(d) { return (d.hour - 1) * gridSize_c3; })
        .attr("y", function(d) { return (d.day - 6) * gridSize_c3; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize_c3)
        .attr("height", gridSize_c3)
        .style("fill", colors_c3[0]);

    // all tiles are first colored #fff5eb and then fade into their
    // respective heat map color
    cards_c3.transition().duration(1000)
        .style("fill", function(d) { return colorScale_c3(d.value); });

    // the bext few blocks of code draws and labels the legend at the bottom
    // as expected the legend if based on the input data as well as the color
    // buckets we defined above as well as the color scale that maps
    // our input data to the color buckets
    var legend_c3 = chart3.selectAll(".legend")
        .data([1].concat(colorScale_c3.quantiles()), function(d) { return d; });

    // this block draws the group in which the legend will live on the html page
    legend_c3.enter().append("g")
        .attr("class", "legend");

    // notice here that the style -- fill is based on the number of color buckets 
    // that we defined all the way at the top and then transformed into a range
    // from the input data
    legend_c3.append("rect")
      .attr("x", function(d, i) { return legendElementWidth_c3 * i; })
      .attr("y", height_c3)
      .attr("width", legendElementWidth_c3)
      .attr("height", gridSize_c3 / 2)
      .style("fill", function(d, i) { return colors_c3[i]; });
    
    // last thing is to add lables to the legend
    legend_c3.append("text")
      .attr("class", "mono")
      .text(function(d) { return "≥ " + +d.toFixed(2); })
      .attr("x", function(d, i) { return legendElementWidth_c3 * i; })
      .attr("y", height_c3 + gridSize_c3);

  });  
};

// finally call the heatmap function to draw the chart
heatmapChart_c3(datasets_c3[0]);