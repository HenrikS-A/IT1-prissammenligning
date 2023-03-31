from flask import Flask, render_template, request
from henteData import hent_data

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/produktene")
def rute_produktene():
    produkter = hent_data(sortering="price_desc")
    return render_template("produktene.html", produkter=produkter["data"])

@app.get("/produkter")
def rute_produkter():
    s=request.args["soek"]

    produkter = hent_data(s, sortering="price_desc") # Her er s søket bruker skriver inn

    return render_template("produktene.html", soek=s, produkter=produkter["data"])







app.run(debug=True, port=5001)

