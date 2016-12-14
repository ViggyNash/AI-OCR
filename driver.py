import Bayes
import sys
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

	blockCounts = [size[2] * size[3]]

	for i in range(size[2]):
		for j in range(size[3]):
			for k in range(size[0]):
				for l in range(size[1]):
					if data[i * size[2] + k][j * size[3] + l] != 0:
						blockCounts[i * j] += 1
	valRange = size[0] * size[1]

	return blockCounts, valRange
#end extract function

# MAIN
args = sys.argv
mode = 0 # 0 = training, 1 = testing
if len(args) == 4:
	mode = 1
if len(args) == 5:
	mode = 0
else:
	print 'Invalid number of arguments' + str(len(args)) 
	sys.exit()

#get labels
try:
	labelFile = open(args[2],'r')
except IOError:
	print "IOError: Unable to open file "+args[2]+"."
	sys.exit()
labels = labelFile.read().split('\n')
trueLen = int(round(len(labels) / 10, 0) * 10)
labels = labels[:trueLen]

#get data
try:
	dataFile = open(args[1],'r')
except IOError:
	print "IOError: Unable to open file "+args[1]+"."
	sys.exit()
data = dataFile.read().split('\n')
trueLen = int(round(len(data) / 10, 0) * 10)
data = data[:trueLen]

# determine data segment size and label mapping
type = args[4].lower()
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
featuresList = [len(data) / size]
for i in range(len(data) / size):
	featuresList[i], valRange = extract(data[i * size:i * size + size], type)

assert len(featuresList)

model = args[3].lower()
if model == 'bayes':
	# Bayes
	bayesTraining(featuresList, labels, labelMapping, valRange)
elif model == 'percept':
	print 'NOT YET IMPLEMENTED'
	# Perceptron
elif model == 'other':
	# Other
	print 'NOT YET IMPLEMENTED'
else :
	print 'Invalid model specified.'
	sys.exit()