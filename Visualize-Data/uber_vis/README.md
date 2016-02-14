Uber Surge Pricing Behavior Visualization
=========================================

Summary
-------
Mobile ride hail company Uber ensures reliability of service when demand cannot be met by increasing prices instantly in the form of a surge ratio. Utilizing only a weeks worth of surge data, the following visualizations reveal simultaneous stability and volatiltiy in surge price behavior. The data was collected from the Uber API in 5 minute increments for a ride between New York City's Penn Station and New York University in Greenwich Village.

[View d3.js Visualization](https://rawgit.com/FrankRuns/Udacity/master/Visualize-Data/uber_vis/index.html)

Files
-----
* index.html -- html code
* libraries -- includes d3 & d3.legend libraries
* data -- includes data files
* munging -- includes script for collecting data and ipython & r files for exploring & cleaning the data
* js -- holds script files for visualizations
* css -- holds style file for html and visualizations

Design
------
When I originally envisioned this on my whiteboard @ home, I knew I wanted to plot a step chart by day of the week over a 24-hour period to show me differences in surge price behavior by day (at this stage I did collect feedback from my companion who agreed it was a good go forward). My co-workers were convinced that surge price behavior was concise and stable meaning once surge pricing is in effect, it stays at that level for a predetermined period. I wasn't convinced -- I wanted data. 

After writing a script to collect the data from the Uber API, doing the data cleaning in r, and creating the plot I mention above, it came out a bit chaotic with little message.

Grouping the data into weekday and weekend buckets helped reveal some patterns, but also showed that surge pricing is definitiely not stable as my colleagues had believed. 

Originally, I only had the weekday step chart when I started to collect feedback. Repeatedly, people asked if there was an alternative was to view the data by day of week. So I started roaming the d3.js examples page and found this amazing tile heatmap showing hour of day and day of week which I replicated in my final charts.

I do believe I should have collected feedback earlier in the development cycle. I only asked for feedback after I devoted many hours to creating this and arriving at what I thought should be a final project. I did make some tweaks and altered the color scheme of the heat map per the 'most helpful commentary' below. 

Feedback
--------
General Commentary
* Very cool
* I didn't know you could do this

Questions
* Is there a way to view the data by day of week?
* What is the applications for this data?
* I don't understand why there is a weekend spike at 2PM...

Most Helpful Commentary
I am unfamiliar with Greenwich Village, but your weekend 2 pm spike could be explained by tourism ie..., If I came to visit NYC for the first time, would it be a place you guys would take me to see. Also, if there are a lot of clubs/bars/restaurants for people to hang out at. That would explain the weekend 6 pm spike. Young folks heading over to have fun and older people like me heading home. If you extrapolate further, people heading home from Greenwich Village would explain the 4 spikes after 9 pm on the weekends. Is that the type of feedback Frank is looking for or am I totally off base ? The recognition of a weather event that created an unusual spike is brillant. Most people never put the two togther. Weather will always affect all forms of travel.

The only other thing I would suggest is use consistent color coding between charts. He used blue for weekdays, in the second chart stay with shades of blue. Starting with a pale green confuses some people. Even though the color key is directly below that chart. And I would go with shades of orange for Saturday and Sunday since that is the color for the first chart and it will make it easier for people to distinguish between weekend and weekday. It will mean the need for an additional color key. I know the days are marked to the left but color coding it this way will create instant recognition/correlation between graphs.

Resources
---------
* [Uber for Developers](https://developer.uber.com/)
* [NBC news report on January 2016 NYC blizzard](http://www.nbcnewyork.com/news/local/NYC-2016-Blizzard-Record-Snowfall-Historic-Snowstorm-Shuts-Down-Transit-Travel-Ban-Plows-366340361.html)
* [M. Bostock multi-series line chart example](http://bl.ocks.org/mbostock/3884955)
* [Z. Jonsson d3 legend generator](https://gist.github.com/ZJONSSON/3918369)
* [TJ Decke d3 tile chart example](http://bl.ocks.org/tjdecke/5558084)
* [Udacity](https://www.udacity.com)
