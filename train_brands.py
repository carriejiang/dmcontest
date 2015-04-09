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
		self.totalRSDCount = 0
		
	def trainFreq(self, n):				
		#n = 0.05 # change to reflect amount of most frequent words in brand you want to test on
		
		for brand, val in self.trainedRSD.items():
			self.totalRSDCount += 1
		
			cnt = Counter()
			
			for rsd in val:
				fixed_rsd = re.sub(r'[^a-zA-Z0-9 ]','', rsd)
				RSDtokens = fixed_rsd.split(' ') # split RSD into words
				
				for i in RSDtokens:
					# if word/token is integer, continue
					if i.isdigit() or len(i)<2:
						continue
					
					cnt[i] += 1 #increment count of word/token for brand
			
			# count of all words
			self.frequency[brand] = dict(cnt)
					
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

	
			
		
