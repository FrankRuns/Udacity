import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy
import scipy.stats
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
def test_rain(data):
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
    without_rain_median = np.median(norain['ENTRIESn_hourly'])
    # Run Mann Whitney U-test to determine similarity / difference in distributions
    # Run Mann Whitney U-test on 100 different samples and find average p-value
    p_roll = 0
    for i in range(1000):
        val, pval = scipy.stats.mannwhitneyu(rain['ENTRIESn_hourly'], norain['ENTRIESn_hourly'])
        p_roll = p_roll + pval
    
    return p_roll / 1000

# Run the Mann Whitney U-test on sample of entries data for weekend and weekday observations
def test_weekend(data):
    # Sample 4,999 rows from dataset (to avoid 'overpowering')
    rows = random.sample(data.index, 4999)
    data_4999 = data.ix[rows]
    # Create rain / norain sub-datasets
    onWeekend = data_4999[data_4999['isWeekend'] == 1]
    notWeekend = data_4999[data_4999['isWeekend'] == 0]
    # Test for normality (or lack thereof)
    scipy.stats.shapiro(onWeekend['ENTRIESn_hourly']) 
    scipy.stats.shapiro(notWeekend['ENTRIESn_hourly'])
    # Find medians for each set
    weekend_median = np.median(onWeekend['ENTRIESn_hourly'])
    weekday_median = np.median(notWeekend['ENTRIESn_hourly'])
    # Run Mann Whitney U-test to determine similarity / difference in distributions
    # Run Mann Whitney U-test on 100 different samples and find average p-value
    p_roll = 0
    for i in range(1000):
        val, pval = scipy.stats.mannwhitneyu(onWeekend['ENTRIESn_hourly'], notWeekend['ENTRIESn_hourly'])
        p_roll = p_roll + pval
    
    return p_roll / 1000

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
plt.figure()
df['ENTRIESn_hourly'][df['rain'] == 0].hist(bins=30)
df['ENTRIESn_hourly'][df['rain'] == 1].hist(bins=30)
plt.show()

# Total entries by day
df['ENTRIESn_hourly'].groupby(df.DATEn).sum().plot()
plt.show()

# Total entries by location
data['ENTRIESn_hourly'].groupby(data.DayOfWeek).median().plot()
plt.show()
