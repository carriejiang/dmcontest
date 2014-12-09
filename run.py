from naiveBayesClassifier import NaiveBayesClassifier
from trainer import Trainer

brandsList = 'data/brands.csv'
categoriesList = 'data/categories.csv'

knownBrands = 'data/trained_brands.csv'
knownCategories = 'data/trained_categories.csv'

unknownBrands = 'data/unknown_brands_test.csv'
unknownCategories = 'data/unknown_categories.csv'

# train data
trainedBrands = Trainer()
trainedBrands.train(brandsList, knownBrands)

# trainedCategories = Trainer()
# trainedCategories.train(categoriesList, knownCategories

# use classifier
brandsClassify = NaiveBayesClassifier(trainedBrands.data)
# categoriesClassify = NaiveBayesClassifier(trainedCategories.data)

 
# test unknown cases
brandsClassification = brandsClassify.classify(unknownBrands)
# categoriesClassification = categoriesClassify.classify(unknownCategories)
