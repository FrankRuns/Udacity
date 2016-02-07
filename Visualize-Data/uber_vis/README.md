Uber Surge Pricing Behavior Visualization
=========================================

Summary
-------
Mobile ride hail company Uber ensures reliability of service when demand cannot be met by increasing prices instantly in the form of a surge ratio. Utilizing only a weeks worth of surge data, the following visualizations reveal simultaneous stability and volatiltiy in surge price behavior. The data was collected from the Uber API in 5 minute increments for a ride between New York City's Penn Station and New York University in Greenwich Village.

Design
------
When I originally envisioned this on my whiteboard @ home, I knew I wanted to plot a step chart by day of the week over a 24-hour period to show me differences in surge price behavior by day. My co-workers were convinced that surge price behavior was concise and stable meaning once surge pricing is in effect, it stays at that level for a predetermined period. I wasn't convinced -- I wanted data. 

After writing a script to collect the data from the Uber API, doing the data cleaning in r, and creating the plot I mention above, it came out a bit chaotic with little message.

Grouping the data into weekday and weekend buckets helped reveal some patterns, but also showed that surge pricing is definitiely not stable as my colleagues had believed. 


Feedback
--------


Resources
---------
* [Uber for Developers](https://developer.uber.com/)
* [NBC news report on January 2016 NYC blizzard](http://www.nbcnewyork.com/news/local/NYC-2016-Blizzard-Record-Snowfall-Historic-Snowstorm-Shuts-Down-Transit-Travel-Ban-Plows-366340361.html)
* [M. Bostock multi-series line chart example](http://bl.ocks.org/mbostock/3884955)
* [Z. Jonsson d3 legend generator](https://gist.github.com/ZJONSSON/3918369)
* [TJ Decke d3 tile chart example](http://bl.ocks.org/tjdecke/5558084)
* [Udacity](https://www.udacity.com)
