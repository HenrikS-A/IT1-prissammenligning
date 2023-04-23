import json
import requests
from datetime import datetime


def lag_graf(produktliste):
    labels = []

    # Lagrer all data om prishistorikk
    all_prishistorikk = []
    for produkt in produktliste:
        all_prishistorikk.append(produkt["price_history"])

    # Finner den lengste liste-lengden (for å få ALLE datoene)
    listelengde = [len(i) for i in all_prishistorikk]
    lengste_listelengde = max(listelengde)

    # Finner dataen til den lengste listen
    for historikk in all_prishistorikk:
        if len(historikk) == lengste_listelengde:
            prishistorikk = historikk   # lagrer listen i variabelen prishistorikk.

    # legger inn datoene i labels så jeg får datapunkter på x-aksen på grafen.
    for tiden in prishistorikk:
        tid = tiden["date"].replace("Z", "")   # Fjerner Z for at jeg kan bruke datetime
        tid = datetime.fromisoformat(tid) # Gjør om formateringen slik at jeg lett kan finne datoer.

        # Finner dag og måned
        d = str(tid.day)
        m = str(tid.month)
        
        dato = d + "/" + m  # Kombinerer dag og måned i norsk format
        labels.append(dato) # Legger inn datoene i listen labels for å få akseverdiene.
    
    # Datoene kom inn feil vei, jeg bare reverserer listen
    labels.reverse()


    # Her finner jeg dataen jeg skal vise på grafen i datasets-lista
    datasets = []
    for produkt in produktliste:

        # Jeg vil ha bestemte farger som gjør at man kjenner igjen butikken, jeg har bestemt farge på bare de vanligste butikkene
        if produkt["store"]["name"].lower() == "meny":
            farge = "rgb(230, 0, 0)"
        elif produkt["store"]["name"].lower() == "oda":
            farge = "rgb(255, 200, 80)"
        elif produkt["store"]["name"].lower() == "kiwi":
            farge = "rgb(115, 200, 0)"
        elif produkt["store"]["name"].lower() == "spar":
            farge = "rgb(0, 125, 0)"
        elif produkt["store"]["name"].lower() == "joker":
            farge = "rgb(215, 200, 50)"
        elif produkt["store"]["name"].lower() == "coop":
            farge = "rgb(35, 90, 150)"
        else:
            farge = "rgb(0, 0, 0)"

        # Prishistorikken til det enkelte produktet
        data = []
        for pris in produkt["price_history"]:
            data.append(pris["price"])

        # Data kom også inn feil vei, jeg reverserer
        data.reverse()

        # Det er dette api-et skal ta imot
        info = {
            'label': produkt["store"]["name"],
            'backgroundColor': farge,
            'borderColor': farge,
            'fill': False,
            'data': data
        }
        datasets.append(info) # Datasets er en liste med info-ordbøker


    url = 'https://quickchart.io/chart/create'
    post_data = {
        "version": "2",
        "width": "500",
        "height": "300",
        "chart": {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': datasets,
            },
            'options': {
                'title': {
                'display': True,
                'text': produktliste[0]["name"],
                },
            },
        }
    }

    respons = requests.post(
        url,
        json=post_data,
    )

    graf_respons = json.loads(respons.text)
    return graf_respons
