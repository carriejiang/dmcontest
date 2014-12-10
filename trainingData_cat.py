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
		trainedFile = {}
		count = {}
		with open(csv_trainedClass, 'rb') as trainedClassFile:
			trainedClassReader = csv.reader(trainedClassFile, delimiter = ',', quotechar = '"')
			next(trainedClassReader, None) #skip the headers
			
			for row in trainedClassReader:
				trainedFile[row[1].upper()] = row[8].upper()
				count[row[1].upper()] = int(row[3])

		def getTokensFromDoc(trainedFile, count):
			for rsd in trainedFile.iterkeys():
				classvalue = trainedFile[rsd]
				if classvalue in allClassList:
					
					# tokenize RSD
					RSDtokens = rsd.split(' ')

					if classvalue not in self.trainedClass_hash:
						# create new sub-dict for class
						self.trainedClass_hash[classvalue] = {}
						
						self.RSDCount[classvalue] = 1
					else:
						self.RSDCount[classvalue] += 1
						
					# add RSD tokens in dict
					for token in RSDtokens:
						classDict = self.trainedClass_hash[classvalue]
						if token in classDict:
							classDict[token] += 1 * count[rsd]
						else:
							classDict[token] = 1 + 1 * count[rsd]
						
			return self.trainedClass_hash
		return getTokensFromDoc(trainedFile, count)

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
