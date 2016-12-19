# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math
import time

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.classProbabilities = 0
    self.featureProbabilities = 0
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    "*** YOUR CODE HERE ***"

    # Begin timer
    print 'Starting timer for naiveBayes training...'
    start_time = time.time()

    featureValCounts = [[[0 for x in range(2)] for y in range(len(self.features))] for z in range(len(self.legalLabels))]
    classCounts = [0 for x in range(len(self.legalLabels))]
    # Count class instances and feature value instances
    for i in range(len(trainingLabels)):                                   #For each label
      classCounts[self.legalLabels.index(trainingLabels[i])] += 1          #Increment the count of the corresponding class
      for j in range(len(self.features)):                                  #For each feature the item has
        featureValCounts[trainingLabels[i]][j][trainingData[i][self.features[j]]] += 1    #Increment the counter of the corresponding value
        #print str(trainingData[i][self.features[j]]) + " " + str(featureValCounts[trainingLabels[i]][j][0]) +","+str(featureValCounts[trainingLabels[i]][j][1])
      #print ''
      #print trainingData[i]

    # Calculate class probabilities
    totalCount = sum(classCounts)
    self.classProbabilities = [classCounts[i]/float(totalCount) for i in range(len(classCounts))]

    # Set up feature probabilities matrix
    self.featureProbabilities = [[[0 for x in range(2)] for y in range(len(self.features))] for z in range(len(self.legalLabels))]

    # Test different smoothing amount
    if self.automaticTuning:
      print "Performing automatic tuning:"
      accuracy = []
      for x in range(len(kgrid)):
        print "\tTesting k = " + str(kgrid[x]) +":"
        self.k = kgrid[x]

        # Calculate feature value probabilities
        self.calcFeatureProbabilities(featureValCounts)

        guesses = self.classify(validationData)
        comparison = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))]

        accuracy.append(comparison.count(True) / len(comparison))
      self.k = kgrid[accuracy.index(max(accuracy))]
      print "Using k = " +str(self.k)+" for smoothing."

    self.calcFeatureProbabilities(featureValCounts)

    # Stop timer
    elapsed_time = time.time() - start_time
    print "naiveBayes training time = " + str(elapsed_time) + "s."

  def calcFeatureProbabilities(self, featureValCounts):
    for i in range(len(featureValCounts)):
      for j in range(len(featureValCounts[i])):
        count = sum(featureValCounts[i][j]) + (self.k * len(featureValCounts[i][j]))
        for k in range(len(featureValCounts[i][j])):
          self.featureProbabilities[i][j][k] = (featureValCounts[i][j][k] + self.k)/float(count)
          #print self.featureProbabilities[i][j][k]
        #print ''
      #print ''
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    "*** YOUR CODE HERE ***"
    for i in range(len(self.legalLabels)):
      logJoint[i] += math.log(self.classProbabilities[i])
      for j in range(len(self.features)):
        if self.featureProbabilities[i][j][datum[j]] != 0:
          logJoint[i] += math.log(self.featureProbabilities[i][j][datum[self.features[j]]])

    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    for i in range(len(self.features)):
      featuresOdds.append((i, self.featureProbabilities[label1][i][1] / self.featureProbabilities[label2][i][1]))

    sortedOdds = sorted(featuresOdds, key = lambda item: item[1], reverse=True)
    if len(sortedOdds) >= 100:
      sortedOdds = sortedOdds[:100]

    featuresOdds = [item[1] for item in sortedOdds]
    #util.raiseNotDefined()

    return featuresOdds
    

    
      
