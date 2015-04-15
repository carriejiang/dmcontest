import csv
import re
from sets import Set

def readCat(TRAINED_CAT):
	"""
	Load the trained cat and iterate through
	"""
	
	# dictionary of cat -> RSD
	setTrainedRSD = {}
	trainedRSD = {}
	numKnowncat = 0
	

	with open(TRAINED_CAT, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
		next(csvreader, None)  # skip the headers
        
		for row in csvreader:
			item_type, item_id, item_descriptor, count, username, log_id, sector, dept, majorCat, cat, subcat = row
            
			if (not majorCat) or (majorCat.upper() in Set(['ISC_UNKNOWN','ISC_NON_ITEM'])):
				continue
			else:
				numKnowncat += int(count)
				# put RSD in dictionary, key = cat, value = RSD
				if majorCat.upper() in trainedRSD:
					trainedRSD[majorCat.upper()].append((item_descriptor.upper(),int(count)))
					setTrainedRSD[majorCat.upper()].add(item_descriptor.upper())
				else:
					trainedRSD[majorCat.upper()] = [(item_descriptor.upper(),int(count))]
					setTrainedRSD[majorCat.upper()] = Set(item_descriptor.upper())
					                
	return trainedRSD, setTrainedRSD, numKnowncat
                    

if __name__ == "__main__":
    read()
