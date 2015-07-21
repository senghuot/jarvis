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
  # leave it here for testing only
  # init()

  # parse our json object to a matrix array
  customers = request.get_json()
  data =  parse(customers['customers'])

  # compute the data and determine the classifier
  label     = classifier.compute(data)
  recommend = classifier.recommend(data).getA1()

  tmp = {}
  for i in range(len(keys)):
    key = keys[i]
    val = recommend[i]
    tmp[key] = val

  return jsonify(label=label, recommend=tmp)

# this is a helper method to parse the data from json into a matrix to follow
# the format and performance
def parse(data):
  res = []
  for i in range(len(data)):
    tmp_json = data[i]

    res.append(int(tmp_json['amount']))
    res.append(int(tmp_json['accountType']))
    res.append(int(tmp_json['bookingType']))
    res.append(int(tmp_json['expectedRevenue']))
    res.append(int(tmp_json['producerCount']))
    res.append(int(tmp_json['recordType']))
    res.append(int(tmp_json['forecastCategory']))
    res.append(int(tmp_json['leadSource']))
    res.append(int(tmp_json['annualRevenue']))
    res.append(int(tmp_json['employeeCount']))
    res.append(int(tmp_json['coreProduct']))
    res.append(int(tmp_json['locationCount']))
    res.append(int(tmp_json['producerCount']))
    res.append(int(tmp_json['oppRevenue']))
    res.append(int(tmp_json['oppCount']))

  return res

if __name__ == "__main__":
    app.run()  