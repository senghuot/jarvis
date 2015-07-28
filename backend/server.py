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

  # compute the data and determine the classifier
  labels     = classifier.compute(data)
  recommends = classifier.recommend(data)

  tmps = []
  for i in range(len(labels)):
    tmps.append({'label': labels[i], 'recommend': recommends[i]})

  won = []
  for tmp in tmps:
    if tmp['label'] == 1:
      won.append(tmp)

  progress = []
  for tmp in tmps:
    if tmp['label'] != 1 and tmp['label'] != 8:
      progress.append(tmp)

  loss = []
  for tmp in tmps:
    if tmp['label'] == 8:
      loss.append(tmp)


  won.sort(key=extract_distance, reverse=True)
  progress.sort(key=extract_distance, reverse=True)
  loss.sort(key=extract_distance, reverse=True)

  final_labels = []
  final_tmps = []

  buildList(final_labels, final_tmps, won)
  buildList(final_labels, final_tmps, progress)
  buildList(final_labels, final_tmps, loss)

  final_recommends = []
  for final_tmp in final_tmps:
    tmp = {}
    for i in range(len(keys)):
      key = keys[i]
      val = final_tmp[i]
      tmp[key] = val
    final_recommends.append(tmp)

  return jsonify(labels=final_labels, recommends=final_recommends)

def buildList(labels, tmps, listSort):
  for tmp in listSort:
    labels.append(tmp['label'])
    tmps.append(tmp['recommend']['recommend'])

# sort the object based on distance
def extract_distance(data):
  try:
    return float(data['recommend']['distance'])
  except KeyError:
    return 0


# this is a helper method to parse the data from json into a matrix to follow
# the format and performance
def parse(data):
  res = []
  for i in range(len(data)):
    tmp_json = data[i]

    # use the keys to avoid typo
    tmp_res = []
    for key in keys:
      tmp_res.append(int(tmp_json[key]))
    res.append(tmp_res)

  return res

if __name__ == "__main__":
    app.run()  