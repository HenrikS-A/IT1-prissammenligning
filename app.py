from flask import Flask, render_template
from henteData import hent_data

app = Flask(__name__)

@app.get("/")
def index():
    produkter = hent_data("taco krydder", sortering="price_desc")

    return render_template("index.html", produkter=produkter)




app.run(debug=True, port=5001)

