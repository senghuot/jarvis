from numpy import *
from sklearn import tree
import copy


class Multiclass:

  def __init__(self):
    self.classifers = []
    self.rec_x      = []
    self.ITERATIONS = 282
    self.K          = 8
    self.train()

  # this algorithm follows directly from class
  def train(self):
    clf = tree.DecisionTreeClassifier(max_depth=5, criterion='entropy')
    train_tmp = genfromtxt('data/multiclass/multiclass-number.txt')

    # setting up hyper parameters
    TRAIN_LEN = len(train_tmp)

    # training weights
    d = [1.0/TRAIN_LEN] * TRAIN_LEN

    # build a training and recommended dataset
    train_x = []
    rec_x   = []
    train_y = []

    for i in range(0, TRAIN_LEN):
      tmp   = train_tmp[i]
      tmp_x = tmp[0:len(tmp)-1]
      tmp_y = tmp[len(tmp)-1]     

      train_x.append(tmp_x)
      train_y.append(tmp_y)
      # add x if the y is equivalent to won
      if tmp_y == 1.0:
        self.rec_x.append(tmp_x)

    # testing set
    test_tmp = genfromtxt('data/multiclass/multiclass-test.txt')
    test_x = []
    test_y = []
    for i in range(len(test_tmp)):
      tmp = test_tmp[i]
      test_x.append(tmp[0:len(tmp)-1])
      test_y.append(tmp[len(tmp)-1])

    # convert narrays to matrices
    train_x = matrix(train_x)
    self.rec_x   = matrix(self.rec_x)
    train_y = matrix(train_y).reshape(len(train_y),1)
    test_x  = matrix(test_x)
    test_y  = matrix(test_y).reshape(len(test_y),1)

    # accumulation of Ys
    final_y = [0] * len(test_y)

    for iteration in range(0, self.ITERATIONS): 
      # checking for error rate for training data
      clf = clf.fit(train_x, train_y, sample_weight=d)
      predicted_y = clf.predict(train_x)

      # Getting epsilon
      epsilon = 0
      for i in range(len(predicted_y)):
        epsilon += d[i] * self.pi(predicted_y[i], train_y[i])

      # This is to calculate the weights fo each classifier
      alpha = 1
      if epsilon != 0:
        # Updates and normalizing the weights
        alpha = math.log((1-epsilon)/epsilon) + math.log(self.K - 1)
        total_weight = 0
        for i in range(0, len(predicted_y)):
          power = alpha * self.pi(train_y[i], predicted_y[i])
          d[i] = d[i] * math.pow(math.e, power)
          total_weight += d[i]

        # Normalizing
        for i in range(0, len(predicted_y)):
          d[i] = d[i] / total_weight

      # Storing all classifer and its weight
      self.classifers.append((alpha, copy.deepcopy(clf)))

  def compute(self, test_x):
    tmp = [0, 0, 0, 0, 0, 0, 0, 0]
    for alpha, clf in self.classifers:
      predicted_y = int(clf.predict(test_x)) - 1
      tmp[predicted_y] += alpha
    return self.getIndex(tmp)


  def recommend(self, test_x):
    diff    = self.rec_x - test_x
    sim_x   = None
    sim_dis = 0
    for i in range(len(diff)):
      tmp = math.sqrt(diff[i] * diff[i].T)
      sim = 1.0 / (1 + tmp)
      if (sim > sim_dis):
        sim_dis = sim
        sim_x = self.rec_x[i]
    return sim_x


  # return the percentage of accuracy rate
  def testing(self, test_x, test_y): 
    correct = 0
    for i in range(len(test_x)):
      tmp_test_x = test_x[i]
      tmp = [0, 0, 0, 0, 0, 0, 0, 0]
      for alpha, clf in self.classifers:
        predicted_y = int(clf.predict(tmp_test_x)[0]) - 1
        tmp[predicted_y] += alpha
      # Test if the predictions are correct
      if self.getIndex(tmp) == test_y[i]:
        correct += 1
    return 1.0 * correct/len(test_x)


  # return the prediction rate
  def getIndex(self, predicted_y):
    res_val = 0
    res_index = 0
    for i in range(len(predicted_y)):
      if predicted_y[i] > res_val:
        res_val = predicted_y[i]
        res_index = i

    return res_index + 1

  # return 1 if the n1 and n2 are not equal, otherwise return 0
  def pi(self, n1, n2):
    if n1 != n2:
      return 1
    return 0
