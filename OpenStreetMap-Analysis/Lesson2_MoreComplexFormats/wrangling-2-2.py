#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    with open('options.html', "r") as html:
        
        soup = BeautifulSoup(html)

        ports = soup.find(id="AirportList")

        for port in ports.find_all("option"):
        	if len(port.get('value')) == 3 and port.get('value') != 'All':
        		data.append(port.get('value')


    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()