from collections import Counter
import math
import re
from sets import Set

import read_brands

class trainBrands():
	def __init__(self, trained_brands, brands_list):
		self.trainedRSD, self.brandsList = read_brands.readBrands(trained_brands, brands_list)
		self.mostFreqWords = {}
		self.frequency = {}
		self.uniqueFrequency = {}
		self.totalRSDCount = 0
		
	def trainFreq(self, n):				
		#n = 0.05 # change to reflect amount of most frequent words in brand you want to test on
		
		for brand, val in self.trainedRSD.items():
			self.totalRSDCount += 1
		
			cnt = Counter()
			uniqueCnt = Counter() #keeps track of word occurrence in each RSD
			
			for rsd in val:
				fixed_rsd = re.sub(r'[^a-zA-Z0-9 ]','', rsd)
				RSDtokens = fixed_rsd.split(' ') # split RSD into words
				uniqueTokens = Set()
				
				for i in RSDtokens:
					
					# if word/token is integer, continue
					if i.isdigit() or len(i)<2:
						continue
					
					cnt[i] += 1 #increment count of word/token for brand
					
					if i not in uniqueTokens:
						uniqueCnt[i] += 1 
			
			# count of all words
			self.frequency[brand] = dict(cnt)
			self.uniqueFrequency[brand] = dict(uniqueCnt)
					
			mostFreq = cnt.most_common(int(math.ceil(len(cnt)*n))) # take top n% most frequent words
			
			for (e, c) in mostFreq:
				if e == '':
					break
				
				if e in self.mostFreqWords.keys():
					self.mostFreqWords[e].append(brand)
				else:
					self.mostFreqWords[e] = [brand]
			
				
	def getFrequency(self, token, className):
		# returns frequencies for each token in class
		try:
			c = self.frequency[className]
		except:
			raise NotSeen(className)

		try:
			return c[token]
		except:
			return None	
			
	def getUniqueFrequency(self, token, className):
		# returns frequencies for each token in class
		try:
			c = self.uniqueFrequency[className]
		except:
			raise NotSeen(className)

		try:
			return c[token]
		except:
			return None	

	
			
		
