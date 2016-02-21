Uber Surge Pricing Behavior Visualization
=========================================

Summary
-------
Mobile ride hail company Uber ensures reliability of service when demand cannot be met by increasing prices instantly in the form of a surge ratio. Utilizing only a weeks worth of surge data, the following visualizations reveal simultaneous stability and volatiltiy in surge price behavior. The data was collected from the Uber API in 5 minute increments for a ride between New York City's Penn Station and New York University in Greenwich Village.

The first graphic shows us 2 things. First, surge pricing is volatile -- changing every few minutes. At the same time, we can see consistent surge trends during the morning and evening commute on weekdays and again in the late afternoon / evenings on the weekend. 

The later graphics break out surge rates by day and hour showing that this particular Monday had a very high sruge rate compared to other days of the week -- I attribute this to the weekend blizzard that happened the day before. 

[View d3.js Visualization](https://rawgit.com/FrankRuns/Udacity/master/Visualize-Data/uber_vis/index.html)

Files
-----
* rawdata -- raw data from uber api
* munging -- includes script for collecting data and ipython & r files for exploring & cleaning the data
* submission
	* index.html -- html code
	* libraries -- includes d3 & d3.legend libraries
	* data -- includes data files
	* js -- holds script files for visualizations
	* css -- holds style file for html and visualizations

Design
------
My co-workers were convinced that surge price behavior was concise and stable meaning once surge pricing is in effect, it stays at that level for a predetermined period. I wasn't convinced -- I wanted data. When I originally envisioned this on my whiteboard @ home, I knew I wanted to plot a step chart by day of the week over a 24-hour period to show me differences in surge price behavior by day. I drew it several times, then I went to r for some quick iterations (one of those pasted directly below). At this point, I collected feedback from my wife (Feedback #1).

![first iteration]['/submission/img/surgeByDate.png']

After writing a script to collect the data from the Uber API, doing the data cleaning in r, and creating the plot I mention above, it came out a bit chaotic with little message.

Based on Feedback #1 and a bit more thinking, grouping the data into weekday and weekend buckets (by average surge rate) helped reveal some patterns, but also showed that surge pricing is definitiely not stable as my colleagues had believed. 

Originally, I only had the weekday step chart when I started to collect further feedback (Feedback #2). In the feedback below I was asked if there was an alternative was to view the data by day of week. So I started roaming the d3.js examples page and found this amazing tile heatmap showing hour of day and day of week which I replicated in my final charts. I had to replicate it. I did and added it to the multiline chart... it was now becoming a story. 

At this point, I went after Feedback #3 and was able to adjust colors and story description accordingly to arrive at the final draft. 

Feedback
--------
Feedback #1
* This graphic looks like it contains a lot of great information, unfortunately I found the color usage a little overwhelming. It's difficult to distinguish the days of the week or really take away something valuable from the visualization quickly. I think it might be interesting to see the average for monday-friday and then the average for saturday-sunday instead. 

Feedback #2
* What do I notice? It's obvious that weekdays have a big hump in the morning and pretty much all days have a hump in the evening. I also see that surge pricing jumps around more than I expected it to -- can drivers really respond to jumps that are this quick? I don't understand why some jumps seem random, however, that's probably not a graphic question. I saw your first graphic and I know it was messy, but I think I'd like to see surge pricing rate for each day. If you've used ggplot in r, you could try to use facet wrap or grid ... one of those ... to see if there are any significant changes from one day of the week to the next.  


Feedback #3
* I am unfamiliar with Greenwich Village, but your weekend 2 pm spike could be explained by tourism ie..., If I came to visit NYC for the first time, would it be a place you guys would take me to see. Also, if there are a lot of clubs/bars/restaurants for people to hang out at. That would explain the weekend 6 pm spike. Young folks heading over to have fun and older people like me heading home. If you extrapolate further, people heading home from Greenwich Village would explain the 4 spikes after 9 pm on the weekends. Is that the type of feedback Frank is looking for or am I totally off base ? The recognition of a weather event that created an unusual spike is brillant. Most people never put the two togther. Weather will always affect all forms of travel. The only other thing I would suggest is use consistent color coding between charts. He used blue for weekdays, in the second chart stay with shades of blue. Starting with a pale green confuses some people. Even though the color key is directly below that chart. And I would go with shades of orange for Saturday and Sunday since that is the color for the first chart and it will make it easier for people to distinguish between weekend and weekday. It will mean the need for an additional color key. I know the days are marked to the left but color coding it this way will create instant recognition/correlation between graphs.

Resources
---------
* [Uber for Developers](https://developer.uber.com/)
* [NBC news report on January 2016 NYC blizzard](http://www.nbcnewyork.com/news/local/NYC-2016-Blizzard-Record-Snowfall-Historic-Snowstorm-Shuts-Down-Transit-Travel-Ban-Plows-366340361.html)
* [M. Bostock multi-series line chart example](http://bl.ocks.org/mbostock/3884955)
* [Z. Jonsson d3 legend generator](https://gist.github.com/ZJONSSON/3918369)
* [TJ Decke d3 tile chart example](http://bl.ocks.org/tjdecke/5558084)
* [Udacity](https://www.udacity.com)
