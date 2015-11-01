setwd("Downloads/")
library(ggplot2)
library(dplyr)
pf = read.csv("pseudo_facebook.tsv", sep = '\t')

# Write code to create a new data frame,
# called 'pf.fc_by_age_gender', that contains
# information on each age AND gender group.
pf.fc_by_age_gender <- group_by(pf, age, gender) %>%
      filter(!is.na(gender)) %>%
      summarize(mean_friend_count = mean(as.numeric(friend_count)),
                median_friend_count = median(as.numeric(friend_count)),
                n=n()) %>%
      ungroup()

# Create a line graph showing the
# median friend count over the ages
# for each gender. Be sure to use
# the data frame you just created,
# pf.fc_by_age_gender.
ggplot(pf.fc_by_age_gender, aes(x=age, y=median_friend_count, colour=gender)) +
      geom_line()

# In order to look at the difference in 
# friend count betwee male and female
# reshape data to wide format
library(reshape2)
pf.fc_by_age_gender_wide <- dcast(pf.fc_by_age_gender,
                                  age ~ gender,
                                  value.var = "median_friend_count")

# Plot the ratio of the female to male median
# friend counts using the data frame
# pf.fc_by_age_gender.wide.
ggplot(pf.fc_by_age_gender_wide, aes(x=age, y=female/male)) +
      geom_line() +
      geom_hline(yintercept = 1, linetype = 2)

# Create a variable called year_joined
# in the pf data frame using the variable
# tenure and 2014 as the reference year.
pf$year_joined <- floor(2014-(pf$tenure/365))

# Create a new variable in the data frame
# called year_joined.bucket by using
# the cut function on the variable year_joined.

# You need to create the following buckets for the
# new variable, year_joined.bucket

#        (2004, 2009]
#        (2009, 2011]
#        (2011, 2012]
#        (2012, 2014]

pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

# Create a line graph of friend_count vs. age
# so that each year_joined.bucket is a line
# tracking the median user friend_count across
# age. This means you should have four different
# lines on your plot.
ggplot(aes(x=age, y=friend_count), data=subset(pf, !is.na(year_joined.bucket))) +
      geom_line(aes(color=year_joined.bucket), stat='summary', fun.y=mean) +
      geom_line(stat='summary',fun.y=mean,linetype=2)

# Find friend rate = friend count / tenure 
# for users whose tenure is > 1
with(subset(pf, tenure > 1), summary(friend_count / tenure))

# Create a line graph of mean of friendships_initiated per day (of tenure)
# vs. tenure colored by year_joined.bucket.

# You need to make use of the variables tenure,
# friendships_initiated, and year_joined.bucket.

# You also need to subset the data to only consider user with at least
# one day of tenure.

ggplot(aes(x=7*round(tenure/7), y=friendships_initiated/tenure), data=subset(pf,tenure>1)) +
      geom_line(aes(color=year_joined.bucket),stat='summary',fun.y=mean)
ggplot(aes(x=7*round(tenure/7), y=friendships_initiated/tenure), data=subset(pf,tenure>1)) +
      geom_smooth(aes(color=year_joined.bucket))


# On to YOGURT dataset
yo <- read.csv("yogurt.csv")
yo$id <- factor(yo$id)
# Create histogram of prices
ggplot(aes(x=price), data=yo) + geom_histogram()
# Don't forget about summary and table
summary(yo$price)
table(yo$price)
# Use transform to find total # of purchases for each household (id)
yo <- transform(yo, all.purchases = strawberry + blueberry + pina.colada + plain + mixed.berry)

# Create a scatterplot of price vs. time
# Attempt 1
ggplot(aes(x=time, y=price), data=yo) + geom_point() # kinda shit.. sooooo
# Attempt 2
temp <- yo %>% group_by(time) %>% summarize(mean.price = mean(price))
ggplot(aes(x=time, y=mean.price), data=temp) + geom_point() # Ehh... sooo
# Attempt 3
yo$time.buckets <- cut(yo$time, breaks=seq(9662,10640,57))
temp <- subset(yo, !is.na(time.buckets)) %>% group_by(time.buckets) %>% summarize(mean.price = mean(price))
ggplot(aes(x=time.buckets, y=mean.price), data=temp) + geom_point() + geom_line(aes(group=1)) # Better but really depends on what these time buckets actually mean
# Attempt 4
ggplot(aes(x=time, y=price), data=yo) + geom_jitter(alpha = 1/4, color = 'orange')

# Look at subset of households
set.seed(4230)
sample <- sample(levels(yo$id), 16)
ggplot(aes(x=time, y=price),
       data = subset(yo, id %in% sample)) +
       facet_wrap(~id) +
       geom_line() +
       geom_point(aes(size=all.purchases), pch=1)
# Now rocking my own shit..
library(ggthemes)
set.seed(0606)
sample <- sample(levels(yo$id), 16)
ggplot(aes(x=time, y=price),
      data = subset(yo, id %in% sample)) +
      labs(title = 'Seed:0606. 16 Sample Households Yogurt Purchase Price Over Time') +
      facet_wrap(~id) +
      geom_line() +
      geom_point(aes(size=all.purchases), pch=1) +
      theme_economist()
ggsave('yogurt.png')

# Scatterplot matrix
library(GGally)
set.seed(1836)
pf_subset <- pf[,c(2:15)]
ggpairs(pf_subset[sample(nrow(pf_subset), 1000), ])

set.seed(1836)
pf_subset <- pf[,c(2:15)]
data <- pf_subset[sample(nrow(pf_subset), 1000), ]
with(data, cor.test(x=friendships_initiated, y=friend_count, method="pearson"))
with(data, cor.test(x=age, y=mobile_likes, method="pearson"))

