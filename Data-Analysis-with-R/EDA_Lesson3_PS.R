# Summarize data
library(ggplot2)
data(diamonds)
nrow(diamonds)
length(names(diamonds))
str(diamonds)
help(diamonds)

# Set theme for ggplots
library(ggthemes)
theme_set(theme_economist())

# Histogram of price
qplot(price, data = diamonds) #+
      # scale_x_log10()
hist

# Subsetting the data
nrow(diamonds[which(diamonds$price >= 15000),])

# Revisit histogram
qplot(price, data = diamonds)
ggplot_build(hist) # $924 bucket contains most obs = 13,256
hist <- qplot(x=diamonds$price, data=diamonds, binwidth=1,
      main = "Diamond Price Histogram", color = I('black'), fill = I('red')) +
      scale_x_continuous(breaks=c(0,5000,10000), limits=c(0,10000))
ggsave('diamondPriceHistogram.png')
# Get the mode price
temp <- table(diamonds$price)
names(temp)[temp == max(temp)]

# Histograms for price by cut
qplot(price, data = diamonds) +
      facet_wrap(~cut, scales='free') + 
      scale_x_log10()

# Summary stats for price and diamond cut
diamonds[which(diamonds$price == max(diamonds$price)),]
diamonds[which(diamonds$price == min(diamonds$price)),]
by(diamonds$price, diamonds$cut, summary)
by(diamonds$price, diamonds$cut, max)

# Into boxplots
qplot(x = clarity, y = price, data = diamonds, geom = 'boxplot')
qplot(x = cut, y=price, data = diamonds, geom = 'boxplot')
qplot(x = color, y=price, data = diamonds, geom = 'boxplot')

# Summary stats for price and diamond color
by(diamonds$price, diamonds$color, summary)
IQR(diamonds[which(diamonds$color == 'D'),][,'price'])
IQR(diamonds[which(diamonds$color == 'J'),][,'price'])

# Exploring price per carat and color
diamonds$pricePerCarat <- NA
diamonds$pricePerCarat <- diamonds$price / diamonds$carat
qplot(x = color, y=pricePerCarat, data = diamonds, geom = 'boxplot')
by(diamonds$pricePerCarat, diamonds$color, summary) # Color is a determinant of price

# Freq plots for carat
fplot = qplot(x=carat, data = subset(diamonds, !is.na(diamonds$carat)),
      binwidth=0.001, geom = 'freqpoly') +
      scale_x_continuous(limit=c(0.9,1.2))
ggplot_build(fplot)

# Sidebar... Data Wrangling with R Tutorial
library('devtools')
devtools::install_github('rstudio/EDAWR')
library('EDAWR')
library('tidyr') # reshapes layout of data sets
# tidyr gather function makes a table into a long dataset so that there is a list of key value pairs
cases_gather <- gather(cases, "year", "n", 2:4)
# Remember that the purpose is to have one variable per row and column
pollution_spread <- spread(pollution, size, amount)
pollution_regather <- gather(pollution_spread, "large", "amount", 2:3)
# spread and gather are inverses of each other
# We can use seperate to split characters in column by a character
separate(storms, date, c("year", "month", "day"), sep="-")
# And unite is the inverse of separate

library('dplyr') # helps transform tabular data
# Look at select, filter, mutate, summarize
library('nycflights13')
select(storms, storm, pressure) # select is all about selecting columns
select(storms, wind:date)
# Also contains(), end_with(), everything(), matches(), num_ranges(), one_of(), start_with()
filter(storms, wind >= 50) # filter is all about selecting rows conditionally
filter(storms, wind >= 50, storm %in% c("Alberto", "Arlene"))
# ?Comparison
mutate(storms, ratio = pressure / wind, inverse = ratio^-1)
mutate(storms, cumsum(wind))
# mutate is all about creating new variables
# Also pmin(), pmax(), between(), cume_dist(), cumall(), cumany(), lead(), lag(), ntile(), dense_rank(), min_rank(), percent_rank(), row_number()
pollution %>% summarize(median = median(amount), variance = var(amount))
pollution %>% summarize(mean = mean(amount), sum = sum(amount), n = n())
# summarize is all about aggregating data
# Also, min(), max(), first(), last(), nth(), n_distinct()
arrange(storms, wind)
arrange(storms, desc(wind))
arrange(storms, wind, date)
# arrange is all about ordering data
# Pipe Operator for multiple operations
storms %>% filter(wind >= 50) %>% select(storm, pressure)
storms %>% mutate(ratio = pressure / wind) %>% select(storm, ratio)
# Pipe is all about multiple operations... just like pipe in terminal
pollution %>% group_by(city)
pollution %>% group_by(city) %>% summarize(mean = mean(amount), sum = sum(amount))
pollution %>% ungroup()
# group_by() and ungroup() all about ... duh grouping data together
left_join(songs, artists, by = "name")
left_join(songs2, artists2, by = c("first", "last"))
anti_join(songs, artists, by = "name")
# Also, inner_join(), semi_join()
# Join is all about combining data frames

# Gapminder Data Analysis
library(XLConnect)
wb = loadWorkbook("laborparticipation.xlsx")
data = readWorksheet(wb, "data", header=T)
colnames(data) <- substr(colnames(data),2,6)
colnames(data)[1] <- 'Country'
# Histogram
data_gather <- gather(data, "Year", "LFPR", 2:29)
labor_part <- select(data_gather, Country, LFPR) %>% arrange(Country)
labor_part <- labor_part %>% group_by(Country) %>% summarize(mean = mean(LFPR))
middle <- median(labor_part$mean)
ggplot(aes(x = mean), data = labor_part) +
      labs(title = 'Avg. Labor Force Participation Rate Histogram (Ages 15-65) by Country', x = 'Avg. Participation Rate 1980 - 2007') +
      geom_histogram(binwidth = 2, fill = I('red')) +
      geom_vline(xintercept = median(labor_part$mean), linetype = 'longdash') +
      scale_x_continuous(breaks = round(c(40, 60, middle, 80),digits = 1))
# Boxplot
data_gather <- gather(data, "Year", "LFPR", 2:29)
labor_box <- arrange(data_gather, Country)
G20 <- c("Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", "India", "Indonesia", "Italy", "Japan", "Korea, Rep.", "Mexico", "Russia", "Saudi Arabia", "South Africa", "Turkey", "United Kingdom", "United States")
labor_box_20 <- filter(labor_box, Country %in% G20)
qplot(x = LFPR, y = Country, 
      data=labor_box_20,
      geom='boxplot')
# What country had widest ranges
labor_iqr <- labor_box %>% group_by(Country) %>% summarize(low = min(LFPR), high = max(LFPR))
mutate(labor_iqr, range = high - low) %>% arrange(desc(range))
# What countries 'currently' have the lowest lfpr's
labor_2007 <- filter(labor_box, Year == '2007') %>% arrange(desc(LFPR))
labor_2007_mean <- mean(labor_2007$LFPR)
labor_2007_std <- sqrt(var(labor_2007$LFPR))
lower <- labor_2007_mean - (labor_2007_std*2)
upper <- labor_2007_mean + (labor_2007_std*2)
filter(labor_2007, LFPR < lower | LFPR > upper)
# Freqpoly
ggplot(aes(x = LFPR), data = labor_2007) + 
      geom_freqpoly()

# Facebook Birthday Analysis
bdays <- read.csv('birthdaysExample.csv')
library(lubridate)
# How many people share your birthday? Do you know them?
# None. These birthdays all occur in 2014... I have no friends that are less than 2 years old.
# Which month contains the most number of birthdays?
bdays2 <- mutate(bdays, mdy(dates))
max(table(month(bdays2$mdy))) # March has most birthdays
min(table(month(bdays2$mdy))) # Dec has least
# How many birthdays are in each month?
table(month(bdays2$mdy))
# Which day of the year has the most number of birthdays?
table(bdays2$mdy) # May 22
# Do you have at least 365 friends that have birthdays on everyday
# of the year?
length(unique(bdays2$mdy)) # In this data set the answer is no bc there are 365 days in a normal calendar year and there are only 348 unique birthdays in this set
plot(table(day(bdays2$mdy)))
