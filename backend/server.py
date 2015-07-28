from multiclass import Multiclass
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from numpy import *

app = Flask(__name__)
cors = CORS(app)
classifier = None

keys = ["amount", "accountType", "bookingType", "expectedRevenue", "productCount","recordType"];
keys += ["forecastCategory", "leadSource", "annualRevenue", "employeeCount"];
keys += ["coreProduct", "locationCount", "producerCount", "oppRevenue", "oppCount"];

@app.route("/init")
def init():
  # training our model with data from multiclass folder
  global classifier
  classifier = Multiclass()
  return jsonify(message='initialized');

@app.route("/compute", methods=['GET', 'POST'])
def compute():
  # parse our json object to a matrix array
  customers = request.get_json()
  data =  parse(customers['customers'])
  data = [data, data]

  # compute the data and determine the classifier
  labels     = classifier.compute(data)
  recommends = classifier.recommend(data)

  tmps = []
  for recommend in recommends:
    tmp = {}
    for i in range(len(keys)):
      key = keys[i]
      val = recommend[i]
      tmp[key] = val
    tmps.append(tmp)

  return jsonify(label=labels, recommend=tmps)

# this is a helper method to parse the data from json into a matrix to follow
# the format and performance
def parse(data):
  res = []
  for i in range(len(data)):
    tmp_json = data[i]

    # use the keys to avoid typo
    for key in keys:
      res.append(int(tmp_json[key]))

  return res

if __name__ == "__main__":
    app.run()  