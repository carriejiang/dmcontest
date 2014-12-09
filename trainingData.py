import csv
from sets import Set

from ExceptionNotSeen import NotSeen

class TrainingData(object):
	def __init__(self):
		self.trainedClass_hash = {}
		self.RSDCount = {} #keeps count of RSD per class

	def train(self, csv_classList, csv_trainedClass):
	
		# make known class into set
		with open(csv_classList, 'rb') as classFile:
			classReader = csv.reader(classFile, delimiter = ',', quotechar = '"')
			allClassList = Set([])
			
			for row in classReader:
				allClassList.add(row[0].upper())
		
		# trained classes
		# bag of tokens represented as dict of dicts
		# Major Dict: key = each class(brand/category) is a dict, value = sub-dicts
		# Sub Dicts: key = token in RSD, value = number of occurences in RSD 
		def getTokensFromDoc(csv_trainedClass):
			with open(csv_trainedClass, 'rb') as trainedClassFile:
				trainedClassReader = csv.reader(trainedClassFile, delimiter = ',', quotechar = '"')
				
				firstLine = True
				#trainedClass_hash = {} #dict of dicts
				for row in trainedClassReader:
					if firstLine: # skips first line of CSV file
						firstLine = False
						continue
						
					if row[6].upper() in allClassList:
						
						# tokenize RSD
						RSDtokens = row[1].split()

						if row[6].upper() not in self.trainedClass_hash:
							# create new sub-dict for class
							self.trainedClass_hash[row[6].upper()] = {}
							
							self.RSDCount[row[6].upper()] = 1
						else:
							self.RSDCount[row[6].upper()] += 1
						
						# add RSD tokens in dict
						for token in RSDtokens:
							classDict = self.trainedClass_hash[row[6].upper()]
							if token.upper() in classDict:
								classDict[token.upper()] += 1 * int(row[3])
							else:
								classDict[token.upper()] = 1 + 1 * int(row[3])
						
				return self.trainedClass_hash
		return getTokensFromDoc(csv_trainedClass)

	def getClassList(self):
		return list(self.trainedClass_hash.keys())

	def getTotalRSDCount(self):
		# returns total number of RSDs
		return sum(self.RSDCount.values())

	
	def getClassRSDCount(self, className):
		# returns count of RSDs for class
		return self.RSDCount[className]

	def getFrequencies(self, token, className):
		# returns frequencies for each token in class
		try:
			c = self.trainedClass_hash[className]
		except:
			raise NotSeen(className)

		try:
			return c[token]
		except:
			return None	
