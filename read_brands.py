import csv
import re
from sets import Set

def readBrands(TRAINED_BRANDS, BRANDS_LIST):
	"""
	Load the trained brands and iterate through
	"""
	
	# dictionary of brands -> RSD
	trainedRSD = {}

	with open(TRAINED_BRANDS, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
		next(csvreader, None)  # skip the headers
        
		for row in csvreader:
			item_type,item_id,item_descriptor,count,username,log_id,major_brand,medium_brand, \
                	minor_brand,sub_brand,subsub_brand = row
            
           	 # brands classification that is still "unknown"
			unknownList = Set(['INDETERMINATE','PRIVATE_LABEL', 'UNKNOWN'])
            
			if major_brand.upper() in unknownList:
				continue
			else: # put RSD in dictionary, key = brand, value = RSD
				if major_brand.upper() in trainedRSD:
					trainedRSD[major_brand.upper()].add(item_descriptor.upper())
				else:
					trainedRSD[major_brand.upper()] = Set([item_descriptor.upper()])
					
	# brands list dictionary
	brandsList = {}
	
# 	with open(BRANDS_LIST, 'rb') as brfile:
# 		csvreader = csv.reader(brfile, delimiter=',', quotechar = '"')
# 		
# 		for row in csvreader:
# 			brand, brand_descriptor = row
# 			
# 			if (re.match('[^_]', brand)):
# 				brand_tokens = brand.split("_")
# 				brandsList[' '.join(brand_tokens).upper()] = brand.upper()
# 				brandsList[''.join(brand_tokens).upper()] = brand.upper()
# 			else:
# 				brandsList[brand.upper()] = brand.upper()
	
	for brand in trainedRSD:
		if (re.match('[^_]', brand)):
			brand_tokens = brand.split("_")
			brandsList[' '.join(brand_tokens).upper()] = brand.upper()
			brandsList[''.join(brand_tokens).upper()] = brand.upper()
			brandsList['-'.join(brand_tokens).upper()] = brand.upper()
			

		else:
			brandsList[brand.upper()] = brand.upper()
                
	return trainedRSD, brandsList
                    

if __name__ == "__main__":
    read()
