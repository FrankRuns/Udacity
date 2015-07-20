# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data"
outfile = "2013_Max_Loads.csv"

# Unzip the excel file
def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

# Create dictionary for max data and dates
def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile+'.xls')
    sheet = workbook.sheet_by_index(0)

    # Create a list of our dates
    dates = []
    for i in range(1, sheet.nrows):
        dates.append(xlrd.xldate_as_tuple(sheet.cell(i,0).value, 0))

    # Create list of geographic locations
    locs = sheet.row(0)[1:9]

    # Populate data list with required data
    data = []
    count = 1
    for el in locs:
        helper = []
        for i in range(1, sheet.nrows):
            helper.append(sheet.cell(i,count).value)
        val = max(helper)
        idx = helper.index(val)
        date = dates[idx]
        data.append([el, date, val])
        count += 1           

    # Return list
    return data

def save_file(filename):
    data = parse_file(datafile)
    with open(filename, 'wb') as thefile:
        w = csv.writer(thefile, delimiter = ',', quotechar = '|')
        w.writerow(['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'])
        for i in range(len(data)):
            w.writerow([data[i][0].value, data[i][1][0], data[i][1][1], data[i][1][2], data[i][1][3], data[i][2]])

def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line[s'Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()


with open(outfile) as of:
    csvfile = csv.DictReader(of, delimiter=",")
    for line in csvfile:
        station = line['Station']
        print station