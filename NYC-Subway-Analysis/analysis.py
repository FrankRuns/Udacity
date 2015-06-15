import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy
import scipy.stats
import statsmodels.api as sm
from ggplot import *
import random

# Read the data
def prepare_data(data):
    # Load improved data set
    data = pd.read_csv('improved-data.csv')
    # Remove outliers defined as hourly entries 3 standard deviations away from the mean
    data = data[np.abs(data.ENTRIESn_hourly-data.ENTRIESn_hourly.mean())<=(3*data.ENTRIESn_hourly.std())]
    # Convert date to datetime object and create is_weekend variable where weekend is Fri, Sat, Sun
    data['DATEn'] = map(lambda x: datetime.datetime.strptime(x, '%m-%d-%y'), data['DATEn']) 
    data['DayOfWeek'] = map(lambda x: x.weekday(), data['DATEn'])
    data['isWeekend'] = (data['DayOfWeek'] == 0) | (data['DayOfWeek'] == 6) | (data['DayOfWeek'] == 5)
    data['isWeekend'] = map(lambda x: int(x), data['isWeekend'])

    # Add variable for temperature range
    # data['temprange'] = data['maxtempi'] - data['mintempi']

    # Add variable for temperature and precipitation difference
    # data['offset_temp'] = data['tempi'].diff()
    # data['offset_temp'].loc[0] = 0
    # data['offset_precip'] = data['precipi'].diff()
    # data['offset_precip'].loc[0] = 0
    # for el in data['UNIT']:
    #     for i in data[data['UNIT'] == el]:
    #         data.loc[:1, 'group'] = 'first-group'
    #         data['offset_entries'][i]
    # data['offset_entries'] = data['ENTRIESn_hourly'].diff(42)
    # for i in range(42):
    #     data['offset_entries'].loc[i] = 0

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

    # Add bucket variable for hour of the day
    # Buckets: 12AM-6AM, 6AM-12PM, 12PM-6PM, 6PM-12AM
    theindex = []
    helper = []
    for index, row in data.iterrows():
        hour = row['hour']
        if hour <= 6:
            theindex.append(0)
            helper.append('12AM-6AM')
        elif hour <= 12:
            theindex.append(1)
            helper.append('6AM-12PM')
        elif hour <= 18:
            theindex.append(2)
            helper.append('12PM-6PM')       
        elif hour <= 24:
            theindex.append(3)
            helper.append('6PM-12AM')

    data['hour_order'] = theindex
    data['hour_chunk'] = helper

    return data

# What is the average temperature on the weekends?
# placeholder = (data['DayOfWeek'] == 6) | (data['DayOfWeek'] == 0)
# np.mean(data[placeholder]['meantempi'])

# Run the Mann Whitney U-test on entries data for rain and no rain observations
def test_rain(data):
    rain = data[data['rain'] == 1]
    norain = data[data['rain'] == 0]

    scipy.stats.shapiro(rain['ENTRIESn_hourly']) 
    scipy.stats.shapiro(norain['ENTRIESn_hourly'])

    with_rain_median = np.median(rain['ENTRIESn_hourly'])
    without_rain_median = np.median(norain['ENTRIESn_hourly'])
    U, p = scipy.stats.mannwhitneyu(rain['ENTRIESn_hourly'], norain['ENTRIESn_hourly'])

    return U, p

# Subsetting sample since throwing warning that p-value may be incorrect with values > 5,000
rows = random.sample(data.index, 4999)
data_4999 = data.ix[rows]
rain = data_4999[data_4999['rain'] == 1]
norain = data_4999[data_4999['rain'] == 0]
with_rain_median = np.median(rain['ENTRIESn_hourly'])
without_rain_median = np.median(norain['ENTRIESn_hourly'])
U, p = scipy.stats.mannwhitneyu(rain['ENTRIESn_hourly'], norain['ENTRIESn_hourly'])

# Run the Mann Whitney U-test on entries data for weekend and weekday observations
def test_weekend(data):
    onWeekend = data[data['isWeekend'] == 1]
    notWeekend = data[data['isWeekend'] == 0]

    scipy.stats.shapiro(onWeekend['ENTRIESn_hourly'])
    scipy.stats.shapiro(notWeekend['ENTRIESn_hourly'])

    # plt.figure()
    # data['ENTRIESn_hourly'][data['isWeekend'] == 0].hist(bins=30)
    # data['ENTRIESn_hourly'][data['isWeekend'] == 1].hist(bins=30)
    # plt.show() # these are skewed
    weekend_median = np.median(onWeekend['ENTRIESn_hourly'])
    weekday_median = np.median(notWeekend['ENTRIESn_hourly'])
    U, p = scipy.stats.mannwhitneyu(onWeekend['ENTRIESn_hourly'], notWeekend['ENTRIESn_hourly'])

    return U, p

def normalize_features(features):
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    X = sm.add_constant(features)  
    # formula = 'ENTRIESn_hourly ~ isWeekend + Hour + rain + precipi + C(UNIT)' 
    # model = sm.OLS(formula=formula, data=data)
    model = sm.OLS(values, X)
    result = model.fit()
    intercept = result.params[0]
    params = result.params[1:]   
    print result.summary()
    return intercept, params

def calc_r_squared(dataframe):
    features = dataframe[['isWeekend', 'hour', 'offset_entries_week', 'offset_entries_day']]
    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    # Add hour_chunk to features using dummy variables
    # dummy_units = pd.get_dummies(dataframe['rain'], prefix='rain')
    # features = features.join(dummy_units)
    # # Add hour_chunk to features using dummy variables
    # dummy_units = pd.get_dummies(dataframe['conds'], prefix='conds')
    # features = features.join(dummy_units)
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


# What are we really interested in in this dataset?
# Entries --- time/date of the entry, location of the entry, rain/temp/precip/wind
# Show me the distributions of each variable
# Show me the distributions of each varaible grouped by rain/norain
# Show me the averages of entries grouped by variables above (time/date, location, weather)
# It makes sense to run t-tests on these averages

# We need to remove outliers
# Break date into month and day of week

# This is only a month of data... so forget stripping out month
# Create linear regression using entries as y and
# Unit, day of week, time of day, rain, meanwindspdi, meantempi, precipi

 
# Trying visualizations

# Total entries by day
data['ENTRIESn_hourly'].groupby(data.DATEn).sum().plot()
plt.show()

# Create a entries histogram split by rain and no rain
plt.figure()
data['ENTRIESn_hourly'][data['rain'] == 0].hist(bins=30)
data['ENTRIESn_hourly'][data['rain'] == 1].hist(bins=30)
plt.show()


mini = onWeekend.ix[:,['Hour', 'ENTRIESn_hourly']]
grouped = mini.groupby(['Hour'])
g_weekend = grouped.aggregate(np.sum)

mini = notWeekend.ix[:,['Hour', 'ENTRIESn_hourly']]
grouped = mini.groupby(['Hour'])
g_notweekend = grouped.aggregate(np.sum)

both_g = pd.concat([g_weekend, g_notweekend], axis=1)
both_g.columns = ['weekend', 'notweekend']

both_g['x'] = both_g.index
data = pd.melt(both_g, id_vars = 'x')
ggplot(aes(x='x', y='value', color='variable'), data) + geom_line()

fig = plt.figure()
plt.bar(both_g.index, both_g['weekend'], color='b')
plt.bar(both_g.index, both_g['notweekend'], color='g')
plt.show()

thething = both_g.groupby('ind').mean()

import pandas as pd

weekend = [2.464, 1.247, 0.113, 0.026, 0.705, 0.366, 0.540]
weekday = [8.343, 3.721, 0.314, 0.054, 1.733, 0.813, 0.128]
data = {'weekend': weekend,
        'weekday': weekday }

data = pd.dataFrame(data)

helper = []
for index, blank in data.iterrows():
    if index <= 1:
        helper.append('first-group')
    elif index <= 4:
        helper.append('second-group')
    elif index <= 6:
        helper.append('third-group')

data['group'] = helper

theindex = []
helper = []
for index, hour in both_g.iterrows():
    if index <= 3:
        theindex.append(0)
        helper.append('12AM-3AM')
    elif index <=7:
        theindex.append(1)
        helper.append('4AM-7AM')
    elif index <=11:
        theindex.append(2)
        helper.append('8AM-11AM')       
    elif index <=15:
        theindex.append(3)
        helper.append('12PM-3PM')
    elif index <=19:
        theindex.append(4)
        helper.append('4PM-7PM')
    elif index <=23:
        theindex.append(5)
        helper.append('8PM-12PM')

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
 
map = Basemap(projection='merc', lat_0 = 57, lon_0 = -135,
    resolution = 'h', area_thresh = 0.1,
    llcrnrlon=-136.25, llcrnrlat=56.0,
    urcrnrlon=-134.25, urcrnrlat=57.75)
 
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'coral')
map.drawmapboundary()
 
plt.show()
