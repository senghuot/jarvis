from multiclass import Multiclass
from flask import Flask

app = Flask(__name__)

@app.route("/init")
def init():
    classifier =  Multiclass()

if __name__ == "__main__":
    app.run()