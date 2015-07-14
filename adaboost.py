from numpy import *
from sklearn import tree

ITERATIONS = 50

# this algorithm follows directly from class
def main():
  clf = tree.DecisionTreeClassifier(max_depth=1, criterion='entropy')
  train_tmp = genfromtxt('data/data-filtered-binary-number.txt')


  # setting up hyper parameters
  TRAIN_LEN = int(len(train_tmp) * (10/100.0))

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



    alpha = 1
    if epsilon != 0:
      # Updates and normalizing the weights
      alpha = 0.5 * math.log((1-epsilon)/epsilon)
      total_weight_new = 0
      for i in range(0, len(predicted_y)):
        power = -1 * alpha * train_y[i] * predicted_y[i]
        d[i] = d[i] * math.pow(math.e, power)
        total_weight_new += d[i]

      # Normalizing
      for i in range(0, len(predicted_y)):
        d[i] = d[i] / total_weight_new

    # Accumulate voting on training data
    correct = 0
    final_y += alpha * clf.predict(test_x)
    for i in range(0, len(final_y)):
      if sign(final_y[i]) == test_y[i]:
        correct += 1 
    
    print 100.0 * correct / len(final_y)

def pi(n1, n2):
  if n1 != n2:
    return 1
  return 0

if __name__ == '__main__':
  main()