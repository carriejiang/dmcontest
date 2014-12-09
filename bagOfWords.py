import csv
from sets import Set

def bagOfWords(csv_brands, csv_trainedBrands):
	# make known brands into set
	with open(csv_brands, 'rb') as brandsFile:
		brandsReader = csv.reader(brandsFile, delimiter = ',', quotechar = '"')
		brandsList = Set([])
		for row in brandsReader:
			brandsList.add(row[0].upper())
	
	# trained brands
	# bag of words represented as dict of dicts
	# Major Dict: key = each brand is a doc/dict, value = sub-dicts
	# Sub Dicts: key = word in RSD, value = number of occurences in RSD 
	def getWordsFromDoc(csv_trainedBrands):
		with open(csv_trainedBrands, 'rb') as trainedBrandsFile:
			trainedBrandsReader = csv.reader(trainedBrandsFile, delimiter = ',', quotechar = '"')
	
			trainedBrands_hash = {} #dict of dicts
			for row in trainedBrandsReader:
				if row[6].upper() in brandsList:

					# tokenize RSD
					RSDwords = row[1].split()

					if row[6].upper() not in trainedBrands_hash:
						# create new sub-dict for brand
						trainedBrands_hash[row[6].upper()] = {}
					
					# add RSD words in dict
					for word in RSDwords:
						brandDict = trainedBrands_hash[row[6].upper()]
						if word.upper() in brandDict:
							brandDict[word.upper()] += 1 * int(row[3])
						else:
							brandDict[word.upper()] = 1 + 1 * int(row[3])
					
			return trainedBrands_hash
	return getWordsFromDoc(csv_trainedBrands)
