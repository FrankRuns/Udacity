var margin_c1 = {top: 20, right: 80, bottom: 30, left: 50},
    // width_c1 = 864 - margin_c1.left - margin_c1.right,
    // height_c1 = 450 - margin_c1.top - margin_c1.bottom;
    width_c1 = 950 - margin_c1.left - margin_c1.right,
    height_c1 = 360 - margin_c1.top - margin_c1.bottom;

var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

var x = d3.time.scale()
    .range([0, width_c1]);

var y = d3.scale.linear()
    .range([height_c1, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(d3.time.format("%I %p"));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("step-after")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.surge); });

var chart1 = d3.select("#linechart").append("svg")
    .attr("width", width_c1 + margin_c1.left + margin_c1.right)
    .attr("height", height_c1 + margin_c1.top + margin_c1.bottom)
  .append("g")
    .attr("transform", "translate(" + margin_c1.left + "," + margin_c1.top + ")");

d3.csv("data/multilinedata.csv", function(error, data) {

  if (error) throw error;

  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "datetime"; }));

  data.forEach(function(d) {
    d.datetime = parseDate(d.datetime);
  });

  var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.datetime, surge: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.datetime; }));
  
  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.surge; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.surge; }); })
  ]);
  
  chart1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height_c1 + ")")
      .call(xAxis);

  chart1.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Surge Rate");

  var city = chart1.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");
  
  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .attr("data-legend",function(d) { return d.name})
      .style("stroke", function(d) { return color(d.name); });
  
  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.surge) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });

  legend = chart1.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend)

});