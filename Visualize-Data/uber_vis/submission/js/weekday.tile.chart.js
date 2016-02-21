/* d3 code to create tile chart for average 
hourly weekday surge prices */

// start off with lots of definitions
/* width and height will define size of box on html page and margin 
will tell how far inside box edges visualization should be drawn */
/* color are defined here (as well as how many levels in the heat map 
we want... a fine exercise is dropping buckets to 2 as see what a
surge / not surge heat map looks like ) */
/* the days and hours we want to use are also defined here as well as the
original weekday dataset and normalized one */
var margin_c2 = { top: 50, right: 0, bottom: 45, left: 30 },
    width_c2 = 960 - margin_c2.left - margin_c2.right,
    height_c2 = 315 - margin_c2.top - margin_c2.bottom,
    gridSize_c2 = Math.floor(width_c2 / 24),
    legendElementWidth_c2 = gridSize_c2*2,
    buckets_c2 = 9,
    colors_c2 = ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b'], // thanks http://colorbrewer2.org/
    days_c2 = ["Mo", "Tu", "We", "Th", "Fr"],
    times_c2 = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];
    datasets_c2 = ["data/wkdaydata1.tsv", "data/wkdaydata2.tsv"];

// setup the svg in which the visualization will live
var chart2 = d3.select("#weekdaytilechart").append("svg")
    .attr("width", width_c2 + margin_c2.left + margin_c2.right)
    .attr("height", height_c2 + margin_c2.top + margin_c2.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_c2.left + "," + margin_c2.top + ")");

// before we bring in the tiles, we bring in the labels -- this block is for the day of week
var dayLabels_c2 = chart2.selectAll(".dayLabel")
    .data(days_c2)
    .enter().append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return i * gridSize_c2; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + gridSize_c2 / 1.5 + ")")
      .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

// before we bring in the tiles, we bring in the labels -- this block is for the time of day
var timeLabels_c2 = chart2.selectAll(".timeLabel")
    .data(times_c2)
    .enter().append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize_c2; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize_c2 / 2 + ", -6)")
      .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

// so if you put a debugger here and tried to load the chart, you would
// see the labels be drawn.. but no tiles yet. Perry Cool. 

// this function allows us to load the data and draw the tile map
// note that it uses the term card when referring to tiles
var heatmapChart_c2 = function(tsvFile) {
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
    // the data at this point is an array container 120 objects 
    // each with a day, hour, and surge value

    // based on the range of surge values we need to map the colors
    // defined above to these values to create a colorScale
    var colorScale_c2 = d3.scale.quantile()
        .domain([1, d3.max(data, function (d) { return d.value; })])
        .range(colors_c2);
    
    // now we draw the tiles based on the same data
    var cards_c2 = chart2.selectAll(".hour")
        .data(data, function(d) {return d.day+':'+d.hour;});

    // the enter helps us really draw the tiles into the html
    // other attibutes are also defined here
    cards_c2.enter().append("rect")
        .attr("x", function(d) { return (d.hour - 1) * gridSize_c2; })
        .attr("y", function(d) { return (d.day - 1) * gridSize_c2; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("class", "hour bordered")
        .attr("width", gridSize_c2)
        .attr("height", gridSize_c2)
        .style("fill", colors_c2[0]);

    // all tiles are first colored #f7fbff and then fade into their
    // respective heat map color
    cards_c2.transition().duration(1000)
        // use the same color scale each time
        .style("fill", function(d) { return colorScale_c2(d.value); });

    // the next three blocks define what happends with a button is clicked
    // indicating we want to see a new dataset    
    // this line removes all the tiles before redrawing new ones
    cards_c2.exit().remove();

    // the bext few blocks of code draws and labels the legend at the bottom
    // as expected the legend if based on the input data as well as the color
    // buckets we defined above as well as the color scale that maps
    // our input data to the color buckets
    var legend_c2 = chart2.selectAll(".legend")
        .data([1].concat(colorScale_c2.quantiles()), function(d) { return d; });

    // this block draws the group in which the legend will live on the html page
    legend_c2.enter().append("g")
        .attr("class", "legend");

    // notice here that the style -- fill is based on the number of color buckets 
    // that we defined all the way at the top and then transformed into a range
    // from the input data
    legend_c2.append("rect")
      .attr("x", function(d, i) { return legendElementWidth_c2 * i; })
      .attr("y", height_c2)
      .attr("width", legendElementWidth_c2)
      .attr("height", gridSize_c2 / 2)
      .style("fill", function(d, i) { return colors_c2[i]; });
    
    // last thing is to add lables to the legend
    legend_c2.append("text")
      .attr("class", "mono")
      .text(function(d) { return "≥ " + +d.toFixed(2); })
      .attr("x", function(d, i) { return legendElementWidth_c2 * i; })
      .attr("y", height_c2 + gridSize_c2);

    // this line removes the legend before redrawing new ones
    legend_c2.exit().remove();

  });  
};

// call the heatmap function to draw the tilechart
// it will first use dataset 1 (original)
heatmapChart_c2(datasets_c2[0]);

// this block selects html div with id of dataset-picker and creates buttons
// for each of our datasets
var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
  .data(datasets_c2);

/* this block draws the datepicker and tells it to draw the tile chart with
the dataset on the button that was clicked on */
datasetpicker.enter()
  .append("input")
  .attr("value", function(d){ if (d === 'data/wkdaydata1.tsv') {
                                return 'Original Data' }
                              else {
                                return 'Normalized Data'
                              }})
  .attr("type", "button")
  .attr("class", "dataset-button")
  .on("click", function(d) {
    heatmapChart_c2(d);
  });