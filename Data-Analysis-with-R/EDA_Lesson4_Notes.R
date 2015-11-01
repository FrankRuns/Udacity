library(ggplot2)
pf = read.csv("pseudo_facebook.tsv", sep = '\t')
# Scatterplots - Age & Friend Count
qplot(x = age, y = friend_count, data = pf) + coord_trans(y="sqrt")
ggplot(aes(x = age, y = friend_count), data = pf) + geom_jitter(alpha = 1/20) +
      xlim(13, 90) # jitter adds moise to your points & alpha adds clarifty... 1/20 means 1 dot is used for every 20
ggplot(aes(x = age, y = friend_count), data = pf) + geom_point(alpha = 1/20, position = position_jitter(h=0)) +
      xlim(13, 90) + coord_trans(y="sqrt") # coord_trans transforms the specified axis
# Scatterplots - Age & Friendship Initiated
qplot(x = age, y = friendships_initiated, data = pf)
ggplot(aes(x = age, y = friendships_initiated), data = pf) + geom_point(alpha = 1/20) +
      xlim(13,90) + coord_trans(y = "sqrt")

# Means and means
library('dplyr')
age_groups <- group_by(pf, age)
pf_fc_by_age <- summarize(age_groups,
            friend_count_mean = mean(friend_count),
            frend_count_median = median(friend_count),
            n = n())
ggplot(aes(x = age, y = friend_count_mean), data = pf_fc_by_age) +
      geom_line()
# Now combine with scatterplot from above
ggplot(aes(x = age, y = friend_count), data = pf) +
      coord_cartesian(xlim = c(13, 70), ylim = c(0,1000)) +
      geom_point(alpha = 1/20, position = position_jitter(h=0), color = 'orange') +
      geom_line(stat = "summary", fun.y = mean) +
      geom_line(stat = "summary", fun.y = median, color = 'green') +
      geom_line(stat = "summary", fun.y = quantile, probs = 0.1, linetype = 2, color = 'blue') +
      geom_line(stat = "summary", fun.y = quantile, probs = 0.9, linetype = 2, color = 'blue')

# Correlation
cor.test(pf$age, pf$friend_count, method = 'pearson')
# cor.test defaults to pearson
with(pf, cor.test(age, friend_count, method = 'pearson'))
with(subset(pf, age <= 70), cor.test(age, friend_count, method = 'pearson'))

# Scatterplot for like vs. desktop likes with linear model (lm)
ggplot(aes(y = likes_received, x = www_likes_received), data = pf) +
      geom_point() +
      xlim(0, quantile(pf$www_likes_received, 0.95)) +
      ylim(0, quantile(pf$likes_received, 0.95)) +
      geom_smooth(method = 'lm', color = 'red')
with(pf, cor.test(likes_received, www_likes_received, method = 'pearson'))

# Correlation in Mitchell dataset
library('alr3')
data(Mitchell)
?Mitchell
# Create scatterplot for temp and month
ggplot(aes(x=Month%%12, y=Temp), data = Mitchell) + geom_point() #+ scale_x_discrete(breaks = seq(0,nrow(Mitchell),12)) + scale_y_continuous(expand=c(2,2))#geom_vline(xintercept=seq(0,nrow(Mitchell),12))
# Look at average temp by month of year
Mitchell$moy <- rep(seq(1,12,1),17)
Mitchell %>% group_by(moy) %>% summarize(mean = mean(Temp))
# Find the pearson correlation between month and temp (my guess is 0)
with(Mitchell, cor.test(Month, Temp, method = 'pearson'))
# The dcor.ttest in the energy package is a non-parametric test of the independence of two variables.
# The null hypothesis is that there is no relationship between the two variables - they are independent
dcor.ttest(Mitchell$Month, Mitchell$Temp)
# p-value of 0.8261 means we cannot reject the null and there is no relationship seen between variables

# Going back to age and frined count, create users age in months
pf$age_with_months <- pf$age + (1 - pf$dob_month/12)
# Now create dataframe grouped by age in months and calcs the mean and median friend count
pf.fc_by_age_months <- pf %>% group_by(age_with_months) %>% summarize(friend_count_mean = mean(friend_count), friend_count_median = median(friend_count), n = n()) %>% arrange(age_with_months)
# Now replot this by months, followed by years, followed by 5yr intervals
ggplot(aes(x=age_with_months, y=friend_count_mean), data = subset(pf.fc_by_age_months, age_with_months<71)) + geom_line() + geom_smooth()
# Interestingly if I wanted to build a loess model (easiest way to think about this is it's a least squares model for local sets of data)
model <- loess(friend_count ~ age, pf)
# predict(the model, the age we want a prediction for..)
predict(model, 30)