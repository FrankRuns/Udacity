setwd("/Users/frankCorrigan/Downloads")

# Libraries used for everything...
library(dplyr)
library(ggplot2)
library(gridExtra)

# Row names read in a bit fucked up, so little adjustment needed
data <- read.csv("FEC_FL2012_Data.csv", row.names = NULL)

correct_names <- names(data)[2:length(names(data))]

data <- select(data, -election_tp)

names(data) <- correct_names

# First problem was with header names.. had to correct

str(data)
# 361K donations, 19 features -- mostly categorical, one numeric, one date (that's still factor)

# Initial things that I'm noticing I use table here a lot
# 1. cmte_id is probably political party affiliation. Actually no, these are committee that support the candidate.. from local to national... PACs are in here
# 2. There is a lot of inconsistency in contributor city name and zip which will have to be cleaned to do any mapping maybe -- ST. AU7GUSTINE, ST. AUGUSTINE, ST. AUGUTINE, ST, AUGUSTINE
# 3. There will be a lot of missing/invalid values in contrb employer and occupation
# 4. The dates look pretty good, but will need to be converted to datetime object to do anything with them, which I'll do right off the bat since it's easy enough

data$date <- as.Date(data$contb_receipt_dt, format = "%d-%b-%y")

nom_date <- as.Date("28-AUG-12", format = "%d-%b-%y")

elec_date <- as.Date("06-NOV-12", format = "%d-%b-%y")

data$days_from_elec <- as.integer(elec_date - data$date)

ggplot(aes(x=days_from_elec, y=contb_receipt_amt, color=party), data=samp) +
      geom_point(alpha=1/20) +
      scale_y_log10() +
      scale_x_log10() # Showing Reps get high $ contributions... days from election same

# Univariate Analysis -- Used to get sense of variables and deal with missing values

# Univariate Analysis -- Candidate Info

table(data$cand_id) # 14 unique

table(data$cand_nm) # 14 unique -- Stein = 45 & McCotter = 1 -- remove these

data <- subset(data, cand_nm != "Stein, Jill" & cand_nm != "McCotter, Thaddeus G") # Removes 46 observations

ggplot(aes(x=cand_nm), data=data) +
      geom_bar() +
      ggtitle("Count of Contributions by Candidate") +
      coord_flip() # Barak most contributions by far, followed by romney, followed by Ron Paul

ggplot(aes(x=cand_nm), data=subset(data, date < nom_date)) + # Even playing field using only days before Romney nominated Repub candidate
      geom_bar() +
      ggtitle("Count of Contributions Pre-Nomination Date by Candidate") +
      coord_flip() # Not a huge difference. Romney and Barack still way out front

# What if we look at average # of donations for each day candidate was in the race?
contrib_per_day_in_race <- data %>%
                           group_by(cand_nm) %>%
                           summarize(min = min(date), max = max(date), n=n()) %>%
                           mutate(days = max-min, contrib_per_day = n/as.numeric(days)) # Herman Cain in race for 670 days (most).. Michele Bachmann in race for 219 days (least)

ggplot(aes(x=cand_nm, y=contrib_per_day), data=contrib_per_day_in_race) +
      geom_bar(stat="identity") +
      coord_flip() # Doesn't change much when we plot count of contributions per canddate per day in race

# One thing I'll want to do with this variable is associate political party with each candidate
data$party <- ifelse(data$cand_nm == "Obama, Barack", c("democrat"), c("republican")) 

data$party[data$cand_nm == "Johnson, Gary Earl"] <- "libertarian"

data$party[data$cand_nm == "Roemer, Charles E. 'Buddy' III" | data$cand_nm == "Stein, Jill"] <- "other"

# How many donations did each party receive?
table(data$party) # Wow, Democrats 1.5x Republican donations

# Univariate Analysis -- Contributor Info

mean(table(data$contbr_nm)) # Average # of contributions is 4.4 assuming each name is unique. Wish there was a contributor id... quick search says multiple contributions from single contributor

table(data$contbr_city) # Lots of variety in single city names... not sure it's worth fixing

table(data$contbr_zip) # Zip codes are a mess. We need to fix this now...

library(zipcode) # https://cran.r-project.org/web/packages/zipcode/

data$zip = clean.zipcodes(data$contbr_zip) # Leaves us with many 9-digit zips. Shorten to 5-digit zips.

data$zip = substr(data$zip, 1, 5)

table(data$zip) # Every zip code in FL starts with 3.. so I'm considering zips that start with 0, 1, and 2 bad data and removing

data <- subset(data, zip >= 30000 & zip < 40000) # We lose 423 observations

# Now, are all of our zip codes in FL?
data(zipcode)

data <- left_join(data, zipcode, by="zip")

# TODO -- check contb_city with zipcode city

table(data$state) # Yikes, 61 zip codes outside FL. Drop them please.

data <- filter(data, state == "FL")

# Univariate Analysis -- EMPLOYER -- just want to see top employer
tail(sort(table(data$contbr_employer)),1) # Retired... of course

# Univariate Analysis -- OCCUPATION
table(data$contbr_occupation) # Wow, so much for kinda clean data entry... so much variety

length(sort(table(data$contbr_occupation))) # 12,643 occupations or average of 28.5 observations per occupation

occs_count <- group_by(data, contbr_occupation) %>% 
              summarize(count = n()) %>%
              arrange(desc(count))

ggplot(aes(x=factor(contbr_occupation, levels = contbr_occupation), y=count),
       data=head(filter(occs_count, contbr_occupation != "RETIRED"),500)) +
       geom_bar(stat="identity") +
       geom_hline(yintercept = 30, color = "red", linetype = 'longdash')

# Goal here was to figure out if I should drop occupations that occur only x number of times
# If we use this in our models.. this will be important (and I think I will).. and we should drop these value
# If we don't use occupationin our models.. this won't be important.. and I should leave these values
# For now, assume it's important and we'll drop occupation occuring only > 30 times

occ_count <- data %>%
             group_by(contbr_occupation) %>%
             summarize(n=n()) %>%
             filter(n > 30) # this removes roughly 60,000 observations

data <- subset(data, contbr_occupation %in% occ_count$contbr_occupation) # took out contributions for occupations that appear less than 31 times

# Univariate Analysis -- CONTRIBUTION AMOUNT AND DATE INFO
summary(data$contb_receipt_amt) # So 25,000's looks like an error or maybe interparty transfer.. drop it

data <- subset(data, contb_receipt_amt < 25000 & contb_receipt_amt > -25000)

# data[data$contb_receipt_amt > 5000,] # Pretty shady data at this level... I think drop it but revisit

# data[data$contb_receipt_amt < 0,]) # Also... lots of transfers or refunds bck to contributors -- about 4,000 -- drop them.

data <- subset(data, contb_receipt_amt < 5000 & contb_receipt_amt > 0)

# Let's do some plots of the amount -- histogram
qplot(contb_receipt_amt, data = data, geom = "histogram") + # 2,700 is individual contribution limit
      geom_vline(xintercept=2700, color="red") # Lots of small donations, yes

qplot(contb_receipt_amt, data = data, geom = "histogram", binwidth = 1, color = "red") +
      geom_vline(xintercept=2600, color="blue") 

tail(sort(table(data$contb_receipt_amt)), 20) # All pretty 'safe' donation amounts -- except for 14?

# What about date? Which days did donations fall on most? Is there a trend in donations
qplot(date, data = data, geom = "histogram", binwidth = 1, color = "red") + 
      geom_vline(xintercept = as.numeric(nom_date), color = "blue", linetype = 'longdash') +
      geom_vline(xintercept = as.numeric(elec_date), color = "black", linetype = 'longdash') 
      # of donations increases as election gets closer and blows up after republican nomination of Mitt

# Univariate Analysis -- Receipt Description -- really just curious
table(data$receipt_desc) # I don't understand most of these.. I believe it's either return to contributor due to legal restriction or transfer to another committee















# Bivariate Analysis
qplot(cand_nm, contb_receipt_amt, data = data, geom = "boxplot") + coord_flip() # It looks like a lot of people supported Barack over any other candidate... but I dont think that's fair since he was the incumbent and only Demo contender. Let's look at party instead.

qplot(party, contb_receipt_amt, data = data, geom = "boxplot") + coord_flip() # So it looks like Republicans get bigger contributions on average. Can we see that numerically?

group_by(data, party) %>% summarize(n=n(), mean=mean(contb_receipt_amt), median=median(contb_receipt_amt)) # Indeed, this is telling. Democrats received more smaller donations than republicans

# And what about just pre-nomination?
filter(data, date > nom_date) %>%
      group_by(party) %>%
      summarize(total = sum(contb_receipt_amt),
                mean = mean(contb_receipt_amt),
                median = median(contb_receipt_amt),
                std = sd(contb_receipt_amt)) # Republicans raised more money in 2012 campaign.. and still lost
      # This tells me it's not about amount per se, but more about # of contributions

# BENCHMARK -- it's not about amount per se, but more about # of contributions

# So, what percentage of donations are > 2700 for each party?
data$over2700 <- ifelse(data$contb_receipt_amt > 2700, "Large", "Small")
data$over200 <- ifelse(data$contb_receipt_amt > 200, "Large", "Small")

### group_by(data, party, over2700) %>% summarize(count=n()) 
# Manually.. Repubs = 0.0003 or 0.3%. Democs = 0.000001.. tiny. Does this hold true if we look at amounts rather than counts?
group_by(data, party, over200) %>% summarize(n=n(), sum=sum(contb_receipt_amt)) 
# Manually... 10512/(10512+19243800) for Dems... 157894/(157894+55488477) for Reps. Same outcome. Most campaign money comes from individual donars.
# However, I'm not convinced this is right. A PAC doesn't necessarily have to give 
# http://www.nytimes.com/interactive/2016/us/elections/election-2016-campaign-money-race.html?_r=2
# TODO: Finish this

# Final look at this distribution of contribution amounts by party in a histogram
qplot(contb_receipt_amt, data = data, geom = "histogram", binwidth = 25, color = "red") +
      facet_wrap(~party) # pretty stark contract between rep and dem

# Was Romney always raising the most money out of all the republicans?
for_real <- c("Cain, Herman", "Gingrich, Newt", "Obama, Barack", "Paul, Ron", "Romney, Mitt", "Santorum, Rick") # The other guys are noise...

pre_nom <- filter(data, date < nom_date, cand_nm %in% for_real) %>%
      group_by(cand_nm, date) %>%
      summarize(n = n(), total = sum(contb_receipt_amt))

# Sum of Monetary Contributions for 'Real' cadidates before Romney's nomination date
p1 <- ggplot(aes(x = date, y = total, color = cand_nm), 
      data = pre_nom) +
      scale_y_log10() +
      ggtitle("Sum of Contributions") +
      geom_jitter(alpha=1/10) + 
      geom_smooth(method="loess") # noisy

# Count of Monetary Contributions for 'Real' cadidates before Romney's nomination date
p2 <- ggplot(aes(x = date, y = n, color = cand_nm), 
      data = pre_nom) +
      scale_y_log10() +
      ggtitle("# of Contributions") +
      geom_jitter(alpha=1/10) + 
      geom_smooth(method="loess") # still noisy

grid.arrange(p1, p2)

# Let's look at cumulative numbers for contributions over the course of the campaign
# And I want to see it all the way through to election day
pre_elec <- filter(data, date < elec_date, cand_nm %in% for_real) %>%
      group_by(cand_nm, date) %>%
      summarize(n = n(), total = sum(contb_receipt_amt)) %>%
      mutate(cumn = cumsum(n), cumtotal = cumsum(total))

# Sum of Monetary Contributions for 'Real' cadidates before Romney's nomination date
p1 <- ggplot(aes(x = date, y = cumtotal, color = cand_nm), 
      data = pre_nom) +
      scale_y_log10() +
      ggtitle("Cumsum of Contributions") +
      geom_jitter(alpha=1/10) + 
      geom_smooth(method="loess")

# Count of Monetary Contributions for 'Real' cadidates before Romney's nomination date
p2 <- ggplot(aes(x = date, y = cumn, color = cand_nm), 
      data = pre_nom) +
      scale_y_log10() +
      ggtitle("Cum # of Contributions") +
      geom_jitter(alpha=1/10) + 
      geom_smooth(method="loess")

grid.arrange(p1, p2) # Yes! Now this looks like race data to me!

# Super telling. Romney raised more total money... but Obama had more contributions
# Those last two should be used for final graphs

# Benchmark -- it looks like republicans raise more money per donations
# Benchmark -- it looks like romney was always the republican front runner
# Benchmark -- it looks like the guy with most cumulative contributions (but not cumulative sum of those donation) won FL -- Barak

# Is there a clear difference among zip codes where donations are going?
by_zip <- filter(data, party %in% c("democrat", "republican")) %>%
      group_by(zip, party) %>%
      summarize(n = n(), total = sum(contb_receipt_amt)) %>%
      mutate(pct = n/sum(n))

ggplot(by_zip, aes(x=zip, y=pct, fill=party)) +
      geom_bar(stat='identity') +
      scale_fill_manual(values=c("blue", "red"))

# Beautiful -- this should also be a final graphic... now how about the same information on a map?

formap <- left_join(by_zip, zipcode, by='zip') # Ahh, let's drop these GA and other values

formap_dem <- subset(formap, party == "democrat")

formap_dem$dom_party <- ifelse(formap_dem$pct > 0.5, c("Democrat"), c("Republican")) # So if more people contributed to Democrat in this zip... it becomes a democrat zip

ggplot(aes(x=longitude, y=latitude, colour=dom_party), data=formap_dem) + geom_point() + scale_color_manual(values=c("blue", "red"))
# Yes, makes sense... contributions to democrats (blue / Obama) dominate the map

# Back to occupation -- similar analysis as by zip code
by_occ <- filter(data, party %in% c("democrat", "republican")) %>%
      group_by(contbr_occupation, party) %>%
      summarize(n = n(), total = sum(contb_receipt_amt)) %>%
      mutate(pct = n/sum(n))

ggplot(by_occ, aes(x=contbr_occupation, y=pct, fill=party)) +
      geom_bar(stat='identity') +
      scale_fill_manual(values=c("blue", "red"))
      # Shows same theme -- some occupations way democrat, some way republican, most lean democrat
      # Depending upon graphs.. we might also use this and then build a better map for zip codes

# Further exploration before modeling data...

# Great now let's see if the donation histogram by candidate changes removing those 2 months of data
# Ahh... 100 seems to be mode followed by 50, 250, 25... all nice easy numbers

# Not really.. I wonder what donations looked like over time to these candidates
don_by_date <- subset(data, contb_receipt_amt > 0 & contb_receipt_amt < 15000) %>%
       group_by(cand_nm, date) %>%
       summarize(donation = sum(contb_receipt_amt))

ggplot(aes(x=date, y=donation),
      data = don_by_date) +
      geom_line() +
      geom_vline(xintercept = as.numeric(nom_date), color = "red", linetype = 'longdash') +
      facet_wrap(~cand_nm)
      # Evident who left race early... also evident that Mitt got a lot of money after he was nominated as Republican nominee

# What if we look at average (measured by median) donation instead of sum by day?
don_by_date <- subset(data, contb_receipt_amt > 0 & contb_receipt_amt < 15000) %>%
      group_by(cand_nm, date) %>%
      summarize(donation = median(contb_receipt_amt))

ggplot(aes(x=date, y=donation), # Donation size got smaller as time went on..
      data = don_by_date) +
      geom_line() +
      geom_vline(xintercept = as.numeric(nom_date), color = "red", linetype = 'longdash') +
      facet_wrap(~cand_nm) +
      scale_y_log10() +
      geom_smooth()

# Final thing on this... look at number of donations
don_by_date <- filter(data, contb_receipt_amt > 0 & contb_receipt_amt < 15000 & date < elec_date) %>%
      group_by(cand_nm, date) %>%
      summarize(donation = n())

ggplot(aes(x=date, y=donation),
      data = don_by_date) +
      geom_jitter(alpha = 1/20) +
      geom_vline(xintercept = as.numeric(nom_date), color = "red", linetype = 'longdash') +
      geom_vline(xintercept = as.numeric(elec_date), color = "green", linetype = 'longdash') +      
      facet_wrap(~cand_nm) +
      scale_y_log10() +
      geom_smooth()
      # Two.. are not like the others...
      # This is most interesting thing I've seen. Using a linear trend... Mitt, Barak, and Ron Paul, Newt, and Santorum all had increased popularity 

# I want to take out the donations that are processed after the election... and then run this again...

# We see that the # of donations tells us a lot -- Mitt and Barak obvious finalists... and Ron Paul also had a lot of support.

# Create a percentage table with occupation as x axis and candidate as y axis

# Who raised the most money?
group_by(data, cand_nm) %>% summarize(money = sum(contb_receipt_amt))

p1 <- ggplot(aes(x=reorder(cand_nm, -money), y=money), 
      data = group_by(data, cand_nm) %>% summarize(money = sum(contb_receipt_amt))) +
      geom_bar(stat="identity") +
      ggtitle("Total Contributions") +
      coord_flip()

# What about contributions per contributor?
p2 <- ggplot(aes(x=reorder(cand_nm, -mean_money), y=mean_money), 
      data = group_by(data, cand_nm) %>%
             summarize(mean_money = mean(contb_receipt_amt))) +
      geom_bar(stat="identity") +
      ggtitle("$ per Contributor") +
      coord_flip() # Proximity of Obama on this list is impressive. Grassroots?

grid.arrange(p1, p2, ncol = 1)

# And this begs the question about Perry...
top_4 <- c("Perry, Rick", "Romney, Mitt", "Obama, Barack", "Paul, Ron")
ggplot(aes(x=contb_receipt_amt), data = filter(data, cand_nm %in% top_4)) +
      geom_histogram() +
      facet_wrap(~cand_nm) +
      scale_y_log10() # no value makes it look negative
      # Obama and Romney have similar contribution pattern.. Romney just a little higher

# Found this: http://www.nytimes.com/2015/05/03/us/politics/fec-cant-curb-2016-election-abuse-commission-chief-says.html

# Very different than what I thought. Suspected big hitteres get more 'big' contributions while the smaller guys get more small contributions. Opposite looks true.

by_zip <- filter(data, party %in% c("democrat", "republican")) %>%
      group_by(zip, party) %>%
      summarize(n = n(), total = sum(contb_receipt_amt)) %>%
      mutate(pct = n/sum(n))

# Fuck it. Let's model 

# 1. Logistic reagression to predict which party the person contributed to

set.seed(1234)
samp <- sample_n(data, 100000)

## 75% of the sample size
smp_size <- floor(0.75 * nrow(samp))

## set the seed to make your partition reproductible
set.seed(1234)
train_ind <- sample(seq_len(nrow(samp)), size = smp_size)

train <- samp[train_ind, ]
test <- samp[-train_ind, ]

model <- glm(as.factor(party) ~ loc + contb_receipt_amt + over200,
             data = train,
             family = "binomial")

predicted_probs = predict(model, test, type="response")
predicted_party = rep("democrat", nrow(test))
predicted_party[predicted_probs > 0.5] = "republican"

table(predicted_party, test$party)
mean(predicted_party != test$party)

########

data$retired <- ifelse(data$contbr_occupation == "RETIRED", "YES", "NO")
test <- table(data$retired, data$party)
prop.table(test, 2)