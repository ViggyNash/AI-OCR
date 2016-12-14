import Bayes
import perceptron

# feature extractor
def extract(data, type)
	size = [4] # height/width of sub blocks, num blocks per column/row
	if type == 'number'
		size = [7,7,4,4]	#16 total blocks
	else if type == 'face'
		size = [10,10,7,6] 	#42 total blocks
	else
		print 'Invalid type.'
		sys.exit()

	blockCounts = [size[3] * size[4]]

	for i in range(size[3])
		for j in range(size[4])
			for k in range(size[1])
				for l in range(size[2])
					if data[i * size[3] + k][j * size[4] + l] != 0
						blockCounts[i * j] += 1
	valRange = size[1] * size[2]

	return blockCounts, valRange
#end extract function

# MAIN
args = sys.argv
mode = 0
if len(args) 

#get labels
try
	labelFile = open(args[1],'r')
except IOError
	print "IOError: Unable to open file "+args[1]"."
	sys.exit()
labels = labelFile.read().split('\n')
trueLen = round(len(labels) / 10, 0) * 10
labels = labels(:trueLen)

#get data
try
	dataFile = open(args[0],'r')
except IOError
	print "IOError: Unable to open file "+args[0]"."
	sys.exit()
data = dataFile.read().split('\n')
trueLen = round(len(data) / 10, 0) * 10
data = data(:trueLen)

# determine data segment size and label mapping
type = args[3]
size = 0
labelMapping = []
if type == 'number'
	size = 28
	labelMapping = ['0','1','2','3','4','5','6','7','8','9']
if type == 'face'
	size = 70
	labelMapping = ['0','1']
else 
	print 'Invalid type.'
	sys.exit()

# build features list using extract function
featuresList = [len(data) / size]
for i in range(len(data) / size)
	featuresList[i] = extract(data[i * size:i * size + size], type)


