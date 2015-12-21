setwd('Desktop/Data_Vis_Code_Files/lesson2/')

library(ggplot2)

data <- read.csv('global_debt2.csv')

names(data) <- c("Country", "Continent", "Region", "Debt2GDP", "TotalDebt", "GDP", "PercentDebt")

data$DebtBucket <- cut(data$PercentDebt, breaks=2)

ggplot(aes(x=reorder(Country, PercentDebt), y=PercentDebt, fill=DebtBucket), data=data) +
  geom_bar(stat='identity') +
  coord_flip()

ggplot(data, aes(x=TotalDebt, y=Debt2GDP, fill=DebtBucket)) +
  geom_bar(stat='identity') +
  scale_fill_manual(values=c("blue", "red"))

ggplot(aes(x=GDP, y=TotalDebt, fill=PercentDebt), data=data) +
  geom_point()


