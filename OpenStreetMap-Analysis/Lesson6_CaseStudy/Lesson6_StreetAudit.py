"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# This is where we map the 'incorrect' with the correct
mapping = { "St.": "Street",
            "Ave" : "Avenue",
            "Rd." : "Road"
            }

# Used by audit. Use regex to get the street label from the name. For example, get Ave. from North Lincoln Ave.
# Add to disciotnary in form 'street_label: [list is street names with this label]'
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# Used by audit. If tag has addr:street attribute, return it.
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# Start here
# Read osm file, declare a dictionary for unexpected street labels
# Look through tags that have a 'addr:street' attribute
# Store street type and name in street_types dictionary
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

# After audit, use this to update street names using mapping. For instance, N. Lincoln Ave. should become N. Lincoln Avenue
def update_name(name, mapping):
    target = None
    for key in mapping.keys():
        if key in name:
            target = key

    name = name.replace(target, mapping[target])

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()