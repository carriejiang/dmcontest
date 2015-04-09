from __future__ import division

import csv
import operator
import re
from sets import Set
from ExceptionNotSeen import NotSeen

class modifiedNaiveBayes(object):
	def __init__(self, trained_data):
		self.data = trained_data
		
		self.mostFreqWords = trained_data.mostFreqWords
		self.frequency = trained_data.frequency
		self.trainedRSD = trained_data.trainedRSD
		self.TotalRSDCount = trained_data.totalRSDCount
		
		self.classified = {} # dict of all possible classes for RSD
		self.predictedClass = {} # dict of most probable class for RSD
								 # predictedClass[RSD] = class
		
		self.defaultProb = 0.000000001
		
	def identifyBrands(self, unknown_brands, numToTest):

		#find scores
		#if there is a match between a word in RSD and brand dictionary
			# then return that brand as predicted class
		# else
			# run classify	
		
		return self.predictedClass
	
	def classify(self, unknown_brands, numToTest):
	
		# read unknown brands file
		with open(unknown_brands, 'rb') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
		
			next(csvreader, None)  # skip the headers
		
			for row in csvreader:
				numToTest -= 1
				if numToTest == 0:
					break

				# determines if word in RSD is most frequented in brands training data
				item_type,item_id,item_descriptor,count = row
				rsd = re.sub(r'[^a-zA-Z0-9 ]','', item_descriptor)
				fixed_rsd = item_descriptor.split(' ')
# 				print rsd #DEBUG
				for word in fixed_rsd:
# 					print word #DEBUG			
					if word.upper() in self.mostFreqWords.keys():
						if item_descriptor in self.classified.keys():
							self.classified[item_descriptor] = \
								list(Set(self.classified[item_descriptor] + \
								self.mostFreqWords[word.upper()]))
						else:
							self.classified[item_descriptor] = self.mostFreqWords[word.upper()]
# 						print self.classified #DEBUG

		#return self.classified
		return self.naiveBayes(self.classified, self.frequency)
	
	def naiveBayes(self, classified, frequency):
		
# 		print classified #DEBUG
		
		for item in classified.keys():
			# probsOfClasses[class] = probability that RSD is in class
			probsOfClasses = {}
			
			fixed_item = re.sub(r'[^a-zA-Z0-9 ]','', item)
			tokens = list(fixed_item.split(' '))
			for brand in classified[item]:
				# calculate probability of seeing each word/token in class/brand
				# P(word_j|class_i)
				tokenProbs = [self.getTokenProb(token, brand) for token in tokens \
				             if not token.isdigit()]
				             
				# print item + ": " + brand #DEBUG
# 				print tokenProbs #DEBUG
			
				#calculate probability of seeing entire RSD in brand
				try:
					itemProb = reduce(lambda a,b: a*b, (i for i in tokenProbs if i))
				except: 
					itemProb = 0
					
# 				print itemProb #DEBUG
				
				# probability * prior prob
				probsOfClasses[brand] = itemProb
# 				probsOfClasses[brand] = itemProb * self.getPrior(brand, self.TotalRSDCount)
				
			# sort by highest probability
			# store class with highest probability in predictedClass
			self.predictedClass[item] = max(probsOfClasses.iteritems(), 
									key=operator.itemgetter(1))[0]
		
		return self.predictedClass
				
	def getPrior(self, brand, totalRSDCount):
		return len(self.trainedRSD[brand])/self.TotalRSDCount
			
			
	def getTokenProb(self, word, brand):
		#P(word|brand)
		classRSDCount = len(self.trainedRSD[brand])
		
		# if token not seen in training set, 
		# return None so it isn't included in calculations
		try:
			tokenFreq = self.data.getFrequency(word, brand)
		except NotSeen as e:
			return None
			
		# class does not have this token
		if tokenFreq is None:
			return self.defaultProb
			
		return tokenFreq/classRSDCount
		