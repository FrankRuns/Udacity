library(ggplot2)
data(diamonds)

# Let's consider the price of a diamond and it's carat weight.
# Create a scatterplot of price (y) vs carat weight (x).
# Limit the x-axis and y-axis to omit the top 1% of values.

ggplot(diamonds, aes(x=carat, y=price)) +
      geom_point(color="orange") +
      stat_smooth(method="lm") +
      scale_x_continuous(limits=c(min(diamonds$carat), quantile(diamonds$carat, 0.99))) +
      scale_y_continuous(trans = log10_trans(), limits=c(min(diamonds$price), quantile(diamonds$price, 0.99))) +
      ggtitle('Price (log10) by Carat')

# You'll need these libraries
library(GGally)
library(scales)
library(memisc)
library(lattice)
library(MASS)
library(car)
library(reshape)
library(plyr)

set.seed(12345)
diamond_samp <- diamonds[sample(1:length(diamonds$price), 1000),]
ggpairs(diamond_samp, params = c(shape = I('.'), outlier.shape = I('.')))

# Next we want to transform our data along these axes
cuberoot_trans = function() trans_new('cuberoot',
                                      transform = function(x) x^(1/3),
                                      inverse = function(x) x^3)

ggplot(diamonds, aes(x=carat, y=price)) +
      geom_jitter(alpha = 1/2, size=3/4, color="orange") +
      stat_smooth(method="lm") +
      scale_x_continuous(trans = cuberoot_trans(), limits=c(min(diamonds$carat), quantile(diamonds$carat, 0.99))) +
      scale_y_continuous(trans = log10_trans(), limits=c(min(diamonds$price), quantile(diamonds$price, 0.99))) +
      ggtitle('Price (log10) by Cube-Root of Carat')

# Adjust the plot to explore clarity impact on price
ggplot(diamonds, aes(x=carat, y=price, color=clarity)) +
      geom_jitter(alpha = 1/2, size=3/4) +
      # stat_smooth(method="lm") +
      scale_x_continuous(trans = cuberoot_trans(), limits=c(min(diamonds$carat), quantile(diamonds$carat, 0.99))) +
      scale_y_continuous(trans = log10_trans(), limits=c(min(diamonds$price), quantile(diamonds$price, 0.99))) +
      ggtitle('Price (log10) by Cube-Root of Carat')

# Adjust the plot to explore cut impact on price
ggplot(diamonds, aes(x=carat, y=price, color=cut)) +
      geom_jitter(alpha = 1/2, size=3/4) +
      # stat_smooth(method="lm") +
      scale_x_continuous(trans = cuberoot_trans(), limits=c(min(diamonds$carat), quantile(diamonds$carat, 0.99))) +
      scale_y_continuous(trans = log10_trans(), limits=c(min(diamonds$price), quantile(diamonds$price, 0.99))) +
      ggtitle('Price (log10) by Cube-Root of Carat colored by Cut')

# Adjust the plot to explore color impact on price
ggplot(diamonds, aes(x=carat, y=price, color=color)) +
      geom_jitter(alpha = 1/2, size=3/4) +
      # stat_smooth(method="lm") +
      scale_x_continuous(trans = cuberoot_trans(), limits=c(min(diamonds$carat), quantile(diamonds$carat, 0.99))) +
      scale_y_continuous(trans = log10_trans(), limits=c(min(diamonds$price), quantile(diamonds$price, 0.99))) +
      ggtitle('Price (log10) by Cube-Root of Carat colored by Color')

# Time to model. Need to use I feature
m1 <- lm(I(log(price)) ~ I(carat^(1/3)), data = diamonds)
m2 <- update(m1, ~ . + carat)
m3 <- update(m2, ~ . + cut)
m4 <- update(m3, ~ . + color)
m5 <- update(m4, ~ . + clarity)
mtable(m1, m2, m3, m4, m5)

# When we model with more data it might
# be a good idea to leave out top outliers

testDiamond = data.frame(carat = 1.00, cut = "Very Good",
                         color = "I", clarity = "VS1")
modelEstimate = predict(m5, newdata = testDiamond,
                        interval = "prediction", level = .95)
exp(modelEstimate)
