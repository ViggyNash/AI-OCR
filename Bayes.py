
modelData = 0


def getModelData(file = 'bData.txt')
	file = open(file, 'r')
	data = file.read()
	list = data.splitlines()
	classCount = len(list) - 1
	featCount = int(list[0].strip())
	valCount = len(list[1]) / featCount

	for i in range(1, classCount)
		line = list[i].split(' ')
		for j = range(featCount)
			for k = range(valCount)
				modelData[i][j][k] = line[j * valCount + k]


def bayesTraining(FeaturesList, LabelsList, labelMapping)

	output = ''
	
	for i = range(LabelsList)
		classIdx = labelMapping.index(LabelsList[i])
		for j = range(FeaturesList)
			for k = range(len(FeaturesList[j])
				modelData[classIdx][j][Features[j][k]] += 1
				output += str(modelData[classIdx][j][Features[j][k]]) +  ' '
		output += '\n'

	file = open('bData.txt','w')
	file.write(output)


def bayesTest(inputFeatures)
	
	cProbs = [len(modelData)]

	for i = len(modelData)
		for j = len(modelData[i])
			cProbs[i] = modelData[i][j]

