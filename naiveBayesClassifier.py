from __future__ import division

import csv
from sets import Set
import operator
from ExceptionNotSeen import NotSeen

class NaiveBayesClassifier(object):

	def __init__(self, trainedData):
		self.data = trainedData
		self.defaultProb = 0.000000001
	
	def classify(self, unknownClass_csv, numToTest):
		
		# dict of most probable class for RSD
		# predictedClass[RSD] = class
		predictedClass = {}
		
		classes = self.data.getClassList()
		totalRSDCount = self.data.getTotalRSDCount()
		
		# read csv of unknown RSD classifications for RSD
		RSD = []
		with open(unknownClass_csv, 'rb') as unknownClassFile:
			classReader = csv.reader(unknownClassFile, delimiter = ',', quotechar = '"')
			for row in classReader:
				if numToTest < 1:
					break
				numToTest = numToTest - 1
				next(classReader, None) #skip the headers
				RSD.append(row[2])
		
		# for each RSD
		for item in RSD:
			# prob of Classes dict
			# probsOfClasses[class] = probability that RSD is in class
			probsOfClasses = {}
			
			# unique tokens only
			tokens = list(set(item.upper().split(' ')))
			
			# for each class
			for className in classes:
				# calculate the probability of seeing each token in the class
				# P(Token_1|Class_i)
				tokenProbs = [self.getTokenProb(token, className) for token in tokens]
												
				# calculate the probability of seeing the RSD item in class
				# P(Token_1|Class_i) * P(Token_2|Class_i) * ... * P(Token_n|Class_i)
				try:
					itemProb = reduce(lambda a,b: a*b, (i for i in tokenProbs if i))
				except:
                			itemProb = 0
				
				# probability * priorProb
				probsOfClasses[className] = itemProb * self.getPrior(className,totalRSDCount)
			
				
			# sort by highest probability
			# store class with highest probability in predictedClass
			predictedClass[item] = max(probsOfClasses.iteritems(), 
									key=operator.itemgetter(1))[0]
						
							
		return predictedClass
				
	def getPrior(self, className, getTotalRSDCount):
		return self.data.getClassRSDCount(className)/getTotalRSDCount
		
	def getTokenProb(self, token, className):
		#p(token|Class_i)
       		classRSDCount = self.data.getClassRSDCount(className)
        
		# if token not seen in training set, 
		# return None so it isn't included in calculations
		try:
			tokenFreq = self.data.getFrequencies(token, className)
		except NotSeen as e:
			return None
			
		# class does not have this token
		if tokenFreq is None:
			return self.defaultProb
			
		return tokenFreq/classRSDCount        	
			
