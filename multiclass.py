from numpy import *
from sklearn import tree
import copy

classifers = []
ITERATIONS = 100
K = 8

# this algorithm follows directly from class
def main():
  clf = tree.DecisionTreeClassifier(max_depth=5, criterion='entropy')
  train_tmp = genfromtxt('data/multiclass/multiclass-number.txt')


  # setting up hyper parameters
  TRAIN_LEN = int(len(train_tmp) * (90/100.0))

  # training weights
  d = [1.0/TRAIN_LEN] * TRAIN_LEN

  # training our data
  train_x = []
  train_y = []

  for i in range(0, TRAIN_LEN):
    tmp = train_tmp[i]
    train_x.append(tmp[0:len(tmp)-1])
    train_y.append(tmp[len(tmp)-1])

  # Testing set
  test_x = []
  test_y = []

  for i in range(TRAIN_LEN, len(train_tmp)):
    tmp = train_tmp[i]
    test_x.append(tmp[0:len(tmp)-1])
    test_y.append(tmp[len(tmp)-1])

  # Convert narrays to matrices
  train_x = matrix(train_x)
  train_y = matrix(train_y).reshape(len(train_y),1)
  test_x  = matrix(test_x)
  test_y  = matrix(test_y).reshape(len(test_y),1)

  # Accumulation of Ys
  final_y = [0] * len(test_y)

  for iteration in range(0, ITERATIONS): 
    # Checking for error rate for training data
    clf = clf.fit(train_x, train_y, sample_weight=d)
    predicted_y = clf.predict(train_x)

    # Getting epsilon
    epsilon = 0
    for i in range(0, len(predicted_y)):
      epsilon += d[i] * pi(predicted_y[i], train_y[i])

    # This is to calculate the weights fo each classifier
    alpha = 1
    if epsilon != 0:
      # Updates and normalizing the weights
      alpha = math.log((1-epsilon)/epsilon) + math.log(K - 1)
      total_weight = 0
      for i in range(0, len(predicted_y)):
        power = alpha * pi(train_y[i], predicted_y[i])
        d[i] = d[i] * math.pow(math.e, power)
        total_weight += d[i]

      # Normalizing
      for i in range(0, len(predicted_y)):
        d[i] = d[i] / total_weight

    # Storing all classifer and its weight
    classifers.append((alpha, copy.deepcopy(clf)))

  # Now we're ready to test the accuracy from classifers
  correct = 0
  for i in range(len(test_x)):
    tmp_test_x = test_x[i]
    tmp = [0, 0, 0, 0, 0, 0, 0, 0]
    for alpha, clf in classifers:
      predicted_y = int(clf.predict(tmp_test_x)[0]) - 1
      tmp[predicted_y] += alpha
    
    # Test if the predictions are correct
    if getIndex(tmp) == test_y[i]:
      correct += 1

  print 1.0 * correct/len(test_x)


# Return the 
def getIndex(predicted_y):
  res_val = 0
  res_index = 0
  for i in range(len(predicted_y)):
    if predicted_y[i] > res_val:
      res_val = predicted_y[i]
      res_index = i

  return res_index + 1

# Return 1 if the n1 and n2 are not equal, otherwise return 0
def pi(n1, n2):
  if n1 != n2:
    return 1
  return 0

if __name__ == '__main__':
  main()