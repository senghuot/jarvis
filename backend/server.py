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
  # leave it here for testing only
  # init()

  # parse our json object to a matrix array
  customers = request.get_json()
  data =  parse(customers['customers'])
  
  # # compute the data and determine the classifier
  res = classifier.compute(data)
  return jsonify(classifier=res)

# this is a helper method to parse the data from json into a matrix to follow
# the format and performance
def parse(data):
  res = []
  for i in range(len(data)):
    tmp_json = data[i]
    tmp_array = []

    tmp_array.append(tmp_json['amount'])
    tmp_array.append(tmp_json['accountType'])
    tmp_array.append(tmp_json['bookingType'])
    tmp_array.append(tmp_json['expectedRevenue'])
    tmp_array.append(tmp_json['producerCount'])
    tmp_array.append(tmp_json['recordType'])
    tmp_array.append(tmp_json['forecastCategory'])
    tmp_array.append(tmp_json['leadSource'])
    tmp_array.append(tmp_json['annualRevenue'])
    tmp_array.append(tmp_json['employeeCount'])
    tmp_array.append(tmp_json['coreProduct'])
    tmp_array.append(tmp_json['locationCount'])
    tmp_array.append(tmp_json['producerCount'])
    tmp_array.append(tmp_json['oppRevenue'])
    tmp_array.append(tmp_json['oppCount'])

    res.append(tmp_array)

  return res

if __name__ == "__main__":
    app.run()  