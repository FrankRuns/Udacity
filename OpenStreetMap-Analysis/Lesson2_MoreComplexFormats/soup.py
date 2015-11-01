from bs4 import BeautifulSoup
import requests
import json

with open('soup-test.html', 'r') as html:
    soup = BeautifulSoup(html, 'html.parser')

print soup.find(id="__EVENTVALIDATION").get('value')
print soup.find(id="__VIEWSTATE").get('value')

# def extract_data(page):
#     data = {"eventvalidation": "",
#             "viewstate": ""}
#     with open(page, "r") as html:
#         soup = BeautifulSoup(html, 'html.parser')
#         pass

#     print soup
#     return data



# def make_request(data):
#     eventvalidation = data["eventvalidation"]
#     viewstate = data["viewstate"]

#     r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
#                     data={'AirportList': "BOS",
#                           'CarrierList': "VX",
#                           'Submit': 'Submit',
#                           "__EVENTTARGET": "",
#                           "__EVENTARGUMENT": "",
#                           "__EVENTVALIDATION": eventvalidation,
#                           "__VIEWSTATE": viewstate
#                     })

#     return r.text


# def test():
#     data = extract_data(html_page)
#     assert data["eventvalidation"] != ""
#     assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
#     assert data["viewstate"].startswith("/wEPDwUKLTI")

    
# test()