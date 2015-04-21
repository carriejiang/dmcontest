import csv
import re
from sets import Set

def readBrands(TRAINED_BRANDS):
	"""
	Load the trained brands and iterate through
	"""
	
	# dictionary of brand -> RSD
	setTrainedRSD = {}
	trainedRSD = {}
	numKnownBrands = 0
	

	with open(TRAINED_BRANDS, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
		next(csvreader, None)  # skip the headers
        
		for row in csvreader:
			item_type,item_id,item_descriptor,count,username,log_id,major_brand,medium_brand, \
                	minor_brand,sub_brand,subsub_brand = row
            
			if (not major_brand) or (major_brand.upper() in Set(['INDETERMINATE','PRIVATE_LABEL', 'UNKNOWN'])):
				continue
			else:
				numKnownBrands += int(count)
				# put RSD in dictionary, key = brand, value = RSD
				if major_brand.upper() in trainedRSD:
					trainedRSD[major_brand.upper()].append((item_descriptor.upper(),int(count)))
					setTrainedRSD[major_brand.upper()].add(item_descriptor.upper())
				else:
					trainedRSD[major_brand.upper()] = [(item_descriptor.upper(),int(count))]
					setTrainedRSD[major_brand.upper()] = Set(item_descriptor.upper())
					                
	return trainedRSD, setTrainedRSD, numKnownBrands