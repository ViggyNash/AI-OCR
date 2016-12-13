
modelData = 0


def getModelData(file)
	file = open(file, 'r')
	data = file.read()
	list = data.splitlines()
	classCount = len(list) - 1
	featCount = int(list[0].strip())
	valCount = len(list[1]) / featCount

	#modelData = [x.split() for x in list]

	for i in range(1, classCount)
		line = list[i].split(' ')
		for j = range(featCount)
			for k = range(valCount)
				modelData[i][j][k] = line[j * valCount + k]


def 
