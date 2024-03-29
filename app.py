from flask import Flask, render_template, request, redirect
from henteData import hent_data, hent_data_ean, hent_butikker
from finnPosisjon import finn_posisjon
from riktigPris import riktig_pris
from prishistorikk import lag_graf
import json

app = Flask(__name__)


fil = open("favorittprodukter.json")
favoritter = json.load(fil)
fil.close()

def endre_favoritter():
    formatert_favoritter = json.dumps(favoritter, indent=4) # formaterer ordboka slik at den er lett å lese i json-filen
    fil = open("favorittprodukter.json", "w") # åpner i 'write' modus
    fil.write(formatert_favoritter) # skriver til filen.
    fil.close()


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


    # Når søket gir produkter:
    if not ingen_produkter:

        # Lagrer alle ean-kodene i en liste for å passe på at samme produkt ikke vises flere ganger
        produktsoek_ean = []
        for produkt in produkter["data"]:
            if produkt["ean"] not in produktsoek_ean: 
                if produkt["ean"] != None: # Det var noen produkter som ikke har ean-kode. Jeg tar ikke de med.
                    produktsoek_ean.append(produkt["ean"])

        # På søksoversikten vil jeg bare ha dataene til det billigste produktet
        produktene_data = []
        for produktkode in produktsoek_ean:
            produkt_data = hent_data_ean(produktkode)

            # Denne sorterer listen etter pris-elementet som ligger i en liste og flere ordbøker
            # sorted tar en liste og returnerer en ny liste i stigende rekkefølge
            # sorted tar også imot en key for å bestemme sorteringen, her lambda
            # Lambda er en funksjon som finner elementet jeg vil ha (["current_price"]["price"]) og returnerer prisen, og som sorted() bruker for å sortere etter riktig ting.
            sortert_products = sorted(produkt_data["data"]["products"], key=lambda element: element["current_price"]["price"])

            billigste_produkt = sortert_products[0]
            produkt_data["data"]["products"] = billigste_produkt # Endrer api-et slik at bare det billigste vises på oversikten.
            produktene_data.append(produkt_data)
    else: # Når søket ikke gir noen produkter
        return render_template("produktene.html", soek=s, ingen_produkter=ingen_produkter, sidetall_naa=sidetall_naa)

    return render_template("produktene.html", soek=s, ingen_produkter=ingen_produkter, produkter=produktene_data, sidetall_naa=sidetall_naa, favoritter=favoritter)


@app.get("/produkt/<ean>")
def rute_produkt(ean):
    produkt_data = hent_data_ean(ean)

    #Sorterer prisen i stigende rekkefølge
    sortert_products = sorted(produkt_data["data"]["products"], key=lambda element: element["current_price"]["price"])
    billigste_produkt = sortert_products[0]

    produkt_data["data"]["products"] = sortert_products # Endrer api-et slik at rekkefølgen går etter pris.

    # Noen av produkt merkene har verdien None. Her finner jeg merket ved å sjekke til jeg finner et.
    for produkt in sortert_products:
        if produkt["brand"] != None:
            merke = produkt["brand"]
            break
        else:
            merke = ""

    # Noen av produkt infoene har verdien None. Her finner jeg infoen ved å sjekke til jeg finner et.
    for produkt in sortert_products:
        if produkt["description"] != None:
            beskrivelse = produkt["description"]
            break
        else:
            beskrivelse = ""

    # Gjør at prisen får riktig antall desimaler med funksjonen riktig_pris(). Jeg har en ny loop fordi jeg bruker break i de over.
    prisene = []
    for produkt in sortert_products:
        prisen = str(produkt["current_price"]["price"])
        pris = riktig_pris(prisen)
        prisene.append(pris)

    # Sjekker om det er allergener for produktet.
    antall_allergener = 0
    for allergen in produkt_data["data"]["allergens"]:
        if allergen["contains"] != "NO":
            antall_allergener += 1

    # Lager prishistorikk-graf med QuickChart.io
    graf = lag_graf(sortert_products)
    graf_src = graf["url"]

    return render_template("produkt.html", ean=ean, produkter=produkt_data["data"], billigst=billigste_produkt, prisene=prisene, merke=merke, beskrivelse=beskrivelse, favoritter=favoritter, antall_allergener=antall_allergener, graf_src=graf_src)


@app.post("/legg-i-favoritter")
def legg_i_favoritter():
    produkt_kode = request.form.get("produkt")
    data = hent_data_ean(produkt_kode)
    sortert_products = sorted(data["data"]["products"], key=lambda element: element["current_price"]["price"]) # sorterer etter prisen.
    
    favoritter[produkt_kode] = sortert_products[0] # index 0 er det billigste produktet, jeg trenger bare dette i json-filen.
    endre_favoritter()
    return redirect(request.referrer) # returnerer den siden som 'refererer' deg til post-requesten. Da kan jeg endre favoritter fra mange steder.

@app.post("/fjern-fra-favoritter")
def fjern_fra_favoritter():
    produkt_kode = request.form.get("produkt")
    del favoritter[produkt_kode]
    endre_favoritter()
    return redirect(request.referrer)


@app.get("/butikker")
def rute_butikker():
    # Finner posisjonen og lagrer koordniatene
    posisjon = finn_posisjon()
    koordinater = [posisjon["location"]["latitude"], posisjon["location"]["longitude"]]

    # Henter info om butikkene
    butikker = hent_butikker(koordinater[0], koordinater[1], 15) # 15km radius fra koordinatene

    return render_template("butikker.html", koordinater=koordinater, butikker=butikker["data"]) 


@app.get("/favoritter")
def rute_favoritter():
    return render_template("favoritter.html", favoritter=favoritter)


app.run(debug=True, port=5001)
