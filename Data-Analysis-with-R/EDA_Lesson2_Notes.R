View(mtcars)

subset(mtcars, mpg < 20)
mtcars[mtcars$mpg<20,]

summary(data)
table(data$employment.status)
levels(data$age.range)

library(ggplot2)
qplot(data$age.range)

ordered(data$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"))
