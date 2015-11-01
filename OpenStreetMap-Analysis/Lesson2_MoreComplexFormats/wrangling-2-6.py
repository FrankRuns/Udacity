with open('error.xml', 'r') as xfile:
	data = xfile.read()

data = data.split('<?xml version="1.0" encoding="UTF-8"?>')

for el in data:
	el = '<?xml version="1.0" encoding="UTF-8"?>' + el



def files():
	n = 0
	while True:
		yield open('{}{}'.format('PATENTS',n), 'wb')
		n+=1
		
pat = '<?xml version="1.0" encoding="UTF-8"?>'
fs = files()
outfile = next(fs)

with open('error.xml') as infile:
    for line in infile:
        if pat not in line:
            outfile.write(line)
        else:
        	items = line.split(pat)
        	print items
        	outfile.write(items[0])
        	for item in items[1:]:
        		outfile = next(fs)
        		outfile.write(pat + item)



with open('error.xml') as xfile:
	data = xfile.readlines()

count = 0
for el in data:
	if el.replace('\n','') == '<?xml version="1.0" encoding="UTF-8"?>':
		outfile = open('{}-{}'.format(filename, count), 'wb')
		print outfile.name
		outfile.write(el)
		count += 1
	else:
		outfile.write(el)
outfile.close()





locs = []
count = 0
loc_count = 0
for el in data:
	if el.replace('\n','') == '<?xml version="1.0" encoding="UTF-8"?>':
		locs.append(loc_count)
		count += 1
	loc_count += 1

with open('error.xml', 'r') as xfile:
	count = 0
	for line in xfile:
		if count in loc_count:
			

