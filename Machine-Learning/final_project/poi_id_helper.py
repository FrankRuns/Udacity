#!/usr/bin/python

### supplement to poi_id.py
### considering this the playground
### considering this the messy work file

# cd /Users/frankCorrigan/Udacity/Machine-Learning/ud120-mini-projects/tools
# cd /Users/frankCorrigan/Udacity/Machine-Learning/ud120-mini-projects/final_project

# Pre-conceptions on who may be a point of interest
# 1. People that get more incentives - bigger salary, bonus, options, etc.
# 2. People in the center of communication - lots of emails
# The first half of feature selection is really going to be sort 
# of a univariate analysis against poi. I need to know if A) there 
# are outliers (should I remove) and B) if there are patterns against
# poi (for instance maybe only poi got loan advances)

# Does it make sense to take out Skilling / Fastow / Lay...
# Ratio of messages sent to messages received
# 

# EDA: Initial Exploratory Data Analysis

# What does a single entry look like?
# How many features does each entry contain?
data_dict.itervalues().next()
len(data_dict.itervalues().next())
# 21


# How many people are in the data?
len(data_dict) 
# 146


# How many people are poi's?
pois = 0
for key, val in data_dict.iteritems():
	if val['poi'] == True:
		pois +=1
print(pois) # 18 or 146 or 12%


# Which fields have many missing values?
# I would love some coach input on this block of code...
countMissing = {}
for key, val in data_dict.iteritems():
	for i, j in val.iteritems():
		if j == "NaN":
			if i not in countMissing:
				countMissing[i] = 1
			else:
				countMissing[i] += 1
# Only 20 features in countMissing, but there are 21 features
for el in data_dict.itervalues().next().keys():
	if el not in countMissing.keys():
		print el # 'poi'
# Makes sense since all 146 were manually identified as poi or not





# Remove outliers
missingByPerson = {}
for key, val in data_dict.iteritems():
    for i, j in val.iteritems():
        # print key, i , j
        if j == "NaN":
            if key not in missingByPerson:
                    missingByPerson[key] = 1
            else:
                    missingByPerson[key] += 1

lotsOfMissing = []
for key, val in missingByPerson.iteritems():
    if val >= 16:
        lotsOfMissing.append(key) # Results in 15% of the observations

for key, val in data_dict.iteritems():
	if key in lotsOfMissing:
		print key, val['poi'] # All these people are not POIs

my_dataset = data_dict
features_list = ['poi', 'salary', 'to_messages', 'deferral_payments', 
				 'total_payments', 'exercised_stock_options',
				 'bonus', 'restricted_stock', 'shared_receipt_with_poi', 
				 'total_stock_value', 'expenses', 'loan_advances', 'from_messages', 
				 'other', 'from_this_person_to_poi', 
				 'director_fees', 'long_term_incentive',
				 'from_poi_to_this_person']


# To identify outlier, I am going to use a two step process
# 1. Use sklearn select percentile to identify best features
# 2. Plot top features to visually identify outliers
# 3. Repeat if necessary to make sure select percentile remains same

# exercised_stock_options, restricted_stock, total_payments, total_stock_value
# director_fees, restricted_stock_deferred 

# only 6 of 21 features falls into our initial NaN criteria...

# going to make data exploration easier by converting
# dictionary to pandas dataframe
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# need this library for ggplot-ish figures
import matplotlib
matplotlib.style.use('ggplot')

# dictionary to dataframe
pdata = pd.DataFrame.from_dict(data_dict, orient='index')

# start by making NaN true NaN rather than string NaN
pdata = pdata.replace("NaN",np.nan, regex=True)

pdata = pdata.replace(np.nan,0, regex=True)

# followed by getting rid of total observation
pdata = pdata[pdata.index != 'TOTAL']

# remove outliers. basng this on financial data -- total payouts
# for each person, what percent of features are NaN?
missingByPerson = {}
for key, val in data_dict.iteritems():
	for i, j in val.iteritems():
		# print key, i , j
		if j == "NaN":
			if key not in missingByPerson:
				missingByPerson[key] = 1
			else:
				missingByPerson[key] += 1

# TODOs:
# examine variable distribution
# look at conditionally colored bar plot
# group by poi and summarize mean/median for that variable

pdata['em_ratio'] = pdata['to_messages'] / pdata['from_messages']
pdata['poi_mails'] = pdata['from_this_person_to_poi'] + pdata['from_poi_to_this_person'] + pdata['to_messages'] + pdata['from_messages']
pdata['s_ratio'] = pdata['exercised_stock_options'] / pdata['salary']
pdata['all_mail'] = pdata['from_poi_to_this_person'] / pdata['from_this_person_to_poi'] pdata['from_poi_to_this_person'] ) / ( pdata['to_messages'] + pdata['from_messages'] )

pdata_dict = pdata.T.to_dict()

avgSal = pdata['salary'].values.mean()
topEarners = pdata.loc[pdata.salary > avgSal]
foi = 'all_mail'
pdata.sort([foi], ascending=False)[['poi', foi]]
topEarners.sort([foi], ascending=False)[['poi', foi]]

pdata = pdata[pdata.index != 'BLACHMAN JEREMY M']
pdata = pdata[pdata.index != 'FREVERT MARK A']
pdata = pdata[pdata.index != 'LAY KENNETH L']

import seaborn as sns
_ = sns.pairplot(pdata[:50], vars=['salary', 'bonus'], size=1.5)

# shared_receipt_with_poi is probably a good one
# take out blackman jeremy

# share_reciept_with_poi
# em_ratio (to_message / from_message)
# bonus

# em_ratio good predictor?

# bonus -- higher bonus

# from poi to this person -- lots for John Lavorato - not a poi himself

# salary - not really
# bonus - not really
# total_payments - maybe

bypoi = pdata.groupby(['poi'])
bypoi[foi].mean()

# median for long term incentive super different between pois and non-pois

k1 = df.loc[(df.Product == p_id) & (df.Time >= start_time) & (df.Time < end_time), ['Time', 'Product']]

d1 = pdata[~np.isnan(pdata[foi])].copy

import matplotlib.pyplot as plt
x = pdata[foi].values
y = pdata['salary'].values
plt.scatter(x, y)

colours = colorMaker(n=3)
pdata[['poi']] = pdata[['poi']].astype(float)
pdata.plot(kind='scatter', x='salary', y='bonus')

nph = np.histogram(data2[foi][~np.isnan(data2[foi])].values)
plt.hist(nph)
plt.show()

# TODO: how do I conditionally color these bars poi/non-poi
data2[foi][~np.isnan(data2[foi])].plot(kind='bar')
plt.show()

by_poi = data2.groupby(['poi'])
by_poi[foi].describe()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
pdata_scaled = pd.DataFrame(scaler.fit_transform(pdata), columns=pdata.salary)

min_max_scaler = MinMaxScaler()
sal_minmax = min_max_scaler.fit_transform(pdata['salary'])
lti_minmax = min_max_scaler.fit_transform(pdata['long_term_incentive'])
bon_minmax = min_max_scaler.fit_transform(pdata['bonus'])
bon_er = np.array(pdata['total_payments'])
poi_er = np.array(pdata['poi'].astype(float))
plt.scatter(x=sal_minmax, y=lti_minmax, c=poi_er, s=50)

from matplotlib import pyplot as plt
plt.scatter(,Y1,color='red')
plt.scatter(X,Y2,color='blue')
plt.show()

groups = pdata.groupby('poi')
fig, ax = plt.subplots()
ax.margins(0.05)
for name, group in groups:
    ax.plot(group.to_messages, group.from_poi_to_this_person, marker='o', linestyle='', ms=12, label=name)
ax.legend()
plt.show()


