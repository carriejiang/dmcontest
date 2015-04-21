from __future__ import division

import csv
import math
from operator import itemgetter
import random
import re
from sets import Set
from ExceptionNotSeen import NotSeen

class classifyBrands(object):
	def __init__(self, trained_data):
		self.data = trained_data		
		self.trainedRSD = trained_data.trainedRSD
		self.setTrainedRSD = trained_data.setTrainedRSD
		self.termToBrands = trained_data.termToBrands
		self.numTermsInBrands = trained_data.numTermsInBrands
		self.numKnownBrands = trained_data.numKnownBrands
		
		self.predictedClass = {} # dict of most probable class for RSD
								 # predictedClass[RSD] = class
								 
		self.accuracy = [0,0] # [correct classifibrandion, incorrect classifibrandion]
		
		self.defaultProb = .0000000001
		
		self.right = [0,0]
		self.wrong = [0,0]
		
	def classify(self, unknown_brand, numToTest):		
		# read unknown brand file
		with open(unknown_brand, 'rb') as csvfile:
			# get random lines from file
			# count number of rows in file
			row_count = sum(1 for row in csvfile)
			samples = Set(random.sample(xrange(row_count), numToTest))
			samp = 1
			csvfile.seek(0)
			
			numTested = 0
			
			csvreader = csv.reader(csvfile, delimiter=',', quotechar = '"')
				
			next(csvreader, None)  # skip the headers
		
			for row in csvreader:
				if samp not in samples:
					samp += 1
					continue
				samp += 1

					
# 				# determines if word in RSD is most frequented in brand training data
# 				item_type,item_id,item_descriptor,count = row # for unknown brand file

				#####
				item_type,item_id,item_descriptor,count,username,log_id,major_brand,medium_brand, \
                	minor_brand,sub_brand,subsub_brand = row # for training data file

				if major_brand.upper() in Set(['INDETERMINATE','PRIVATE_LABEL', 'UNKNOWN']):
					continue	
				###
				
				numTested+=int(count)
				
				#skip if item is just digit
				if item_descriptor.isdigit():
					continue
				
				rsd = re.sub(r'[^a-zA-Z0-9 ]',' ', item_descriptor.upper())
				if not re.search('[a-zA-Z]', rsd):
					continue
				
				tokens = rsd.split(' ')
				
				possibleBrands = []
				for term in tokens:
					try:
						possibleBrands += list(self.termToBrands[term])
					except:
						continue
									
				if len(possibleBrands) == 1:
					self.predictedClass[item_descriptor.upper()] = possibleBrands[0]
					
					#####
					if item_descriptor.upper() in self.setTrainedRSD[possibleBrands[0]]: # for training data file
						self.accuracy[0] += int(count)
					else:
						self.accuracy[1] += int(count)
					#####
					
					continue
					
				elif not possibleBrands:
					continue
				
				else:
					possibleBrands = Set(possibleBrands)	
					self.tfidf(item_descriptor.upper(), tokens, possibleBrands, count)
					
		
		#####
		acc = self.accuracy[0]/sum(self.accuracy)*100
		print "right=" + str(self.right[0]/self.right[1])
		print "wrong=" + str(self.wrong[0]/self.wrong[1])
		print "Recall: " + str(numTested/(self.numKnownBrands+numTested) * 100) + "%"
		print "Accuracy: " + str(acc) + "%"
		#####
		
		return self.predictedClass

	
	def tfidf(self, item_descriptor, tokens, possibleBrands, count):
		#(raw term frequency/total # terms in brand) *
		#log(total # brand/# brand that contain term)
		
		# probsOfClasses[class] = probability that RSD is in class
		probsOfClasses = []
		
		for brand in possibleBrands:
			#calculate tfidf for each word
			tokenProbs = [self.tf(token,brand)* self.idf(token) \
							for token in tokens if (len(token)>1)]		
	
			#calculate probability of seeing entire RSD in brand
			try:
				itemProb = reduce(lambda a,b: a+b, (i for i in tokenProbs if i))
			except: 
				itemProb = 0
							
			probsOfClasses.append((brand, itemProb))
						
		# sort by highest probability
		# store class with highest probability in predictedClass

		probsOfClasses = sorted(probsOfClasses,key=itemgetter(1))	
					
		highestProb = probsOfClasses[-1]
		
		# normalize probabilities
		for k in range(0,len(probsOfClasses)):
			try:
				probsOfClasses[k] = (probsOfClasses[k][0],probsOfClasses[k][1]/highestProb[1])
			except:
				return self.predictedClass
				
		
		# update class highest predicted probability
		highestProb = probsOfClasses[-1]
		
		if len(probsOfClasses) == 1:
			#####
			if item_descriptor.upper() in self.setTrainedRSD[highestProb[0].upper()]: # for training data file
				self.accuracy[0] += int(count)
			else:
				self.accuracy[1] += int(count)
			#####
				
			self.predictedClass[item_descriptor] = highestProb[0]
			return self.predictedClass
		
		# remove all potentially wrongly classified brand
		lowerProb = probsOfClasses[-2]
		if highestProb[1] - lowerProb[1] < 0.99:
			return self.predictedClass
		
		self.predictedClass[item_descriptor] = highestProb[0]
								
		#####
		if item_descriptor.upper() in self.setTrainedRSD[highestProb[0].upper()]: # for training data file
			self.right[0] += highestProb[1]-lowerProb[1] #DEBUG
			self.right[1] += 1 #DEBUG
		
			self.accuracy[0] += int(count)
		else:
			self.wrong[0] += highestProb[1]-lowerProb[1] #DEBUG
			self.wrong[1] += 1 #DEBUG
			
			self.accuracy[1] += int(count)
		#####
		
		return self.predictedClass
				
			
	def tf(self, word, brand):
		#P(word|brand)
		#word Freq / total number of terms in Brands
				
		# if token not seen in training set, 
		# return None so it isn't included in calculations
		try:
			tokenFreq = self.data.getFrequency(word, brand)
		except NotSeen as e:
			tokenFreq = None
			
		# class does not have this token
		if tokenFreq is None:
			return self.defaultProb
		
		try:
			return float(tokenFreq)/self.numTermsInBrands[brand]
		except:
			return self.defaultProb
		
	def idf(self, word):
		#log(num brand total/num brand containing term)
		try:
			return math.log(float(self.numKnownBrands)/len(self.termToBrands[word]),10)
		except:
			return self.defaultProb
		