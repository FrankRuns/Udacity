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

data$date <- as.Date(data$contb_receipt_dt, format = "%d-%b-%y")

nom_date <- as.Date("28-AUG-12", format = "%d-%b-%y")

elec_date <- as.Date("06-NOV-12", format = "%d-%b-%y")

data$days_from_elec <- as.integer(elec_date - data$date)

data <- subset(data, cand_nm != "Stein, Jill" & cand_nm != "McCotter, Thaddeus G") # Removes 46 observations

data$party <- ifelse(data$cand_nm == "Obama, Barack", c("democrat"), c("republican")) 

data$party[data$cand_nm == "Johnson, Gary Earl"] <- "libertarian"

data$party[data$cand_nm == "Roemer, Charles E. 'Buddy' III" | data$cand_nm == "Stein, Jill"] <- "other"

library(zipcode) # https://cran.r-project.org/web/packages/zipcode/

data$zip = clean.zipcodes(data$contbr_zip) # Leaves us with many 9-digit zips. Shorten to 5-digit zips.

data$zip = substr(data$zip, 1, 5)

data <- subset(data, zip >= 30000 & zip < 40000) # We lose 423 observations

data(zipcode)

data <- left_join(data, zipcode, by="zip")

data <- filter(data, state == "FL")

occ_count <- data %>%
      group_by(contbr_occupation) %>%
      summarize(n=n()) %>%
      filter(n > 30) # this removes roughly 60,000 observations

data <- subset(data, contbr_occupation %in% occ_count$contbr_occupation) # took out contributions for occupations that appear less than 31 times

data <- subset(data, contb_receipt_amt < 25000 & contb_receipt_amt > -25000)

data <- subset(data, contb_receipt_amt < 5000 & contb_receipt_amt > 0)

data$over2700 <- ifelse(data$contb_receipt_amt > 2700, "Large", "Small")
data$over200 <- ifelse(data$contb_receipt_amt > 200, "Large", "Small")

data$loc <- abs(data$latitude * data$longitude)

## Sample dataset first
set.seed(1234)
samp <- sample_n(data, 5000)

## 75% of the sample size for training
smp_size <- floor(0.75 * nrow(samp))

## set the seed to make your partition reproductible
set.seed(1234)
train_ind <- sample(seq_len(nrow(samp)), size = smp_size)

train <- samp[train_ind, ]
test <- samp[-train_ind, ]

## Model time -- prob of donating to republican
model <- glm(as.factor(party) ~ latitude + contb_receipt_amt + over200,
             data = train,
             family = "binomial")

library(aod)
wald.test(b = coef(model), Sigma = vcov(model), Terms = 3)
## Chi-squared test:
## X2 = 8273.1, df = 3, P(> X2) = 0.0
## Meaning contribution size is significant

# Create odds ratios
exp(cbind(OR = coef(model), confint(model)))
##                            OR     2.5 %    97.5 %
##(Intercept)          0.1392128 0.1099123 0.1763128
##loc                  1.0010795 1.0009770 1.0011821
##contb_receipt_amt    1.0007696 1.0007166 1.0008236
##factor(over200)Small 0.2942782 0.2803070 0.3089187

with(model, null.deviance - deviance)
with(model, df.null - df.residual)
with(model, pchisq(null.deviance - deviance, df.null - df.residual, lower.tail = FALSE))
logLik(model)


predicted_probs = predict(model, test, type="response")
predicted_party = rep("democrat", nrow(test))
predicted_party[predicted_probs > 0.5] = "republican"

table(predicted_party, test$party)
mean(predicted_party != test$party)

########

