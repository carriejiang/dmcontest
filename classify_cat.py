from __future__ import division

import csv
import operator
import random
import re
from sets import Set
from ExceptionNotSeen import NotSeen

class classifyCat(object):
	def __init__(self, trained_data):
		self.data = trained_data
		self.catList = trained_data.catList
		
		self.mostFreqWords = trained_data.mostFreqWords
		self.trainedRSD = trained_data.trainedRSD
		self.TotalRSDCount = trained_data.totalRSDCount
		
		self.predictedClass = {} # dict of most probable class for RSD
								 # predictedClass[RSD] = class
								 
		self.accuracy = [0,0] # [correct classification, incorrect classification]
		
		self.defaultProb = 0.00000001
		
	def identifyCat(self, unknown_cat, numToTest):		
		# read unknown cat file
		with open(unknown_cat, 'rb') as csvfile:
			
			# get random lines from file
			# count number of rows in file
			row_count = sum(1 for row in csvfile) - 1
			samples = Set(random.sample(xrange(row_count), numToTest))
			samp = 1
			csvfile.seek(0)
			
			csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
				
			next(csvreader, None)
			next(csvreader, None)  # skip the headers
		
			for row in csvreader:
				if samp not in samples:
					samp += 1
					continue
				samp += 1
# 				numToTest -= 1
# 				if numToTest == 0:
# 					break
					
				# determines if word in RSD is most frequented in cat training data
# 				item_type,item_id,item_descriptor,count = row # for unknown cat file

				#####
				item_type,item_id,item_descriptor,count,username,log_id,sector,dept, \
					majorcat,cat,subcat = row # for training data file
                #####
				
				#skip if item is just digit
				if item_descriptor.isdigit():
					continue
				
				rsd = re.sub(r'[^a-zA-Z ]',' ', item_descriptor)				
# 				rsd = re.sub(r'[^a-zA-Z0-9 ]',' ', item_descriptor)
				if not re.search('[a-zA-Z]', rsd):
					continue
				
				fixed_rsd = rsd.split(' ')
								
				self.classify(item_descriptor.upper(), fixed_rsd)
												
# 				possibleCat = []
# 				for i in range(len(fixed_rsd)):
# 					j = 0
# 					while j+i+1 < len(fixed_rsd)+1:
# 						withSpaces = ' '.join(fixed_rsd[j:j+i+1])
# 						withoutSpaces = ''.join(fixed_rsd[j:j+i+1])
# 												
# 						if withSpaces.upper() in self.catList.keys():
# 							possibleCat.append(self.catList[withSpaces.upper()])
# 						if withoutSpaces.upper() in self.catList.keys():
# 							possibleCat.append(self.catList[withoutSpaces.upper()])
# 						j += 1 #increments to next set of words in rsd
# 				
# 				possibleCat = Set(possibleCat)
# 				if len(possibleCat) > 1:
# 					# check if each of the possible cat are in trainedRSD
# 					brct = 0
# 					for cat in possibleCat:
# 						if cat in self.trainedRSD.keys():
# 							brct += 1
# 						else:
# 							possibleCat.remove(cat)
# 					# if so, check if there is still more than 1 cat --> do naive Bayes
# 					if brct > 1:
# 						self.naiveBayes(item_descriptor.upper(), fixed_rsd, possibleCat)
# 				
# 				if len(possibleCat) == 1:
# 					found = possibleCat.pop()
# 					self.predictedClass[item_descriptor.upper()] = found
# 					
# 					#####
# 					if item_descriptor.upper() in self.trainedRSD[found]: # for training data file
# 						self.accuracy[0] += 1
# 					else:
# 						self.accuracy[1] += 1
# 					#####
# 									
# 				if not possibleCat:
# 					self.classify(item_descriptor.upper(), fixed_rsd)		
			
		#####
		acc = self.accuracy[0]/sum(self.accuracy)*100
		print "Accuracy: " + str(acc) + "%"
		#####
		
		return self.predictedClass
	
	def classify(self, item_descriptor, tokens):
		possibleCat = []
	
		for word in tokens:
			if word.upper() in self.mostFreqWords.keys():
				possibleCat = possibleCat + self.mostFreqWords[word.upper()]

		possibleCat = Set(possibleCat)
		if len(possibleCat) == 1:
			found = possibleCat.pop()
			self.predictedClass[item_descriptor] = found
			
			#####
			if item_descriptor in self.trainedRSD[found]:
				self.accuracy[0] += 1
			else:
				self.accuracy[1] += 1
			#####
			
			return self.predictedClass
			
			
		elif not possibleCat:
			return self.naiveBayes(item_descriptor, tokens, self.trainedRSD.keys())
# 			self.predictedClass[item_descriptor] = "unknown"
# 			return self.predictedClass
		else:
			return self.naiveBayes(item_descriptor, tokens, possibleCat)
	
	def naiveBayes(self, item_descriptor, tokens, possibleCat):
		# probsOfClasses[class] = probability that RSD is in class
		probsOfClasses = {}
		
		for cat in possibleCat:
			if cat not in self.trainedRSD.keys():
				continue
			# calculate probability of seeing each word/token in class/cat
			# P(word_j|class_i)
			tokenProbs = [self.getTokenProb(token, cat) for token in tokens \
						 if not token.isdigit()]
		
			#calculate probability of seeing entire RSD in cat
			try:
				itemProb = reduce(lambda a,b: a*b, (i for i in tokenProbs if i))
			except: 
				itemProb = 0
								
			# probability * prior prob
			probsOfClasses[cat] = itemProb
# 				probsOfClasses[cat] = itemProb * self.getPrior(cat, self.TotalRSDCount)

		if not probsOfClasses:
			return self.predictedClass
			
		# sort by highest probability
		# store class with highest probability in predictedClass
		highestProb = max(probsOfClasses.iteritems(), key=operator.itemgetter(1))[0]
		self.predictedClass[item_descriptor] = highestProb
										
		#####
		if item_descriptor in self.trainedRSD[highestProb]: # for training data file
			self.accuracy[0] += 1
		else:
			self.accuracy[1] += 1
		#####
		
		return self.predictedClass
				
	def getPrior(self, cat, totalRSDCount):
		return len(self.trainedRSD[cat])/self.TotalRSDCount
			
			
	def getTokenProb(self, word, cat):
		#P(word|cat)
		classRSDCount = len(self.trainedRSD[cat])
		
		# if token not seen in training set, 
		# return None so it isn't included in calculations
		try:
			tokenFreq = self.data.getFrequency(word, cat)
		except NotSeen as e:
			return None
			
		# class does not have this token
		if tokenFreq is None:
			return self.defaultProb
			
		return tokenFreq/classRSDCount
		