from flask import Flask, render_template, request
from henteData import hent_data, hent_data_ean, hent_butikker
from finnPosisjon import finn_posisjon
import json

app = Flask(__name__)


# Fungerer ikke, må se nermere på dette.

# fil_historikk = open("historikk.json")
# historikk = json.load(fil_historikk)
# fil_historikk.close()

# historikk_liste = []

# def lagre_historikk():
#     fil_historikk = open("historikk.json", "w") # Åpner filen slik at jeg kan skrive ting inn i den.
#     json.dump(historikk_liste, fil_historikk)
#     fil_historikk.close()



@app.get("/")
def index():
    return render_template("index.html")



@app.get("/produkter")
def rute_produkter():

    # Den ser om jeg har skrevet inn et søk eller bare vil til produktsiden. Jeg har et søk når vi har argumentet "soek".
    try:
        s = request.args["soek"]
    except KeyError:
        s = None

    produkter = hent_data(s, sortering="price_asc")

    # -------- DETTE FUNGERTE IKKE, prøvde å ikke vise de som ikke har 'data' --------
    # i = 0
    # for produkt in produkter["data"]:
        
    #     ean = produkt["ean"]
    #     if ean == None:
    #         del produkter["data"][i]

    #     i += 1

        
    # for produkt in produkter["data"]:
    #     print(produkt["ean"])


    # for produkt in range(len( produkter["data"] )):
    #     try:
    #         hent_data_ean(produkter["data"][produkt]["ean"])
    #     except KeyError:
    #         del produkter["data"][produkt]
    #         print("slett")

    # for produkt in produkter["data"]:
    #     print(produkt["ean"])

    # ---------------


    # historikk_liste.append(s)
    # lagre_historikk()


    return render_template("produktene.html", soek=s, produkter=produkter["data"])



@app.get("/produkt/<ean>")
def rute_produkt(ean):
    produkt = hent_data_ean(ean)
    return render_template("produkt.html", ean=ean, produkt=produkt["data"])




@app.get("/butikker")
def rute_butikker():

    posisjon = finn_posisjon()
    koordinater = [posisjon["location"]["latitude"], posisjon["location"]["longitude"]]

    butikker = hent_butikker(koordinater[0], koordinater[1], 15) # Det siste tallet er radius fra koordinatene der den skal lete etter butikker

    return render_template("butikker.html", koordinater=koordinater, butikker=butikker["data"])




app.run(debug=True, port=5001)

