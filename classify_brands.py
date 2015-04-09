from __future__ import division

import csv
import operator
import random
import re
from sets import Set
from ExceptionNotSeen import NotSeen

class classifyBrands(object):
	def __init__(self, trained_data):
		self.data = trained_data
		self.brandsList = trained_data.brandsList
		
		self.mostFreqWords = trained_data.mostFreqWords
		self.trainedRSD = trained_data.trainedRSD
		self.TotalRSDCount = trained_data.totalRSDCount
		
		self.predictedClass = {} # dict of most probable class for RSD
								 # predictedClass[RSD] = class
								 
		self.accuracy = [0,0] # [correct classification, incorrect classification]
		
		self.defaultProb = .00000001
		
# 		self.right = [0,0]
# 		self.wrong = [0,0]
		
	def identifyBrands(self, unknown_brands, numToTest):		
		# read unknown brands file
		with open(unknown_brands, 'rb') as csvfile:
			
			# get random lines from file
			# count number of rows in file
			row_count = sum(1 for row in csvfile)
			samples = Set(random.sample(xrange(row_count), numToTest))
			samp = 1
			csvfile.seek(0)
			
			csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
				
			next(csvreader, None)  # skip the headers
		
			for row in csvreader:
				if samp not in samples:
					samp += 1
					continue
				samp += 1
# 				numToTest -= 1
# 				if numToTest == 0:
# 					break
					
				# determines if word in RSD is most frequented in brands training data
# 				item_type,item_id,item_descriptor,count = row # for unknown brands file

				#####
				item_type,item_id,item_descriptor,count,username,log_id,major_brand,medium_brand, \
                	minor_brand,sub_brand,subsub_brand = row # for training data file
                #####
				
				#skip if item is just digit
				if item_descriptor.isdigit():
					continue
				
				rsd = re.sub(r'[^a-zA-Z ]',' ', item_descriptor.upper())				
# 				rsd = re.sub(r'[^a-zA-Z0-9 ]',' ', item_descriptor)
				if not re.search('[a-zA-Z]', rsd):
					continue
				
				tokens = rsd.split(' ')
												
				possibleBrands = []
				for i in range(len(tokens)):
					j = 0
					while j+i+1 < len(tokens)+1:
						withSpaces = ' '.join(tokens[j:j+i+1])
						withoutSpaces = ''.join(tokens[j:j+i+1])
												
						if withSpaces.upper() in self.brandsList.keys():
							possibleBrands.append(self.brandsList[withSpaces.upper()])
						if withoutSpaces.upper() in self.brandsList.keys():
							possibleBrands.append(self.brandsList[withoutSpaces.upper()])
						j += 1 #increments to next set of words in rsd
				
				possibleBrands = Set(possibleBrands)
				if len(possibleBrands) > 1:
					# check if each of the possible brands are in trainedRSD
					brct = 0
					for brand in possibleBrands:
						if brand in self.trainedRSD.keys():
							brct += 1
						else:
							possibleBrands.remove(brand)
					# if so, check if there is still more than 1 brands --> do naive Bayes
					if brct > 1:
						self.naiveBayes(item_descriptor.upper(), tokens, possibleBrands, count)
				
				if len(possibleBrands) == 1:
					found = possibleBrands.pop()
					self.predictedClass[item_descriptor.upper()] = found
					
					#####
					if item_descriptor.upper() in self.trainedRSD[found]: # for training data file
						self.accuracy[0] += int(count)
					else:
						self.accuracy[1] += int(count)
					#####
									
				if not possibleBrands:
					self.classify(item_descriptor.upper(), tokens, count)		
		
		#####
		acc = self.accuracy[0]/sum(self.accuracy)*100
# 		print "right=" + str(self.right[0]/self.right[1])
# 		print "wrong=" + str(self.wrong[0]/self.wrong[1])
		print "Accuracy: " + str(acc) + "%"
		#####
		
		return self.predictedClass
	
	def classify(self, item_descriptor, tokens, count):
		possibleBrands = []
	
		for word in tokens:
			if word.upper() in self.mostFreqWords.keys():
				possibleBrands = possibleBrands + self.mostFreqWords[word.upper()]

		possibleBrands = Set(possibleBrands)
		if len(possibleBrands) == 1:
			found = possibleBrands.pop()
			self.predictedClass[item_descriptor] = found
			
			#####
			if item_descriptor.upper() in self.trainedRSD[found]:
				self.accuracy[0] += int(count)
			else:
				self.accuracy[1] += int(count)
			#####
			
			return self.predictedClass
			
			
		elif not possibleBrands:
# 			return self.naiveBayes(item_descriptor, tokens, self.trainedRSD.keys(), count)
# 			self.predictedClass[item_descriptor] = "unknown"
			return self.predictedClass
		else:
			return self.naiveBayes(item_descriptor, tokens, possibleBrands, count)
	
	def naiveBayes(self, item_descriptor, tokens, possibleBrands, count):
		# probsOfClasses[class] = probability that RSD is in class
		probsOfClasses = {}
		
		for brand in possibleBrands:
			if brand not in self.trainedRSD.keys():
				continue
			# calculate probability of seeing each word/token in class/brand
			# P(word_j|class_i)
			tokenProbs = [self.getTokenProb(token, brand) for token in tokens \
						 if (len(token)>1)]
		
			#calculate probability of seeing entire RSD in brand
			try:
				itemProb = reduce(lambda a,b: a*b, (i for i in tokenProbs if i))
			except: 
				itemProb = 0
								
			# probability * prior prob
# 			probsOfClasses[brand] = itemProb
			probsOfClasses[brand] = itemProb * self.getPrior(brand, self.TotalRSDCount)

		if not probsOfClasses:
			return self.predictedClass
			
		# sort by highest probability
		# store class with highest probability in predictedClass
		highestProb = max(probsOfClasses.iteritems(), key=operator.itemgetter(1))
		
		# normalize probabilities
		for k in probsOfClasses.keys():
			probsOfClasses[k] = probsOfClasses[k]/highestProb
		
		# update class highest predicted probability
		highestProb = max(probsOfClasses.iteritems(), key=operator.itemgetter(1))
		
		# remove all potentially wrongly classified brands
		lowestProb = min(probsOfClasses.iteritems(), key=operator.itemgetter(1))
		if highestProb[1] - lowestProb[1] > 0.1:
			return self.predictedClass
		
		self.predictedClass[item_descriptor] = highestProb[0]
								
		#####
		if item_descriptor.upper() in self.trainedRSD[highestProb[0]]: # for training data file
# 			print "right: " + item_descriptor + ": " + str(highestProb[1]-lowestProb[1]) #DEBUG
# 			self.right[0] += highestProb[1]-lowestProb[1] #DEBUG
# 			self.right[1] += 1 #DEBUG
		
			self.accuracy[0] += int(count)
		else:
			lowestProb = min(probsOfClasses.iteritems(), key=operator.itemgetter(1)) #DEBUG
# 			print "wrong: " + item_descriptor + ": " + str(highestProb[1]-lowestProb[1]) #DEBUG
# 			self.wrong[0] += highestProb[1]-lowestProb[1] #DEBUG
# 			self.wrong[1] += 1 #DEBUG
			
			self.accuracy[1] += int(count)
		#####
		
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
		