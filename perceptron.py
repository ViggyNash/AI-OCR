import util
import time 

PRINT = True

class PerceptronClassifier:
  """
  Perceptron classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "perceptron"
    self.max_iterations = max_iterations
    self.weights = {}
    for label in legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use

  def setWeights(self, weights):
    assert len(weights) == len(self.legalLabels)
    self.weights == weights
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    """
    The training loop for the perceptron passes through the training data several
    times and updates the weight vector for each label based on classification errors.
    See the project description for details. 
    
    Use the provided self.weights[label] data structure so that 
    the classify method works correctly. Also, recall that a
    datum is a counter from features to values for those features
    (and thus represents a vector a values).
    """

    # Begin timer
    print 'Starting timer for perceptron training...'
    start_time = time.time()
    
    self.features = trainingData[0].keys() # could be useful later
    # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
    # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      for i in range(len(trainingData)):
          "*** YOUR CODE HERE ***"
          f = trainingData[i]
          #print f
          label = trainingLabels[i]
          guessedLabel = self.getLabelWithMaxScore(self.weights, f)
          if (guessedLabel != label):
            self.weights[label] += f
            self.weights[guessedLabel] -= f

    # Stop timer
    elapsed_time = time.time() - start_time
    print "naiveBayes training time = " + str(elapsed_time) + "s."


  def getLabelWithMaxScore(self, weights, features):
    """
    Helper function used for finding the label with the max score,
    given a set of features and their weights.
    """
    scores = util.Counter()
    for label in self.legalLabels:
      scores[label] = weights[label] * features
    return scores.argMax()


  def classify(self, data ):
    """
    Classifies each datum as the label that most closely matches the prototype vector
    for that label.  See the project description for details.
    
    Recall that a datum is a util.counter... 
    """
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.weights[l] * datum
      guesses.append(vectors.argMax())
    return guesses

  