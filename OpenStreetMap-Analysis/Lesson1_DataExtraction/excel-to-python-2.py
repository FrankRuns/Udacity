import xlrd

datafile = "ERCOT_2013.xls"

def avg(list):
    sum = 0
    for el in list:
        sum += el
    return sum / len(list)

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    # Create list of coast values
    coast = []

    for i in range(1, sheet.nrows):
        coast.append(float(sheet.cell(i,1).value))

    '''Obtain min and max coast values as well as list index of those values. 
       Also, find the average coast value'''
    peak = max(coast) 
    peak_idx = coast.index(max(coast))
    low = min(coast)
    low_idx = coast.index(min(coast))
    meen = avg(coast)

    # Create list of date values
    dates = []

    for i in range(1, sheet.nrows):
        dates.append(sheet.cell(i,0).value) 

    # Obtain time of occurance for peak and low values as a tuple
    peak_time = xlrd.xldate_as_tuple(dates[peak_idx],0)
    low_time = xlrd.xldate_as_tuple(dates[low_idx], 0)

    # Store desired vals in dict
    data = {
            'maxtime': peak_time,
            'maxvalue': peak,
            'mintime': low,
            'minvalue': low_time,
            'avgcoast': meen 
    }

    return data

data = parse_file(datafile)