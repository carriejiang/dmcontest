"""
Run this script to implement the Naive Bayes Classifier.

Output is written in CSV files named 
brandsClassified.csv and categoriesClassified.csv
for classified unknown brands and categories respectively.


"""

from classify_brands import classifyBrands
from train_brands import trainBrands
from classify_cat import classifyCat
from train_cat import trainCat
import csv
import time

start = time.time()

NUMTOTEST = 10000
n = 0.035 #top % most frequent words for each brand in training set

BRANDS_LIST = 'data/brands.csv'
# CAT_LIST = 'data/categories.csv'

TRAINED_BRANDS = './data/trained_brands.csv'
# TRAINED_CAT = 'data/trained_categories.csv'

# unknown_brands = 'data/unknown_brands.csv'
# unknown_brands = 'data/unknown_brands_test.csv'
unknown_brands = './data/trained_brands.csv'
# unknown_cat = 'data/unknown_categories.csv'
# unknown_cat = 'data/trained_categories.csv'

# train data
# for n in range(25,45, 5):
# 	print "n=" + str(float(n)/1000)
print "Training..."
trainedBrands = trainBrands(TRAINED_BRANDS, BRANDS_LIST)
trainedBrands.trainFreq(n)

# trainedCategories = trainCat(TRAINED_CAT, CAT_LIST)
# trainedCategories.trainFreq()


# use classifier
print "Classifying..."
brandsClassify = classifyBrands(trainedBrands)
# categoriesClassify = classifyCat(trainedCategories)
# print len(brandsClassify.data.trainedClass_hash.keys())


# test unknown cases
brandsClassification = brandsClassify.identifyBrands(unknown_brands, NUMTOTEST)
# categoriesClassification = categoriesClassify.identifyCat(unknown_cat, NUMTOTEST)

# write to file
# brands
# with open('classifiedBrands.csv', 'wb') as bc:
# 	csv_writer = csv.writer(bc, delimiter=',')
# 	csv_writer.writerow(['item_id','major_brand'])
# 	for item in brandsClassification.keys():
# 		csv_writer.writerow([item, brandsClassification[item]])

# categories
# with open('classifiedCategories.csv', 'wb') as cc:
# 	csv_writer = csv.writer(cc, delimiter=',')
# 	csv_writer.writerow(['item_id','majorcat'])
# 	for item in categoriesClassification.keys():
# 		csv_writer.writerow([item, categoriesClassification[item]])

end = time.time()
elapsed = end - start
print "Time: " + str(elapsed) + " seconds"