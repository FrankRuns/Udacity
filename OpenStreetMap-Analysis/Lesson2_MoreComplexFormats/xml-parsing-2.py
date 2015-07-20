#!/usr/bin/env python
# Your task here is to extract data from xml on authors of an article
# and add it to a list, one item for an author.
# See the provided data structure for the expected format.
# The tags for first name, surname and email should map directly
# to the dictionary keys, but you have to extract the attributes from the "insr" tag
# and add them to the list for the dictionary key "insr"
import xml.etree.ElementTree as ET
import pprint

tree = ET.parse('exampleResearchArticle.xml')
root = tree.getroot()

# print "\nChildren of Root"
# for child in root:
# 	print child.tag

# title = root.find('./fm/bibl/title')
# title_text = ""
# for p in title:
# 	title_text += p.text
# print "\nTitle:\n", title_text

# print "\nAuthor email addresses:"
# for a in root.findall('./fm/bibl/aug/au'):
# 	email = a.find('email')
# 	if email is not None:
# 		print email.text

authors = []
for author in root.findall('./fm/bibl/aug/au'):
	data = {
			"fnm": None,
			"snm": None,
			"email": None,
			"insr": []
	}

	data['fnm'] = author.find('fnm').text
	data['snm'] = author.find('snm').text
	data['email'] = author.find('email').text

	for el in author:
		if el.tag == 'insr':
			data['insr'].append(el.attrib['iid'])

	authors.append(data)

print authors
