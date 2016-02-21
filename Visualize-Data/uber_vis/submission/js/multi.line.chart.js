/* d3 code to create multi line visualization for 
average weekday and average weekend surge prices */

// declare width & height of vis on page and margin around vis
var margin_c1 = {top: 20, right: 80, bottom: 30, left: 50},
    width_c1 = 950 - margin_c1.left - margin_c1.right,
    height_c1 = 360 - margin_c1.top - margin_c1.bottom;

// declare function to parse x-axis date
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// declare x-axis scale (we will delcare domain after we import data)
var x = d3.time.scale()
    .range([0, width_c1]);

// declare y-axis scale
var y = d3.scale.linear()
    .range([height_c1, 0]);

/*declare colors to be used for lines
probably don't need 10 color scale since only 2 lines
but if we add more lines we'll have it */
var color = d3.scale.category10();

// delcare x-axis, its position, and the tick format
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(d3.time.format("%I %p"));

// declate y-axis and its position
var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

// declare line and its type -- step chart is appropriate for data
// also declare what coordinate from the data will be used
var line = d3.svg.line()
    .interpolate("step-after")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.surge); });

// declare where the chart will be on the html page and its width/height/margin attributes
var chart1 = d3.select("#linechart").append("svg")
    .attr("width", width_c1 + margin_c1.left + margin_c1.right)
    .attr("height", height_c1 + margin_c1.top + margin_c1.bottom)
  .append("g")
    .attr("transform", "translate(" + margin_c1.left + "," + margin_c1.top + ")");

// now the magic begins -- import your data and create the chart
d3.csv("data/multilinedata.csv", function(error, data) {

  // if we can import data, throw an error
  if (error) throw error;

  // now that we have data we can declare domain (input) for colors
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "datetime"; }));

  // loop through rows of data and format the datetime as specified above
  data.forEach(function(d) {
    d.datetime = parseDate(d.datetime);
  });

  // this is what a sample data point now loos like
  // note that we don't care about Jan 01 2001 bc we'll format axis with only time of day
  // datetime: Mon Jan 01 2001 00:00:00 GMT-0500 (EST)
  // weekday: "1"
  // weekend: "1.2"

  // map the colors to either weekday or weekend
  var weekparts = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.datetime, surge: +d[name]};
      })
    };
  });

  // now we have 2 objects -- a weekday object and a weekend object
  // each of these objects have many arrays of data points representing datetime and surge rate

  // declare domain (or input values) for x-axis
  x.domain(d3.extent(data, function(d) { return d.datetime; }));
  
  // delare domain (or input values) for y-axis
  y.domain([
    d3.min(weekparts, function(c) { return d3.min(c.values, function(v) { return v.surge; }); }),
    d3.max(weekparts, function(c) { return d3.max(c.values, function(v) { return v.surge; }); })
  ]);
  
  // draw the x-axis
  chart1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height_c1 + ")")
      .call(xAxis);

  // draw the y-axis and add a axis title
  chart1.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Surge Rate");

  // now we start to draw the lines accoring to our formatted 'weekparts' data obects
  var part = chart1.selectAll(".part")
      .data(weekparts)
    .enter().append("g")
      .attr("class", "part");
  
  // this block of code will draw the lines
  part.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .attr("data-legend",function(d) { return d.name})
      .style("stroke", function(d) { return color(d.name); });
  
  // this block of code will add labels to the end of each line
  part.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.surge) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });

  // adding an additional legend to make it obvious which line is weekday and which is weekend
  // I used gist from Ziggy Jonson to add this second legend
  legend = chart1.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend)

});