setwd("/Users/frankcorrigan/Desktop")
library(ggplot2)
library(dplyr)
library(reshape2)

# read data in
data <- read.csv('surge.csv')

# create list to 'correct' 5 minute mishap
start <- rep(seq(0,55,5),167)
end <- c(0, 5, 10, 15)
data$new_moh <- c(start, end)
data$min_difference <- data$minuteofhour - data$new_moh
data$new_mod = as.integer((data$hourofday * 60) + data$new_moh)

# creat new datetime object with new minuteofday as well as hour and minute column for graphing axes
data$datetime <- ISOdatetime(2015, 1, data$dayofmonth, data$hourofday, data$new_moh, 0)
data$hm <- format(data$datetime, format = "%H:%M")

# Create weekend varaiable to identify weekends
data$weekend <- ifelse(data$dayofweek > 4, "Weekend", "Weekday")

# take on what needed and plot one line for each day
fdata <- select(data, surge, dayofweek, new_mod, datetime, hm)
ggplot(data=fdata, aes(x=new_mod, y=surge, colour=factor(dayofweek))) + 
  geom_step() +
  scale_x_discrete(labels = fdata$hm)

# group by average surge per minute
avgbymin <- fdata %>% group_by(new_mod) %>% summarize(avgsurge = mean(surge))
ggplot(data=avgbymin, aes(x=new_mod, y=avgsurge)) + 
  geom_step()

# group by weekend / non-weekend
fdata$weekend <- ifelse(fdata$dayofweek > 4, "Weekend", "Weekday")
ffdata <- select(fdata, surge, new_mod, weekend, datetime)

# create new df that has avg surge for weekday / non-weekday and plot it
weekend <- ffdata %>% group_by(weekend, new_minuteofday) %>% summarize(avgsurge = mean(surge))
ggplot(data=weekend, aes(x=new_minuteofday, y=avgsurge, colour=factor(weekend))) + 
  geom_step()

# ----------

library(scales)
data$testdate <- factor(as.Date(data$datetime))
data$testtime <- as.POSIXct(sprintf('%s %s:%s', Sys.Date(), format(data$datetime, '%H:%M'), '00'))
p <- ggplot(data, aes(x=testtime, y=surge, group=testdate, color=testdate)) + geom_step()
p + scale_x_datetime(breaks=date_breaks('1 hour'), labels=date_format('%H:%M')) + theme_light()

# if we want to plot average of weekend versus weekday
# group by testtime and day of weekend boolean ... summarize by mean(surge)
# so your columes will be testtime, weekend, avg surge

wdata <- data %>% select(testtime, weekend, surge) %>% group_by(testtime, weekend) %>% summarize(avgsurge=mean(surge))
p2 <- ggplot(wdata, aes(x=testtime, y=avgsurge, group=weekend, color=weekend)) + geom_step()
p2 + scale_x_datetime(breaks=date_breaks('1 hour'), labels=date_format('%H:%M')) + theme_light()

t <- ggplot(data=data, aes(x=testtime, y=surge, group=weekend, colour=weekend)) + geom_step() + facet_wrap(~testdate)
t + scale_x_datetime(breaks=date_breaks('1 hour'), labels=date_format('%H:%M'))

cdata <- filter(data, testdate != '2015-01-24')
t <- ggplot(data=cdata, aes(x=testtime, y=surge, group=weekend, colour=weekend)) + 
    geom_step() + 
    facet_wrap(~testdate) +
    theme_light()

# -----

setwd("/Users/frankcorrigan/Desktop")
library(ggplot2)
library(dplyr)
library(reshape2)

# read data in
data <- read.csv('surge.csv')

# check to make sure we have consecutive data
c_time <- rev( data$date )
difftime(c_time[1:(length(c_time)-1)] , c_time[2:length(c_time)])
# we didn't get 5 minute intervales exactly, but we more or less have consecutive intervals

# what is the start and end datetime?
sort(data$date)[1]
sort(data$date)[length(data$date)]
# which means you should have how many observations? ...
# on day 1 you have 1PM - midnight ... 11 hours each with 12 observations is 132
# on last day you have until 1PM ... 13 hours each with 12 observations is 156
# on the other 6 days you should have 24 hours each with 12 observations so 1728
# 1728 + 156 + 132 = 2016
nrow(data) # 2008 due to the 5.x intervals

# rename date to datetime
names(data)[2] <- 'datetime'

# creat new datetime object with new minuteofday as well as hour and minute column for graphing axes
# data$datetime <- ISOdatetime(2015, 1, data$dayofmonth, data$hourofday, data$minuteofhour, 0)
data$date <- factor(as.Date(data$datetime))
data$time <- strftime(data$datetime, format="%H:%M:%S")
data$weekend <- ifelse(data$dayofweek > 4, "weekend", "weekday")

# Columns used --- time, surge, weekend
t <- ggplot(data=data, aes(x=time, y=surge, group=weekend, colour=weekend)) + 
  geom_step() + 
  facet_wrap(~date) +
  theme_light()
# ok. the data is good. move forward

# ------

# First thing I want to do is graph one line for each day on top of one another
# Columns used --- time, surge, date
t2 <- ggplot(data=data, aes(x=as.POSIXct(paste("20010101", time), format="%Y%m%d %H:%M:%S"), y=surge, group=date, colour=date)) + 
  geom_step() + 
  theme_light() +
  scale_x_datetime(limits = c(min(as.POSIXct(data$time, format="%Y-%m-%d %H:%M:%S")), max(as.POSIXct(data$time, format="%Y-%m-%d %H:%M:%S"))), minor_breaks=date_breaks("6 hour"), labels=my_format("%H:%M")) +
  labs(x="Hour of Day", y="Surge Rate", title="Late Jan 2016 Uber Surge Rate Between Penn & NYU in 5 Minute Intervals") 

# wdata <- data %>% select(time, weekend, surge) %>% group_by(time, weekend) %>% summarize(avgsurge=mean(surge))
# need to make the time an actual time to format the x axes in chart
# wdata$time <- gsub( ":", "", as.character(wdata$time))
# use arbitrary date... because date won't matter only the time will
# wdata$time_formatted <- as.POSIXct(paste("20010101", wdata$time), format="%Y%m%d %H%M")

# plot average surge by weekday / weekend
# p2 <- ggplot(wdata, aes(x=time_formatted, y=avgsurge, group=weekend, color=weekend)) + geom_step()
my_format <- function (format = "%Y-%m-%d %H:%M:%S") {
  function(x) format(x, format)
}
# p2 + scale_x_datetime(limits = c(min(wdata$time_formatted), max(wdata$time_formatted)), minor_breaks=date_breaks("6 hour"), labels=my_format("%H:%M"))

# create 5 minute interval buckets
library(chron)
group <- seq(0,55,5)
data$fmintervals <- sapply(data$datetime, function(x){
  x <- minutes(x)
  for(i in 2:length(group)){
    if(x < group[i]) {return(group[i-1]); break}
    else if(x >= group[length(group)]) return(group[length(group)])
  }
})


# wdata$date <- factor(as.Date(wdata$time_formatted))
data["fmintervals"] <- lapply(data["fmintervals"], function(x) ifelse(nchar(x) < 2, paste0("0",x), x))
data["hourofday"] <- lapply(data["hourofday"], function(x) ifelse(nchar(x) < 2, paste0("0",x), x))
data$hms <- paste0(data$hourofday, data$fmintervals, "00")

# now do same thing grouped by 5 minute intervals
# wdata2 <- wdata %>% group_by(fmintervals, weekend) %>% summarize(avgsurge=mean(avgsurge))
# wdata2["fmintervals"] <- lapply(wdata2["fmintervals"], function(x) ifelse(nchar(x) < 2, paste0("0",x), x))
# wdata2$time <- as.POSIXct(paste0("20010101", " ", wdata2$fmintervals, "00"), format="%Y%m%d %H%M")
data$date <- gsub( "-", "", as.character(data$date))
data$date_graph <- as.POSIXct(paste0(data$date, " ", data$hour, data$fmintervals, "00"), format="%Y%m%d %H%M%S")
data$time2 <- strftime(data$date_graph, format="%H:%M:%S")

weekend <- data %>% group_by(time2, weekend) %>% summarize(avgsurge = mean(surge))
weekend$date <- factor(as.Date(weekend$time_formatted))

p3 <- ggplot(weekend, aes(x=time_formatted, y=avgsurge, group=date, color=weekend)) + geom_step()
weekend$time_formatted <- as.POSIXct(paste("20010101", weekend$time2), format="%Y%m%d %H:%M:%S")
p3 + scale_x_datetime(limits = c(min(weekend$time_formatted), max(weekend$time_formatted)), minor_breaks=date_breaks("6 hour"), labels=my_format("%H:%M"))

test <- data %>% group_by(dayofweek, hms, weekend) %>% summarize(avgsurge=mean(surge))
test2 %>% group_by(hms, weekend) %>% summarize(avgsurge=mean(avgsurge))
test2$datetime <- as.POSIXct(paste("20010101", test2$hms), format="%Y%m%d %H%M%S")

p4 <- ggplot(data=test2, aes(x=datetime, y=avgsurge, group=weekend, color=factor(weekend))) + geom_step() + theme_light()
p4 <- p4 + scale_x_datetime(limits = c(min(test2$datetime), max(test2$datetime)), labels=my_format("%H:%M"))
p4 <- p4 + geom_hline(yintercept=mean(filter(test2, weekend == 'weekend')$avgsurge), color='#00BFC4', linetype='longdash') + geom_hline(yintercept=mean(filter(test2, weekend != 'weekend')$avgsurge), color='#F8766D', linetype='longdash')
p4 + labs(x="Hour of Day", y="Avg Surge Rate", title="Avg. Uber Surge Rate Between Penn & NYU (week of Jan 24) ")

blockchart <- data %>% group_by(dayofweek, hourofday) %>% summarize(avgsurge=mean(surge))
blockchart$dayofweek <- as.factor(as.integer(blockchart$dayofweek) + 1)
blockchart$hourofday <- as.factor(as.integer(blockchart$hourofday) + 1)
blockchart$avgsurge <- as.factor(blockchart$avgsurge)
names(blockchart) <- c("day", "hour", "value")
write.table(blockchart, file = "blockchart.tsv", row.names=FALSE)

# what if monday wasn't all that crazy bc of the snow?
filter(blockchart, dayofweek %in% c(1,2,3,4)) %>% filter(hourofday %in% c("06","07","08","09", "10", "18", "19", "20")) %>% group_by(hourofday) %>% summarize(mean_surge = mean(avgsurge))

# ------

# need data for multiline chart in d3
wkd <- filter(test2, weekend == 'weekday') %>% select(avgsurge)
wke <- filter(test2, weekend == 'weekend') %>% select(avgsurge)
dt <- filter(test2, weekend == 'weekend') %>% select(datetime)
df = data.frame(dt[,2], wkd[,2], wke[,2])
names(df) <- c("datetime", "weekday", "weekend")
df$datetime <- as.factor(df$datetime)
df$weekday <- as.factor(df$weekday)
df$weekend <- as.factor(df$weekend)
write.csv(df, file = "multidata.csv", row.names=FALSE)



