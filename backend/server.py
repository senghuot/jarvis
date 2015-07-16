from multiclass import Multiclass
from flask import Flask, request, jsonify

app = Flask(__name__)
classifier = None

@app.route("/init")
def init():
  # training our model with data from multiclass folder
  global classifier
  classifier = Multiclass()
  return 'Initialized'

@app.route("/compute")
def compute():
  # leave it here for testing only
  init()

  # compute the data and determine the classifier
  data = [[147060 ,1 ,2 ,58824 ,13 , 4, 3, 10,  350000 , 20 , 0 ,-1 , -1  ,147160,  2]]
  res = classifier.compute(data)
  return jsonify(classifier=res)

if __name__ == "__main__":
    app.run()