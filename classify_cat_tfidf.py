from __future__ import division

import csv
import math
from operator import itemgetter
import random
import re
from sets import Set
from ExceptionNotSeen import NotSeen

class classifyCat(object):
	def __init__(self, trained_data):
		self.data = trained_data		
		self.trainedRSD = trained_data.trainedRSD
		self.setTrainedRSD = trained_data.setTrainedRSD
		self.termToCat = trained_data.termToCat
		self.numTermsInCat = trained_data.numTermsInCat
		self.numKnownCat = trained_data.numKnownCat
		
		self.predictedClass = {} # dict of most probable class for RSD
								 # predictedClass[RSD] = class
								 
		self.accuracy = [0,0] # [correct classification, incorrect classification]
		
		self.defaultProb = .00000001
		
		self.right = [0,0]
		self.wrong = [0,0]
		
	def classify(self, unknown_cat, numToTest):		
		# read unknown cat file
		with open(unknown_cat, 'rb') as csvfile:
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

					
# 				# determines if word in RSD is most frequented in cat training data
# 				item_type,item_id,item_descriptor,count = row # for unknown cat file

				#####
				item_type,item_id,item_descriptor,count,username,log_id,major_cat,medium_cat, \
                	minor_cat,sub_cat,subsub_cat = row # for training data file

				if major_cat.upper() in Set(['ISC_UNKNOWN','ISC_NON_ITEM']):
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
				
				possibleCat = []
				for term in tokens:
					try:
						possibleCat += list(self.termToCat[term])
					except:
						continue
									
				if len(possibleCat) == 1:
					self.predictedClass[item_descriptor.upper()] = possibleCat[0]
					
					#####
					if item_descriptor.upper() in self.setTrainedRSD[possibleCat[0]]: # for training data file
						self.accuracy[0] += int(count)
					else:
						self.accuracy[1] += int(count)
					#####
					
					continue
					
				elif not possibleCat:
					continue
				
				else:
					possibleCat = Set(possibleCat)	
					self.tfidf(item_descriptor.upper(), tokens, possibleCat, count)
					
		
		#####
		acc = self.accuracy[0]/sum(self.accuracy)*100
		print "right=" + str(self.right[0]/self.right[1])
		print "wrong=" + str(self.wrong[0]/self.wrong[1])
		print "Recall: " + str(numTested/(self.numKnownCat+numTested) * 100) + "%"
		print "Accuracy: " + str(acc) + "%"
		#####
		
		return self.predictedClass

	
	def tfidf(self, item_descriptor, tokens, possibleCat, count):
		#(raw term frequency/total # terms in cat) *
		#log(total # cat/# cat that contain term)
		
		# probsOfClasses[class] = probability that RSD is in class
		probsOfClasses = []
		
		for cat in possibleCat:
			#calculate tfidf for each word
			tokenProbs = [self.tf(token,cat)* self.idf(token) \
							for token in tokens if (len(token)>1)]		
	
			#calculate probability of seeing entire RSD in cat
			try:
				itemProb = reduce(lambda a,b: a*b, (i for i in tokenProbs if i))
			except: 
				itemProb = 0
							
			probsOfClasses.append((cat, itemProb))
						
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
			if item_descriptor.upper() in self.setTrainedRSD[highestProb[0].upper()]: # for training data file
				self.accuracy[0] += int(count)
			else:
				self.accuracy[1] += int(count)
				
			self.predictedClass[item_descriptor] = highestProb[0]
			return self.predictedClass
		
		# remove all potentially wrongly classified cat
		lowerProb = probsOfClasses[-2]
		if highestProb[1] - lowerProb[1] < 0.98:
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
				
			
	def tf(self, word, cat):
		#P(word|cat)
		#word Freq / total number of terms in Cat
				
		# if token not seen in training set, 
		# return None so it isn't included in calculations
		try:
			tokenFreq = self.data.getFrequency(word, cat)
		except NotSeen as e:
			tokenFreq = None
			
		# class does not have this token
		if tokenFreq is None:
			return self.defaultProb
		
		try:
			return float(tokenFreq)/self.numTermsInCat[cat]
		except:
			return self.defaultProb
		
	def idf(self, word):
		#log(num cat total/num cat containing term)
		try:
			return math.log(float(self.numKnownCat)/len(self.termToCat[word]))
		except:
			return self.defaultProb
		