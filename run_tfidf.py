"""
Run this script to implement TFIDF.

Output is written in CSV files named 
brandsClassified.csv and categoriesClassified.csv
for classified unknown brands and categories respectively.


"""

# from classify_brands_tfidf import classifyBrands
# from train_brands_tfidf import trainBrands
# from read_brands_tfidf import readBrands
from read_cat_tfidf import readCat
from classify_cat_tfidf import classifyCat
from train_cat_tfidf import trainCat
import csv
import time

start = time.time()

NUMTOTEST = 20000
# 
# #Brands
# # BRANDS_LIST = 'data/brands.csv'
# TRAINED_BRANDS = './data/trained_brands.csv'
# unknown_brands = './data/trained_brands.csv' #training data as test set
# # unknown_brands = './data/unknown_brands.csv'
# 
# #read data
# print "Reading training file..."
# parseData = readBrands(TRAINED_BRANDS)
# 
# #train data
# print "Training..."
# trainedBrands = trainBrands(parseData)
# trainedBrands.trainFreq(n)

# 
# #use classifier
# print "Classifying..."
# brandsClassify = classifyBrands(trainedBrands)
# #print len(brandsClassify.data.trainedClass_hash.keys())
# # test unknown cases
# brandsClassification = brandsClassify.identifyBrands(unknown_brands, NUMTOTEST)
	
	# write to file
# print "Writing File..."
# with open('classifiedBrands-' + time.strftime("%Y%m%d-%H%M") + '.csv', 'wb') as bc:
# 	csv_writer = csv.writer(bc, delimiter=',')
# 	csv_writer.writerow(['item_id','major_brand'])
# 	for item in brandsClassification.keys():
# 		csv_writer.writerow([item, brandsClassification[item]])


#Categories
# CAT_LIST = 'data/categories.csv'
TRAINED_CAT = './data/trained_categories.csv'
# unknown_cat = 'data/unknown_categories.csv'
unknown_cat = 'data/trained_categories.csv'


#read data
print "Reading training file..."
parseData = readCat(TRAINED_CAT)

# train data
print "Training..."
trainedCategories = trainCat(parseData)
trainedCategories.trainFreq()

# use classifier
print "Classifying..."

categoriesClassify = classifyCat(trainedCategories)
# test unknown cases
categoriesClassification = categoriesClassify.classify(unknown_cat, NUMTOTEST)

# 
# # write to file
# # categories
# with open('classifiedCat-tfidf-' + time.strftime("%Y%m%d-%H%M") + '.csv', 'wb') as cc:
# 	csv_writer = csv.writer(cc, delimiter=',')
# 	csv_writer.writerow(['item_id','majorcat'])
# 	for k in categoriesClassification.keys():
# 		csv_writer.writerow([k, categoriesClassification[k]])

end = time.time()
elapsed = end - start
print "Time: " + str(elapsed) + " seconds"