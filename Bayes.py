
import re

class BayesModel:

	modelData = []	#class x feature x value
	classCounts = []

	def __init__(self):
		pass

	def getModelData(self, file = 'bData.txt'):
		try:
			fileObj = open(file, 'r')
		except IOError:
			print "IOError: File "+file+" not found, unable to read model data."
			sys.exit()

		data = fileObj.read()
		list = re.split('[\n\r]',data)
		classCount = len(list) - 2
		featCount = int(list[0].strip())
		valCount = len(list[1].split(' ')) / featCount
		#print str(classCount) + " " + str(featCount) +" " +  str(valCount)

		self.modelData = [[[0 for x in range(valCount)] for y in range(featCount)] for z in range(classCount)]
		self.classCounts = [0 for x in range(classCount)]

		for i in range(0, classCount):
			line = list[i + 1].split(' ')[0:-1]
			for j in range(featCount):
				for k in range(valCount):
					self.modelData[i][j][k] = int(line[j * valCount + k])
			for k in range(valCount):
				self.classCounts[i] += self.modelData[i][0][k]
		fileObj.close()


	def bayesTraining(self, FeaturesList, LabelsList, labelMapping, valRange):

		output = str(len(FeaturesList[0])) + "\n"
		self.modelData = [[[0 for x in range(valRange + 1)] for y in range(len(FeaturesList[0]))] for z in range(len(labelMapping))]
		self.classCounts = [0 for x in range(len(labelMapping))]

		print len(self.modelData[0][0])

		for i in range(len(LabelsList)): 								#For each label
			classIdx = labelMapping.index(LabelsList[i])				#Get the class index of the given label
			self.classCounts[classIdx] += 1
			for j in range(len(FeaturesList[i])):					#For each feature the item has
				self.modelData[classIdx][j][FeaturesList[i][j]] += 1		#Increment the counter of the corresponding value
				

		for i in range(len(self.modelData)):
			for j in range(len(self.modelData[i])):
				for k in range(len(self.modelData[i][j])):
					output += str(self.modelData[i][j][k]) +  ' '
			output += '\n'

		try:
			file = open('bData.txt','w')
			file.write(output)
		except IOError:
			print "IOError: Unable to write model data to bData.txt, terminating training."
		file.close()

	def bayesTest(self, inputFeatures, labelMapping):
		
		conditionalProbs = [1 for x in range(len(self.modelData))] # Counts for input feature value given class
		for i in range(len(self.modelData)):
			for j in range(len(self.modelData[i])):
				conditionalProbs[i] *= float(self.modelData[i][j][inputFeatures[j]])/self.classCounts[i]
				#Multiply the probability of the matching value for a given feature of a given class was seen
				#print str(i) + ":" + str(j) + " " + str(float(self.modelData[i][j][inputFeatures[j]])/self.classCounts[i])


		totalI = sum(self.classCounts)
		probI = [0 for x in range(len(self.classCounts))]
		for i in range(len(self.classCounts)):
			probI[i] = conditionalProbs[i] * self.classCounts[i] / totalI

		#normalize probabilities:
		sumProbs = sum(probI)
		probI = [probI[i]/sumProbs for i in range(len(probI))]

		return labelMapping.index(str(probI.index(max(probI)))), max(probI)
