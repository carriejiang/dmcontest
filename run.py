"""
Run this script to implement the Naive Bayes Classifier.

Output is written in CSV files named 
brandsClassified.csv and categoriesClassified.csv
for classified unknown brands and categories respectively.

Change numToTest to the number of unknown brands/categories 
you want the classifier to run on.

"""

from naiveBayesClassifier import NaiveBayesClassifier
from trainer_brands import BrandsTrainer
from trainer_cat import CatTrainer
import csv

# number of items to test in testing set
numToTest = 1000

brandsList = 'data/brands.csv'
categoriesList = 'data/categories.csv'

knownBrands = 'data/trained_brands.csv'
knownCategories = 'data/trained_categories.csv'

unknownBrands = 'data/unknown_brands.csv'
unknownCategories = 'data/unknown_categories.csv'

# train data
trainedBrands = BrandsTrainer()
trainedBrands.train(brandsList, knownBrands)

trainedCategories = CatTrainer()
trainedCategories.train(categoriesList, knownCategories)

# use classifier
brandsClassify = NaiveBayesClassifier(trainedBrands.data)
categoriesClassify = NaiveBayesClassifier(trainedCategories.data)

 
# test unknown cases
brandsClassification = brandsClassify.classify(unknownBrands, numToTest)
categoriesClassification = categoriesClassify.classify(unknownCategories, numToTest)

# write to file
# brands
with open('brandsClassified.csv', 'wb') as bc:
	csv_writer = csv.writer(bc, delimiter=',')
	csv_writer.writerow(['item_id','major_brand'])
	for item in brandsClassification.keys():
		csv_writer.writerow([item, brandsClassification[item]])

# categories
with open('categoriesClassified.csv', 'wb') as cc:
	csv_writer = csv.writer(cc, delimiter=',')
	csv_writer.writerow(['item_id','majorcat'])
	for item in categoriesClassification.keys():
		csv_writer.writerow([item, categoriesClassification[item]])
