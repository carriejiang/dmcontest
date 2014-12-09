import csv
from sets import Set

class naiveBayesClassifier(object):

	def __init__(self, trainedData):
		self.data = trainedData
		self.defaultProb = 0.000000001
	
	def classify(self, unknownClass_csv):
		
		# dict of most probable class for RSD
		# predictedClass[RSD] = class
		predictedClass = {}
		
		classes = self.data.classList
		
		# read csv of unknown RSD classifications for RSD
		RSD = []
		with open(unknownClass_csv, 'rb') as unknownClassFile:
			classReader = csv.reader(unknownClassFile, delimiter = ',', quotechar = '"')
			for row in classReader:
				RSD.append(row[2])
		
		# for each RSD
		for item in RSD:
			# prob of Classes dict
			# probsOfClasses[class] = probability that RSD is in class
			probsOfClasses = {}
			
			# unique words only
			words = list(set(item.upper().split(' ')))
			print words #DEBUG
			
			# for each class
			for className in classes:
				if className not in self.data.classList:
					continue
				# calculate the probability of seeing each word in the class
				# P(Token_1|Class_i)
				wordProbs = [self.getWordProb(word, className) for word in words]
				
				# calculate the probability of seeing the RSD item in class
				# P(Token_1|Class_i) * P(Token_2|Class_i) * ... * P(Token_n|Class_i)
				try:
					itemProb = reduce(lambda a,b: a*b, (i for i in wordProbs if i))
				except:
                			itemProb = 0
				
				# probability * priorProb
				probsOfClasses[className] = itemProb * self.getPrior(className)
				
				# sort by highest probability
				# store class with highest probability in predictedClass
				predictedClass[item] = sorted(probsOfClasses.items(), 
										key=operator.itemgetter(1), reverse=True)
										
		return predictedClass
				
	def getPrior(self, className):
		return self.data.getClassRSDCount(className)/self.data.getTotalRSDCount()
		
	def getWordProb(self, word, className):
		#p(token|Class_i)
       		classRSDCount = self.data.getClassRSDCount(className)
        
		# if class not seen in training set, 
		# return None so it isn't included in calculations
		try:
			wordFreq = self.data.getFrequencies(word, className)
		except NotSeen as e:
			return None
			
		# class does not have this word
		if wordFreq is None:
			return self.defaultProb
			
		probability = wordFreq/classRSDCount
		
		return probability
        	
			
