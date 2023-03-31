import requests

# Valgfrie argumenter (optional arguments) som har startverdien None
def hent_data(soek=None, sidetall=None, merke=None, sortering=None):
    url = "https://kassal.app/api/v1/products"

    parametere = {
        "search": soek,
        "page": sidetall,
        "size": 15,
        "brand": merke,
        "sort": sortering
    }

    authToken = "kl5WOZbtvjPcPpLLnKYABpyQ22DnWav7ORT4ARat"
    headers = {
            "Authorization": "Bearer " + authToken,
            "Content-Type": "application/json"
        }
  
    respons = requests.get(url, parametere, headers=headers)
    data = respons.json()

    return data



# Bruk dette for å lettere kunne lese printet data i json format:


## a = hent_api("Appelsin", sortering="price_desc")

## import json
## print(json.dumps(a, indent=4))
