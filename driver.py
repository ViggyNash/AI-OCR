import Bayes
import sys
import numpy
import re
#import perceptron

# feature extractor
def extract(data, type):
	size = [4] # height/width of sub blocks, num blocks per column/row
	if type == 'number':
		size = [7,7,4,4]	#16 total blocks
	elif type == 'face':
		size = [10,10,7,6] 	#42 total blocks
	else:
		print 'Invalid type.'
		sys.exit()

	blockCounts = [0 for x in range(size[2] * size[3])]
	#print size
	#print len(blockCounts)
	#print str(len(data)) + " " + str(len(data[0]))
	for i in range(size[2]):
		for j in range(size[3]):
			for k in range(size[0]):
				for l in range(size[1]):
					if data[i * size[2] + k][j * size[3] + l] != ' ':
						blockCounts[i * size[2] + j] += 1
	valRange = size[0] * size[1]
	return blockCounts, valRange
	'''
	size = [2] # height/width of sub blocks, num blocks per column/row
	if type == 'number':
		size = [28,28]	#16 total blocks
	elif type == 'face':
		size = [70,60] 	#42 total blocks
	else:
		print 'Invalid type.'
		sys.exit()

	blockCounts = [0 for x in range(size[0] * size[1])]
	for i in range(size[0]):
		for j in range(size[1]):
			if data[i][j] != ' ':
				blockCounts[i * size[0] + j] += 1
	valRange = 2
	return blockCounts, valRange
	'''
#end extract function

def main():
	args = sys.argv
	mode = 0 # 0 = training, 1 = testing
	if len(args) == 4:
		mode = 1
	elif len(args) == 5:
		mode = 0
	else:
		print 'Invalid number of arguments ' + str(len(args)) 
		sys.exit()

	#get labels
	if mode == 0:
		try:
			labelFile = open(args[2],'r')
		except IOError:
			print "IOError: Unable to open labels file "+args[2]+"."
			sys.exit()
		labels = re.split('[\n\r]',labelFile.read())	#labelFile.read().split({'\n','\n\r'})
		trueLen = int(round(len(labels) / 10, 0) * 10)
		labels = labels[0:trueLen:2]

	#get data
	try:
		dataFile = open(args[1],'r')
	except IOError:
		print "IOError: Unable to open data file "+args[1]+"."
		sys.exit()
	data = re.split('[\n\r]',dataFile.read())
	trueLen = int(round(len(data) / 10, 0) * 10)
	data = data[0:trueLen:2]
	data = [list(data[x]) for x in range(len(data))]

	# determine data segment size and label mapping
	type = args[4 - mode].lower()
	size = 0
	labelMapping = []
	if type == 'number':
		size = 28
		labelMapping = ['0','1','2','3','4','5','6','7','8','9']
	elif type == 'face':
		size = 70
		labelMapping = ['0','1']
	else:
		print 'Invalid type.' + type
		sys.exit()

	# build features list using extract function
	valRange = 0
	featuresList = [[] for x in range(len(data) / size)]
	for i in range(len(data) / size):
		featuresList[i], valRange = extract(data[i * size:i * size + size], type)

	# apply classifier/ test input
	model = args[3 - mode].lower()
	if model == 'bayes':
		# Bayes
		if mode == 0:
			bayes = Bayes.BayesModel()
			bayes.bayesTraining(featuresList, labels, labelMapping, valRange)
		else:
			bayes = Bayes.BayesModel()
			bayes.getModelData()
			labels = ''
			for i in range(len(featuresList)):
				label, prob = bayes.bayesTest(featuresList[i], labelMapping)
				labels += str(label) + "\n"
			print labels

	elif model == 'percept':
		print 'NOT YET IMPLEMENTED'
		# Perceptron
	elif model == 'other':
		# Other
		print 'NOT YET IMPLEMENTED'
	else :
		print 'Invalid model specified.'
		sys.exit()

main()