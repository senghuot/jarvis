from multiclass import Multiclass
from flask import Flask, request, jsonify
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
classifier = None

@app.route("/init")
def init():
  # training our model with data from multiclass folder
  global classifier
  classifier = Multiclass()
  return jsonify(message='initialized');

@app.route("/compute", methods=['GET', 'POST'])
def compute():
  # test posting
  data = request.get_json()
  print data['message']
  
  # leave it here for testing only
  init()

  # compute the data and determine the classifier
  data = [[147060 ,1 ,2 ,58824 ,13 , 4, 3, 10,  350000 , 20 , 0 ,-1 , -1  ,147160,  2]]
  res = classifier.compute(data)
  return jsonify(classifier=res)

if __name__ == "__main__":
    app.run()  