#!/usr/bin/python

import numpy
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
from studentReg import studentReg
from class_vis import prettyPicture, output_image

from ages_net_worths import ageNetWorthData

ages_train, ages_test, net_worths_train, net_worths_test = ageNetWorthData()



reg = studentReg(ages_train, net_worths_train)

km_net_worth = reg.predict([27])[0]
print('katies net worth: ', km_net_worth)

slope = reg.coef_[0][0]
print('slope: ', slope)

intercept = reg.intercept_[0]
print('intercept: ', intercept)

test_score = reg.score(ages_test, net_worths_test) 
print('r-squared: ', test_score)

plt.clf()
plt.scatter(ages_train, net_worths_train, color="b", label="train data")
plt.scatter(ages_test, net_worths_test, color="r", label="test data")
plt.plot(ages_test, reg.predict(ages_test), color="black")
plt.legend(loc=2)
plt.xlabel("ages")
plt.ylabel("net worths")


plt.savefig("test.png")
output_image("test.png", "png", open("test.png", "rb").read())
