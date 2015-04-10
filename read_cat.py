import csv
import re
from sets import Set

def readCat(TRAINED_CAT):
	"""
	Load the trained brands and iterate through
	"""
	
	# dictionary of brands -> RSD
	trainedRSD = {}

	with open(TRAINED_CAT, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
		next(csvreader, None)  # skip the headers
        
		for row in csvreader:
			item_type, item_id, item_descriptor, count, username, log_id, sector, dept, majorCat, cat, subcat = row
            
			if not majorCat:
				continue
			else:
				# put RSD in dictionary, key = cat, value = RSD
				if majorCat.upper() in trainedRSD:
					trainedRSD[majorCat.upper()].add(item_descriptor.upper())
				else:
					trainedRSD[majorCat.upper()] = Set([item_descriptor.upper()])
	
                
	return trainedRSD
                    

if __name__ == "__main__":
    read()
