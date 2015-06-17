import pandas as pd
import numpy as np
import datetime
import scipy
import statsmodels.api as sm
from ggplot import *
import random

# Load improved data set
df = pd.read_csv('improved-data.csv')

# Remove outliers defined as hourly entries 3 standard deviations away from the mean
data = df[np.abs(df.ENTRIESn_hourly-df.ENTRIESn_hourly.mean())<=(3*df.ENTRIESn_hourly.std())]

# Convert date to datetime object and create is_weekend variable where weekend is Fri, Sat, Sun
data['DATEn'] = map(lambda x: datetime.datetime.strptime(x, '%m-%d-%y'), data['DATEn'])
data['DayOfWeek'] = map(lambda x: x.weekday(), data['DATEn'])
data['isWeekend'] = (data['DayOfWeek'] == 0) | (data['DayOfWeek'] == 6) | (data['DayOfWeek'] == 5)
data['isWeekend'] = map(lambda x: int(x), data['isWeekend'])

# Create 'week ago' variable
helper = []
for el in data['UNIT'].unique():
    helper.append(data[data['UNIT'] == el])
for el in helper:
    el['offset_entries_week'] = el['ENTRIESn_hourly'].diff(42)
data = helper[0]
count = 1
for df in helper[1:]:
    data = pd.DataFrame.append(data, df)

# Create 'day before' variable
helper = []
for el in data['UNIT'].unique():
    helper.append(data[data['UNIT'] == el])
for el in helper:
    el['offset_entries_day'] = el['ENTRIESn_hourly'].diff(7)
data = helper[0]
count = 1
for df in helper[1:]:
    data = pd.DataFrame.append(data, df)

# Drop rows where prior entries is Nan
data = data.dropna()

# Statistical Testing

# Run the Mann Whitney U-test on sample of entries data for rain and no rain observations
random.seed(1234)
def test_rain(data):
	rain_med = 0
	norain_med = 0
	val = 0
	p_roll = 0
	# Perform mwut on 10 samples of subway data
	for i in range(100):
		# Sample 4,999 rows from dataset (to avoid 'overpowering')
		rows = random.sample(data.index, 4999)
		data_4999 = data.ix[rows]
		# Create rain / norain sub-datasets
		rain = data_4999[data_4999['rain'] == 1]
		norain = data_4999[data_4999['rain'] == 0]
		# Test for normality (or lack thereof)
		scipy.stats.shapiro(rain['ENTRIESn_hourly']) 
		scipy.stats.shapiro(norain['ENTRIESn_hourly'])
		# Find medians for each set
		with_rain_median = np.median(rain['ENTRIESn_hourly'])
		rain_med = rain_med + with_rain_median
		without_rain_median = np.median(norain['ENTRIESn_hourly'])
		norain_med = norain_med + without_rain_median
		# Run Mann Whitney U-test to determine similarity / difference in distributions
		mw_val, pval = scipy.stats.mannwhitneyu(rain['ENTRIESn_hourly'], norain['ENTRIESn_hourly'])
		val = val + mw_val
		p_roll = p_roll + pval
	return rain_med / 100, norain_med / 100, val / 100, p_roll / 100

# Run the Mann Whitney U-test on sample of entries data for weekend and weekday observations
random.seed(1234)
def test_weekend(data):
	weekend_med = 0
	weekday_med = 0
	val = 0
	p_roll = 0
	# Perform mwut on 10 samples of subway data
	for i in range(100):
		# Sample 4,999 rows from dataset (to avoid 'overpowering')
		rows = random.sample(data.index, 4999)
		data_4999 = data.ix[rows]
		# Create rain / norain sub-datasets
		weekend = data_4999[data_4999['isWeekend'] == 1]
		weekday = data_4999[data_4999['isWeekend'] == 0]
		# Test for normality (or lack thereof)
		scipy.stats.shapiro(weekend['ENTRIESn_hourly']) 
		scipy.stats.shapiro(weekday['ENTRIESn_hourly'])
		# Find medians for each set
		weekend_median = np.median(weekend['ENTRIESn_hourly'])
		weekend_med = weekend_med + weekend_median
		weekday_median = np.median(weekday['ENTRIESn_hourly'])
		weekday_med = weekday_med + weekday_median
		# Run Mann Whitney U-test to determine similarity / difference in distributions
		mw_val, pval = scipy.stats.mannwhitneyu(weekend['ENTRIESn_hourly'], weekday['ENTRIESn_hourly'])
		val = val + mw_val
		p_roll = p_roll + pval
	return weekend_med / 100, weekday_med / 100, val / 100, p_roll / 100

# Predictions with Linear Regression

# Normalize features for linear regression model
def normalize_features(features):
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

# Recover un-normalized parameters for interpretation
def recover_params(means, std_devs, norm_intercept, norm_params):
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

# Buld linear regression model
def linear_regression(features, values):
    X = sm.add_constant(features)  
    model = sm.OLS(values, X)
    result = model.fit()
    intercept = result.params[0]
    params = result.params[1:]   
    print result.summary()
    return intercept, params

# Calculate predictions from model and generate r^2 value
def calc_r_squared(dataframe):
    features = dataframe[['isWeekend', 'hour', 'offset_entries_week', 'offset_entries_day']]
    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    # Values
    values = dataframe['ENTRIESn_hourly']
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values
    # Normalize and store features
    means, std_devs, normalized_features_array = normalize_features(features_array)
    # Perform regression
    norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
    # Recover non-normalized parameters
    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    # Make predictions
    predictions = intercept + np.dot(features_array, params)
    # Calculate r^2
    SSR = ((values - predictions)**2).sum()
    SST = ((values - np.mean(values))**2).sum()
    r_squared = 1 - (SSR/SST)
    
    return r_squared

# Visualizations

# Create an entries histogram split by rain and no rain
ggplot(aes(x='ENTRIESn_hourly', color='rain'), data=data) +\
    geom_histogram() +\
    ggtitle('Histogram of Hourly Subway Entries') +\
    labs('Entries', 'Freq')

# Daily Entries Line Chart
byDate = data['ENTRIESn_hourly'].groupby(data.DATEn).sum()
byDate.index.name = 'thedate'
byDate = byDate.reset_index()
longdf = pd.melt(byDate, id_vars=['thedate'])
ggplot(aes(x='thedate', y='value', colour='variable'), data=longdf) +\
    geom_line() +\
    scale_x_date(breaks=date_breaks('2 day'), labels='%b %d %Y') +\
    scale_y_continuous(labels='comma') +\
    xlab('Date') +\
    ylab('Daily Entries') +\
    ggtitle('NYC Daily Subway Entries: May 2011')

# Week Ago Scatterplot
# Remember to re-read original data since we removed week one for the week over week difference

# First need to get # of entries from one week prior
helper = []
for el in data['UNIT'].unique():
    helper.append(data[data['UNIT'] == el])
for el in helper:
    el['week_ago'] = el['ENTRIESn_hourly'].shift(42)
data = helper[0]
count = 1
for df in helper[1:]:
    data = pd.DataFrame.append(data, df)
data = data.dropna()

# Now we can create scatter plot between entries today and entries one week prior colored by whether the day is a weekend or not
byDate = data[['ENTRIESn_hourly', 'week_ago', 'isWeekend']].groupby(data.DATEn).sum().dropna().reset_index(drop=True)
byDate['isWeekend'] = byDate['isWeekend'] > 0
ggplot(aes(x=byDate['ENTRIESn_hourly'], y=byDate['week_ago'], color='isWeekend'), data=byDate) +\
    geom_point(size=150) +\
    xlab('Daily Entries') +\
    ylab('Week Prior Entries') +\
    ggtitle('Entries versus Week Prior')
