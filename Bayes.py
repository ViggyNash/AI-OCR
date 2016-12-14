
modelData = []	#class x feature x value
classCounts = []

def getModelData(file = 'bData.txt')
	try:
		fileObj = open(file, 'r')
		break;
	except IOError
		print "IOError: File "+file+" not found, unable to read model data."
		sys.exit()

	data = fileObj.read()
	list = data.splitlines()
	classCount = len(list) - 1
	featCount = int(list[0].strip())
	valCount = len(list[1]) / featCount

	modelData = [classCount][featCOunt][valCount]
	classCounts = zeroes(classCount)

	for i in range(1, classCount)
		line = list[i].split(' ')
		for j in range(featCount)
			for k in range(valCount)
				modelData[i][j][k] = int(line[j * valCount + k])
				classCount[i] += modelData[i][j][k]
	fileObj.close()


def bayesTraining(FeaturesList, LabelsList, labelMapping, valRange)

	output = ''
	modelData = [len(labelMapping)][len(FeaturesList[0])][valRange]
	classCounts = [len(labelMapping)]
	
	for i in range(len(LabelsList)) 								#For each label
		classIdx = labelMapping.index(LabelsList[i]) 				#Get the class index of the given label
		classCounts[classIdx] += 1
		for j in range(len(FeaturesList))							#For each item in the list
			for k in range(len(FeaturesList[j]))					#For each feature the item has
				modelData[classIdx][j][Features[j][k]] += 1			#Increment the counter of the corresponding value
				output += str(modelData[classIdx][j][Features[j][k]]) +  ' '
		output += '\n'

	try
		file = open('bData.txt','w')
		file.write(output)
		break;
	except IOError
		print "IOError: Unable to write model data to bData.txt, terminating training."
	file.close()

def bayesTest(inputFeatures, labelMapping)
	
	conditionalProbs = [1 for x in range(len(modelData))] # Counts for input feature value given class
	for i in len(modelData)
		for j in len(modelData[i])
			conditionalProbs[i][j] *= modelData[i][j][inputFeatures[j]]	#Multiply the counts of the number of times the matching value
																		#value for a given feature of a given class was seen
	conditionalProbs = 	[conditionalProbs[x]/classCounts[x] for x in range(len(conditionalProbs))]

	totalI = sum(classCounts)
	probI = [len(classCounts)]
	for i in range(len(classCounts))
		probI[i] = conditionalProbs[i] * classCounts[i] / totalI

	return max(probI), labelMapping[find(max(probI))]
