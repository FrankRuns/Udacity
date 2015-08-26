# Looking at friends data from Facebook (not actual data from FB, pho)
pf <- read.csv('pseudo_facebook.tsv', sep='\t')
library(ggplot2)
qplot(x=dob_day, data=pf) +
  scale_x_discrete(breaks=1:31) +
  facet_wrap(~dob_month, ncol=3)
# Also consider facet_grid
library(ggthemes)
theme_set(theme_economist()) # now run qqplot again. See examples https://github.com/jrnold/ggthemes#examples

# Peoples perceived audience size not close to actual audience size
# Apparently people underestimate their audience size

qplot(pf$friend_count) # also called long tail data
qplot(x=friend_count, data=subset(pf, !is.na(gender)), binwidth=25) + 
      scale_x_continuous(limit=c(0,1000), breaks=seq(0,1000,50)) + 
      facet_wrap(~gender)
ggplot(aes(x = friend_count), data = pf) + 
      geom_histogram() + 
      scale_x_continuous(limits = c(0, 1000))
table(pf$gender) # more dudes
by(pf$friend_count, pf$gender, summary) # median is more robust

## Sidebar: Is difference in median statistically significant? #################

attach(pf)
wilcox.test(friend_count ~ gender, data = subset(pf, !is.na(gender)))
detach(pf)

##############################################################################
# Tenure is how many days someones been using facebook
qplot(x=tenure, data=pf, binwidth=30,
      color = I('black'), fill = I('#099009')) 
qplot(x=tenure_years, data=pf, binwidth=0.25,
      color = I('black'), fill = I('#F79420')) +
      scale_x_continuous(breaks=seq(1,7,1), limits=c(0,7)) +
      xlab('# of years using FB') + 
      ylab('# of Users')

qplot(x=age, data=pf, binwidth = 1, 
      color = I('black'), fill = I('#099009')) +
      xlab('Age of Users on FB') +
      ylab('Count of Ages') +
      scale_x_discrete(breaks=seq(0,113,10))

# Transforming the data (rescaling)
summary(pf$friend_count)
summary(log10(pf$friend_count)) # -Inf...gross
summary(log10(pf$friend_count+1)) # Better
summary(sqrt(pf$friend_count))

# Multiple plots in same window
library(gridExtra)
p1 = qplot(x=friend_count, data=pf,
           color = I('black'), fill = I('#099009')) 
p2 = qplot(x=log10(friend_count), data=pf,
           color = I('black'), fill = I('#099009')) 
p3 = qplot(x=sqrt(friend_count), data=pf,
           color = I('black'), fill = I('#099009')) 
grid.arrange(p1, p2, p3)
# OR
p1 = ggplot(aes(x=friend_count), data=pf) + geom_histogram() 
p2 = p1 + scale_x_log10() # This way the x-axis labels are in actual friend counts
p3 = p1 + scale_x_sqrt()
grid.arrange(p1, p2, p3)

# Frequency Polygons
qplot(x=friend_count, y = ..count../sum(..count..),
      data=subset(pf, !is.na(gender)), 
      binwidth=10, geom='freqpoly', color=gender) + 
      scale_x_continuous(limit=c(0,1000), breaks=seq(0,1000,50)) +
      ylab('% of Users with that Friend Count')

# Frequency plot for www_likes between male/female
qplot(x=www_likes, y = ..count../sum(..count..),
      data=subset(pf, !is.na(gender)), 
      binwidth=10, geom='freqpoly', color=gender) + 
      scale_x_continuous(limit=c(0,100), breaks=seq(0,100,10)) +
      ylab('% of Users with # of Likes Generated on Web')
# Using log10 transormation (rescaling) gives more insight
qplot(x=www_likes, data = subset(pf, !is.na(gender)),
      geom = 'freqpoly', color=gender) +
      scale_x_continuous() + 
      scale_x_log10()
ggplot(aes(x = www_likes), data = subset(pf, !is.na(gender))) + 
      geom_freqpoly(aes(color = gender)) + 
      scale_x_log10()
by(pf$www_likes, pf$gender, sum)

# Box Plots
qplot(x=gender, y=friend_count, 
      data=subset(pf, !is.na(gender)),
      geom='boxplot') +
      # scale_y_continuous(limit=c(0,1000)) # this removes some data points
      coord_cartesian(ylim=c(0,1000)) # this keeps all data points
      scale_y_log10()
by(pf$friend_count, pf$gender, summary) # using cartesion matches this output
by(pf$friendships_initiated, pf$gender, summary)

qplot(x=gender, y=friendships_initiated, 
      data=subset(pf, !is.na(gender)),
      geom='boxplot') +
      # scale_y_continuous(limit=c(0,1000)) # this removes some data points
      # coord_cartesian(ylim=c(0,1000)) # this keeps all data points
      scale_y_log10()

# Creating new variable
summary(pf$mobile_likes)
summary(pf$mobile_likes>0)
pf$mobile_check_in <- NA
pf$mobile_check_in <- ifelse(pf$mobile_likes > 0, 1, 0)
pf$mobile_check_in <- factor(pf$mobile_check_in)
# What percent of mobile users have done a mobile checkin?
summary(pf$mobile_check_in)[2]/length(pf$mobile_check_in)
# So it makes sense to continue mobile dev since more than half of users are using mobile

