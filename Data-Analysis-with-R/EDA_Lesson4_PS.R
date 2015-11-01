library(ggplot2)
library(ggthemes)
theme_set(theme_economist())
data(diamonds)

# Your first task is to create a
# scatterplot of price vs x.
# using the ggplot syntax.
ggplot(aes(x=x, y=price), data=diamonds) + geom_point() + xlim(3,12)+ geom_smooth()
model <- loess(price ~ x, data=diamonds)
predict(model, 5.7)

# Correlations
with(diamonds, cor.test(x=price, y=x, method='pearson'))
with(diamonds, cor.test(x=price, y=y, method='pearson'))
with(diamonds, cor.test(x=price, y=z, method='pearson'))

# Create a simple scatter plot of price vs depth.
p1 <- ggplot(aes(x=depth, y=price), data=diamonds) + geom_point()
p2 <- ggplot(aes(x=depth, y=price), data=diamonds) + geom_point(alpha=1/20)
library(grid); library(gridExtra)
grid.arrange(p1,p2)

# Whats the correlation between depth and price?
with(diamonds, cor.test(x=depth, y=price, method='pearson')) # a very small correlation
library(energy)
set.seed(1234)
samp <- diamonds[sample(nrow(diamonds), 5000),]
dcor.ttest(samp$depth, samp$price)
# Getting a small p-value so we can reject the null.. a relationship exists.. but not sure what kind

# Create a scatterplot of price vs carat
# and omit the top 1% of price and carat
# values.
top_price <- quantile(diamonds$price, .99)
top_carat <- quantile(diamonds$carat, .99)
bottom99 <- subset(diamonds, price < top_price & carat < top_carat)
ggplot(aes(x=carat, y=price), data=bottom99) + geom_point()

# Create a scatterplot of price vs. volume (x * y * z).
# This is a very rough approximation for a diamond's volume.
diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
ggplot(aes(x=volume, y=price), data=diamonds) + geom_point()
library(plyr)
count(diamonds$volume == 0) # count is in plyr package
detach("package:plyr", unload=TRUE) # do this so it doesn't fuck up dplyr package later

# Whats correlation between price and volume.
# Exclude values with volume of 0 or less than/equal to 800
data_clean_carat <- subset(diamonds, carat != 0 & carat <= 800)
with(data_clean_carat, cor.test(x=carat, y=price, method='pearson'))

# Subset the data to exclude diamonds with a volume
# greater than or equal to 800. Also, exclude diamonds
# with a volume of 0. Adjust the transparency of the
# points and add a linear model to the plot. (See the
# Instructor Notes or look up the documentation of
# geom_smooth() for more details about smoothers.)
diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
data_clean_volume <- subset(diamonds, volume != 0 & volume <= 800)
ggplot(aes(x=volume, y=price), data=data_clean_volume) + geom_point(alpha=1/20) + geom_smooth(method='lm')

# Use the function dplyr package
# to create a new data frame containing
# info on diamonds by clarity.

# Name the data frame diamondsByClarity

# The data frame should contain the following
# variables in this order.

#       (1) mean_price
#       (2) median_price
#       (3) min_price
#       (4) max_price
#       (5) n

# where n is the number of diamonds in each
# level of clarity.
library('dplyr')
diamondsByClarity <- diamonds %>%
      group_by(clarity) %>%
      summarize(
            mean_price = mean(as.numeric(price)),
            median_price = median(as.numeric(price)),
            min_price = min(as.numeric(price)),
            max_price = max(as.numeric(price)),
            n = n())

# We’ve created summary data frames with the mean price
# by clarity and color. You can run the code in R to
# verify what data is in the variables diamonds_mp_by_clarity
# and diamonds_mp_by_color.

# Your task is to write additional code to create two bar plots
# on one output image using the grid.arrange() function from the package
# gridExtra.
diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

diamonds_by_cut <- group_by(diamonds, cut)
diamonds_mp_by_cut <- summarise(diamonds_by_cut, mean_price = mean(price))

library(gridExtra)
p1 <- ggplot(aes(x=factor(clarity), y=mean_price), data = diamonds_mp_by_clarity) +
      geom_bar(stat='identity')
p2 <- ggplot(aes(x=factor(color), y=mean_price), data = diamonds_mp_by_color) +
      geom_bar(stat='identity')
grid.arrange(p1,p2)
# Mean price by cut
ggplot(aes(x=factor(cut), y=mean_price), data = diamonds_mp_by_cut) +
      geom_bar(stat='identity')

# The Gapminder website contains over 500 data sets with information about
# the world's population. Your task is to continue the investigation you did at the
# end of Problem Set 3 or you can start fresh and choose a different
# data set from Gapminder.

# In your investigation, examine pairs of variable and create 2-5 plots that make
# use of the techniques from Lesson 4.

# Once you've completed your investigation, create a post in the discussions that includes:
#       1. the variable(s) you investigated, your observations, and any summary statistics
#       2. snippets of code that created the plots
#       3. links to the images of your plots

setwd("/Users/frankCorrigan/Downloads")
library(XLConnect)
# Read and clean headers for labor participation
wb = loadWorkbook("life_part_over_15.xlsx")
labor = readWorksheet(wb, "data", header=T)
colnames(labor) <- substr(colnames(labor),2,6)
colnames(labor)[1] <- 'Country'
# Read and clean headers for economic growth
wb = loadWorkbook("economic_growth.xlsx")
wb = loadWorkbook("indicatorwdigdp_percapita_growth.xlsx")
growth = readWorksheet(wb, "data", header=T)
colnames(growth) <- substr(colnames(growth),2,6)
colnames(growth)[1] <- 'Country'
# Subset only 2004 data and join both sets
library('dplyr')
labor_2003 <- select(labor, Country, 25)
growth_2003 <- select(growth, Country, 45)
data_2003 <- left_join(labor_2003, growth_2003, by="Country")
colnames(data_2003) <- c('country', 'labor', 'growth')
# Remove NA values
data_2003_v1 <- subset(data_2003, !is.na(growth))
# Create plots
ggplot(aes(x=growth, y=labor), data=data_2003_v1) + geom_point() # Looks like no relationship.. but lets remove outliers..
data_2003_v2 <- arrange(data_2003_v1, desc(growth)) %>% filter(growth < 10 & growth > -0.5)
# data_2003_v2 <- data_2003_v2[3:nrow(data_2003_v2),]
ggplot(aes(x=growth, y=labor), data=data_2003_v2) + geom_point() # Looks like no relationship.. but lets add lines to be sure
ggplot(aes(x=growth, y=labor), data=data_2003_v2) +
      geom_point() +
      geom_vline(xintercept = median(data_2003_v2$growth), linetype = 'longdash') +
      geom_hline(yintercept = median(data_2003_v2$labor), linetype = 'longdash') +
      geom_smooth(method="lm") # looks like definitely no relationship
# So lets use some correlation and ttest to confirm
with(data_2003_v1, cor.test(x=growth, y=labor, method="pearson")) # very weak
library(energy)
# Null hypothesis is that there is some kind of relationship between these variables
dcor.ttest(data_2003_v2$growth, data_2003_v2$labor)
# Hmm getting a large p-value so we cannot reject the null... which tells me there no relationship here...
# I want to reshope the original data to get the 
# average labor force participaion rate between 1993 
# and 2003 for each country since we are comparing it
# to the economic growth over those 10 years.
library('tidyr')
lab_avg <- gather(labor, "year", "labpart", 16:25) %>% select(Country, year, labpart)
avg_lab_part <- lab_avg %>% group_by(Country) %>% summarize(mean_labor = mean(labpart))
# Great, now join this up with economic growth
growth_2003 <- select(growth, Country, 45)
data = left_join(avg_lab_part, growth_2003, by="Country")
colnames(data) <- c('country', 'labor', 'growth')
# Remove NA values
data_avg <- subset(data, !is.na(growth))
# Start with a plot
ggplot(aes(x=growth, y=labor), data=data_avg) + geom_point() # Still looks weak... so let's see if we use 10 yr change in labor participation

# I want to find the 10 yr change in labor
# participation and then compare to 10 yr
# economic growth rate
labor$change <- ((labor$"2003" - labor$"1994") / labor$"1994") * 100
# Now clean datasets, combine, and look for relationship
library('dplyr')
labor_chg <- select(labor, Country, change) # this is change from 1994 to 2003
growth_chg <- select(growth, Country, 45) # this is 2003
data_chg <- left_join(labor_chg, growth_chg, by="Country")
colnames(data_chg) <- c('country', 'labor', 'growth')
# Remove NA values
data_chg_clean <- subset(data_chg, !is.na(growth))
# Plot 10 yr change datasets
ggplot(aes(x=growth, y=labor), data=data_chg_clean) + geom_point() # still looks weak... remove outliers
# Remove outliers in growth
data_chg_clean_out <- arrange(data_chg_clean, desc(growth)) %>% filter(growth < 10 & growth > -0.5)
# Plot again
ggplot(aes(x=growth, y=labor), data=data_chg_clean_out) + geom_point() # still looks weak... remove outliers
ggplot(aes(x=growth, y=labor), data=data_chg_clean_out) +
      geom_point() +
      geom_vline(xintercept = median(data_chg_clean_out$growth), linetype = 'longdash') +
      geom_hline(yintercept = median(data_chg_clean_out$labor), linetype = 'longdash') +
      geom_smooth(method="lm")
with(data_chg_clean_out, cor.test(x=growth, y=labor, method="pearson"))
# Relationship still weak... really non-existent... next question is about lag.. if we offset the data so that for instance we plot year 2000 economic growth versus 2003 labor participation will that make a difference

# I want to see if there is a lag
# effect happeing here that will 
# show us stronger relationship. I 
# will assume stronger economy leads to
# increased labor participation...
# I need economic growth 2000 and labor part 2005 for a 5 year lag
labor_lag <- select(labor, Country, 4)
growth_lag <- select(growth, Country, 22)
data_lag <- left_join(labor_lag, growth_lag, by="Country")
colnames(data_lag) <- c('country', 'labor', 'growth')
# Remove NA values
data_lag_clean <- subset(data_lag, !is.na(growth))
# Remove outliers in growth
data_lag_clean_out <- arrange(data_lag_clean, desc(growth)) %>% filter(growth < 10 & growth > -0.5)
# Plot
ggplot(aes(x=growth, y=labor), data=data_lag_clean_out) + geom_point()
ggplot(aes(x=growth, y=labor), data=data_lag_clean_out) +
      geom_point() +
      geom_vline(xintercept = median(data_lag_clean_out$growth), linetype = 'longdash') +
      geom_hline(yintercept = median(data_lag_clean_out$labor), linetype = 'longdash') +
      geom_smooth(method="lm")
# What about correlation
with(data_lag_clean_out, cor.test(x=growth, y=labor, method="pearson"))
# Playing around with years and lag periods it would seem there is almost a negative relationship. Strong growth over past 10 years leads to lower labor participation in the next few years... which means labor productivity is probably strong at work influenctially

# So lets look at individual nations over time
labor_US <- filter(labor, Country == "United States")
growth_US <- filter(growth, Country == "United States")
labor_US_gather <- gather(labor_US, "year", "labpart", 2:29)
growth_US_gather <- gather(growth_US, "year", "econ_grow", 2:46)
data_US <- left_join(labor_US_gather, growth_US_gather, by="year")
data_US_small <- select(data_US, year, labpart, econ_grow)
data_US_smaller <- filter(data_US_small, year < 2005)
# Finally, now plot over time
ggplot(aes(x=econ_grow, y=labpart), data=data_US_smaller) + geom_point() + geom_line()
# Nothing...

# Shit.. using a 2 year lag. So.. strong econ growth in 1980 leads to better labor participation in 1982
data_US_smaller$lag <- c(data_US_smaller[6:nrow(data_US_smaller), 2], NA, NA, NA, NA, NA)
need <- nrow(data_US_smaller)-5
data_US_smallest <- data_US_smaller[1:need, ]
data_test <- filter(data_US_smallest, lag > 65)
ggplot(aes(x=econ_grow, y=lag), data=data_US_smallest) + geom_point() + geom_line()
ggplot(aes(x=econ_grow, y=lag), data=data_test) + geom_point() + geom_smooth(method="lm")
# Nothing significant.. I am thinking that 10 year economic growth has little to do with trends in labor participation... 
# It's probably a good idea to look at yoy economic growth, trends in labor participation, as well as trends in labor productivity

# Last attempt.
setwd("/Users/frankCorrigan/Downloads")
library(XLConnect)
library('ggplot2')
library('dplyr')
library('tidyr')
library('energy')
# Read and clean headers for labor participation
wb = loadWorkbook("life_part_over_15.xlsx")
labor = readWorksheet(wb, "data", header=T)
colnames(labor) <- substr(colnames(labor),2,6)
colnames(labor)[1] <- 'Country'
# Read and clean headers for economic growth
wb = loadWorkbook("indicatorwdigdp_percapita_growth.xlsx")
growth = readWorksheet(wb, "data", header=T)
colnames(growth) <- substr(colnames(growth),2,6)
colnames(growth)[1] <- 'Country'
# Gather datasets and find average labor and growth rate and combine
growth <- select(growth, Country, 22:49)
labor_gather <- gather(labor, "year", "labpart", 2:29)
growth_gather <- gather(growth, "year", "econ_grow", 2:29)
labor_avg <- labor_gather %>% group_by(Country) %>% summarize(mean_labor = mean(labpart))
growth_avg <- growth_gather %>% group_by(Country) %>% summarize(mean_growth = mean(econ_grow))
data <- left_join(labor_avg, growth_avg, by="Country")
# Remove NA values
data_clean <- subset(data, !is.na(mean_growth))
# Remove outliers in growth
data_clean_out <- arrange(data_clean, desc(mean_growth)) %>% filter(mean_growth < 8 & mean_growth > -0.2)
# Plot
ggplot(aes(x=mean_growth, y=mean_labor), data=data_clean_out) +
      geom_point() +
      geom_vline(xintercept = median(data_clean_out$mean_growth), linetype = 'longdash') +
      geom_hline(yintercept = median(data_clean_out$mean_labor), linetype = 'longdash') +
      geom_smooth(method="lm")
with(data_clean, cor.test(x=mean_growth, y=mean_labor, method="pearson"))

# What if growth is followed by increased participation?
data <- left_join(labor_gather, growth_gather, by=c("Country", "year"))
data_clean <- subset(data, !is.na(econ_grow))
ggplot(data=data_clean, aes(x=econ_grow, y=labpart)) +
      geom_point() +
      labs(x="Growth", y="Part.") +
      geom_smooth(method="lm") +
      facet_wrap(~year, scales="free")
# Still digging!!! -- lag labor part one year behind growth
temp <- filter(labor_gather, year != 1980)
labor_gather$next_year <- c(temp$labpart, rep(NA, nrow(labor_gather) - length(temp$labpart)))
data <- subset(labor_gather, !is.na(next_year))
data$chg <- ((data$next_year-data$labpart) / data$next_year) * 100
together <- left_join(data, growth_gather, by=c("Country", "year"))
together_clean <- subset(together, !is.na(econ_grow))
together_cleaner <- select(together_clean, Country, year, chg, econ_grow)
ggplot(data=together_cleaner, aes(x=econ_grow, y=chg)) +
      geom_point(alpha=1/10) +
      xlim(-10,10) +
      labs(title="Growth & Labor Participation 1Yr Later", x="Growth", y="Change in Part.") +
      geom_vline(xintercept = median(together_cleaner$econ_grow), linetype = 'longdash') +
      geom_hline(yintercept = median(together_cleaner$chg), linetype = 'longdash') +
      geom_smooth(method="lm") +
      facet_wrap(~year, scales="free")
ggsave("growth&participation.png")
# What does this relationship look like decaded by decade?