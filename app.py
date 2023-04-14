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
    s = request.args.get("soek")

    # Sidetall
    try:
        sidetall_naa = int(request.args.get("sidetall"))
    except (ValueError, TypeError):
        sidetall_naa = 1

    # Lagrer produktene hentet fra API-en
    produkter = hent_data(s, sidetall=sidetall_naa, sortering="price_asc")

    # Sjekker om det du søkte på finnes i databasen.
    if len(produkter["data"]) < 1:
        ingen_produkter = True
    else:
        ingen_produkter = False



    # Når søket gav produkter:
    if ingen_produkter == False:

        # Lagrer alle ean-kodene i en liste for å passe på at samme produkt ikke vises flere ganger
        produktsoek_ean = []
        for produkt in produkter["data"]:
            if produkt["ean"] not in produktsoek_ean: 
                if produkt["ean"] != None: # Det var noen produkter som ikke har ean-kode. Jeg tar ikke de med.
                    produktsoek_ean.append(produkt["ean"])


        # Så lagrer den dataen til BARE det BILLIGSTE produktet i en ny liste. Dataen finner jeg med ean-kodene og funksjonen hent_data_ean.
        produktene_data = []
        for produktkode in produktsoek_ean:
            produkt_data = hent_data_ean(produktkode)

            # Denne sorterer listen etter pris-elementet som ligger i en liste og flere ordbøker
            # Lambda er en funksjon som finner det jeg leter etter inne ordboken og som sorted() bruker for å sortere riktig.
            sortert_products = sorted(produkt_data["data"]["products"], key=lambda element: element["current_price"]["price"])

            billigste_produkt = sortert_products[0] # Billigste vil ha index 0.
            produkt_data["data"]["products"] = billigste_produkt # Endrer api-ets fil slik at bare det billigste vises på oversikten.
            produktene_data.append(produkt_data)


    # Når søket ikke gir noen produkter
    else:
        return render_template("produktene.html", soek=s, ingen_produkter=ingen_produkter, sidetall_naa=sidetall_naa)


    # historikk_liste.append(s)
    # lagre_historikk()


    return render_template("produktene.html", soek=s, ingen_produkter=ingen_produkter, produkter=produktene_data, sidetall_naa=sidetall_naa)



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

