from collections import Counter
import math
import re
from sets import Set
from ExceptionNotSeen import NotSeen

import read_cat_tfidf

class trainCat(object):
	def __init__(self, parsed_data):
		(self.trainedRSD, self.setTrainedRSD, self.numKnownCat) = parsed_data
		self.frequency = {}
		self.termToCat = {}
		self.numTermsInCat = {}
		self.totalRSDCount = 0
		
	def trainFreq(self):						
		for cat, val in self.trainedRSD.items():
			cnt = Counter()
						
			for (rsd,count) in val:
				fixed_rsd = re.sub(r'[^a-zA-Z0-9 ]','', rsd)
				RSDtokens = fixed_rsd.split(' ') # split RSD into words
				
				for i in RSDtokens:
					# if word/token is integer, continue
					if i.isdigit() or len(i)<2:
						continue
					
					cnt[i] += count #increment count of word/token for cat
			
			# count of all words
			self.numTermsInCat[cat] = sum(cnt.values())
			self.frequency[cat] = dict(cnt)	
									
			for e in cnt:
				if e in self.termToCat:
					self.termToCat[e].add(cat)
				else:
					self.termToCat[e] = Set([cat])
							
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

	
			
		
