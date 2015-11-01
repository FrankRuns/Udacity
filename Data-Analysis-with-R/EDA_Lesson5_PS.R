library(ggplot2)
library(dplyr)
library(ggthemes)
theme_set(theme_tufte())

# Create a histogram of diamond prices.
# Facet the histogram by diamond color
# and use cut to color the histogram bars.

data(diamonds)
ggplot(aes(x=price), data=diamonds, color=cut) +
      geom_histogram(aes(color=cut)) +
      facet_wrap(~color) +
      scale_x_continuous(limits = c(0,12000), breaks=c(0,6000,12000)) +
      scale_x_log10()

# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.

ggplot(aes(x=table, y=price), data=diamonds) +
      geom_point(aes(color = cut))

# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.

diamonds$volume = as.integer(diamonds$x*diamonds$y*diamonds$z)
ggplot(aes(y=price, x=volume), data=subset(diamonds, volume < quantile(diamonds$volume, .99))) +
      geom_point(aes(color=clarity)) + 
      scale_y_log10()

# Your task is to create a new variable called 'prop_initiated'
# in the Pseudo-Facebook data set. The variable should contain
# the proportion of friendships that the user initiated.

setwd("Downloads/")
pf = read.csv("pseudo_facebook.tsv", sep = '\t')
pf$prop_initiated <- pf$friendships_initiated / pf$friend_count

# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.

pf$year_joined <- floor(2014-(pf$tenure/365))
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))
ggplot(aes(x=30*round(tenure/30), y=prop_initiated, color=year_joined.bucket), data=subset(pf, !is.na(prop_initiated))) +
      geom_line(stat="summary", fun.y=median)

# Whats mean prop_initiated for people who joined between 2012 and 2014?
new_comers <- subset(pf, !is.na(prop_initiated))
new_comers <- subset(new_comers, year_joined.bucket == "(2012,2014]")
avg_prop <- mean(new_comers$prop_initiated)

# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.

diamonds = transform(diamonds, pc_ratio = price / carat)
ggplot(aes(x=cut, y=pc_ratio), data=diamonds) +
      geom_jitter(aes(colour=color)) +
      facet_wrap(~clarity)

# The Gapminder website contains over 500 data sets with information about
# the world's population. Your task is to continue the investigation you did at the
# end of Problem Set 4 or you can start fresh and choose a different
# data set from Gapminder.
# Last lesson I explored labor participation rate and GDP growth...
# Now I'll explore labor participation further with GDP growth, education, inflation rate, unemployment, and something I don't even think is related - hydroelectric production per capita

setwd("/Users/frankCorrigan/Downloads")
library(XLConnect)
library('ggplot2')
library('dplyr')
library('tidyr')
library('energy')

onhold = "

files = c("laborpart_1564.xlsx", "gdpcapita_growth.xlsx",
          "literacy_15above.xlsx", "inflation.xlsx", 
          "unemployment_15plus.xlsx", "hydro_production.xlsx")

all <- lapply(files, function(i) {
      wb = loadWorkbook(i)
      readWorksheet(wb, "data", header=T)
})

names(all) <- gsub(".xlsx","",files)

for (i in seq_along(all)) {
      names(all[[i]]) <- substr(names(all[[i]]),2,6)
      names(all[[i]])[1] <- "Country"
}

# Do a sequence of gather & summarize
medians <- lapply(all, function(i) {
      gath <- gather(i, "year", "value", 2:length(names(i)))
      med <- group_by(gath, Country) %>% summarize(median = median(value, na.rm=TRUE))
})

names(medians) <- gsub(".xlsx","_median",files)

# Do a sequence of join and plot
lab_growth <- left_join(medians[[1]], medians[[2]], by="Country")
with(lab_growth, cor.test(median.y, median.x, method="pearson")) #-.021
ggplot(aes(x=median.y, y=median.x), data = lab_growth) +
      geom_jitter() +
      geom_smooth()

lab_lit <- left_join(medians[[1]], medians[[3]], by="Country")
with(lab_lit, cor.test(median.y, median.x, method="pearson")) # -.197
ggplot(lab_lit, aes(x=median.y, y=median.x)) +
      geom_jitter() +
      geom_smooth()

lab_inf <- left_join(medians[[1]], medians[[4]], by="Country")
with(lab_inf, cor.test(median.y, median.x, method="pearson")) #.016
ggplot(lab_inf, aes(x=median.y, y=median.x)) +
      geom_jitter() +
      geom_smooth()

lab_unemp <- left_join(medians[[1]], medians[[5]], by="Country")
with(lab_unemp, cor.test(median.y, median.x, method="pearson")) #-.309
ggplot(lab_unemp, aes(x=median.y, y=median.x)) +
      geom_jitter() +
      geom_smooth(method="lm")

lab_hydro <- left_join(medians[[1]], medians[[6]], by="Country")
with(lab_hydro, cor.test(median.y, median.x, method="pearson")) #.253
ggplot(lab_hydro, aes(x=median.y, y=median.x)) +
      geom_jitter() + 
      scale_x_log10() +
      geom_smooth()

var1_var2 <- left_join(medians[[3]], medians[[5]], by="Country")
with(var1_var2, cor.test(median.y, median.x, method="pearson"))
ggplot(data = subset(var1_var2, !is.na(median.y)), aes(x=median.y, y=median.x, group=Country)) +
      geom_point() + 
      labs(title = "Literacy & Unemployment", x = "Unemployment", y = "Literacy Rate") +
      geom_smooth(method="lm")

# Nothing terribly interesting plotting the medians against each other
# I am going to explore with some line charts
labor_gather <- gather(all[[1]], "year", "value", 2:length(names(all[[1]])))
growth_gather <- gather(all[[2]], "year", "growth", 2:length(names(all[[2]])))
lab_growth_year <- left_join(labor_gather, growth_gather, by=c("Country","year"))
lab_growth_year_clean <- subset(lab_growth_year, !is.na(growth))
ggplot(aes(year, group = "Country"), data=subset(lab_growth_year_clean, Country == "United States")) +
      geom_line(aes(y=log10(value), colour = "value")) +
      geom_line(aes(y=growth, colour = "growth"))
"
files = c("cell_phones.xlsx", "blood_pressure.xlsx")

all <- lapply(files, function(i) {
      wb = loadWorkbook(i)
      readWorksheet(wb, "data", header=T)
})

names(all) <- gsub(".xlsx","",files)

for (i in seq_along(all)) {
      names(all[[i]]) <- substr(names(all[[i]]),2,6)
      names(all[[i]])[1] <- "Country"
}

medians <- lapply(all, function(i) {
      gath <- gather(i, "year", "value", 2:length(names(i)))
      med <- group_by(gath, Country) %>% summarize(median = median(value, na.rm=TRUE))
})

names(medians) <- gsub(".xlsx","_median",files)

phones_stress <- left_join(medians[[1]], medians[[2]], by="Country")
names(phones_stress) <- c("Country", "Phones", "Stress")
with(subset(phones_stress, Phones > 0), cor.test(Phones, Stress, method="pearson", na.rm=TRUE))
ggplot(subset(phones_stress, Phones < 4900000 & Phones > 0), aes(x=Phones, y=Stress)) +
      geom_jitter() +
      scale_y_log10() +
      geom_smooth(method="lm")