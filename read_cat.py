import csv
import re
from sets import Set

def readCat(TRAINED_CAT, CAT_LIST):
	"""
	Load the trained brands and iterate through
	"""
	
	# dictionary of brands -> RSD
	trainedRSD = {}

	with open(TRAINED_CAT, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
		next(csvreader, None)  # skip the headers
        
		for row in csvreader:
			item_type,item_id,item_descriptor,count,username,log_id,sector,dept, \
					majorCat,cat,subcat = row
            
# 			#brands classification that is still "unknown"
# 			unknownList = Set(['INDETERMINATE','PRIVATE_LABEL', 'UNKNOWN'])
#             
# 			if major_brand.upper() in unknownList:
# 				continue
			if not majorCat:
				continue
			else:
				# put RSD in dictionary, key = cat, value = RSD
				if majorCat.upper() in trainedRSD:
					trainedRSD[majorCat.upper()].add(item_descriptor.upper())
				else:
					trainedRSD[majorCat.upper()] = Set([item_descriptor.upper()])
					
	# cat list dictionary
	catList = {}
	
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
	
	for cat in trainedRSD:
		if (re.match('[^_]', cat)):
			cat_tokens = cat.split("_")
			catList[' '.join(cat_tokens).upper()] = cat.upper()
			catList[''.join(cat_tokens).upper()] = cat.upper()
		else:
			catList[cat.upper()] = cat.upper()
                
	return trainedRSD, catList
                    

if __name__ == "__main__":
    read()
