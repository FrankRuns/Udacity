#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        clean away the 10% of points that have the largest
        residual errors (different between the prediction
        and the actual net worth)

        return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error)
    """
    
    cleaned_data = []

    ### your code goes here

    ### calc errors
    errors = (predictions - net_worths)**2
    
    ### find the val
    s = []
    for el in errors:
        s.append(el[0])
    s.sort()
    theval = s[len(s)-10]

    ### get error indexes of figures > theval
    indies = []
    count = 0
    for el in errors:
        if el[0] > theval:
            indies.append(count)
        count += 1

    ### remove indies from ages, net_worth, and error
    ages = numpy.delete(ages, indies)
    net_worths = numpy.delete(net_worths, indies)
    errors = numpy.delete(errors, indies)

    ### create tuple
    for i in range(81):
        cleaned_data.append((ages[i], net_worths[i], errors[i]))

    return cleaned_data

