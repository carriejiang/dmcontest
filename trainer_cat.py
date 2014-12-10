from trainingData_cat import TrainingData

class CatTrainer(object):
	def __init__(self):
 		#super(Trainer, self).__init__()
		self.data = TrainingData()
		
	def train (self, csv_classList, csv_trainedClass):
		self.data.train(csv_classList, csv_trainedClass)
