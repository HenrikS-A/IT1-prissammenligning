import requests

# Valgfrie argumenter (optional arguments) som har startverdien None
def hent_data(soek=None, sidetall=None, merke=None, sortering=None):
    url = "https://kassal.app/api/v1/products"

    parametere = {
        "search": soek,
        "page": sidetall,
        "size": 15,
        "brand": merke,
        "price_min": 1, # flesteparten av produktene under 15kr er ikke veldig interessante, man kan justere her.
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


def hent_data_ean(ean):
    url = f"https://kassal.app/api/v1/products/ean/{ean}" # Annen måte å legge inn parametere, her skal jeg bare ha 1'

    authToken = "kl5WOZbtvjPcPpLLnKYABpyQ22DnWav7ORT4ARat"
    headers = {
            "Authorization": "Bearer " + authToken,
            "Content-Type": "application/json"
        }
  
    respons = requests.get(url, headers=headers)
    data = respons.json()

    return data


def hent_butikker(lat, lng, km=None):
    url = "https://kassal.app/api/v1/physical-stores"

    parametere = {
        "size": 10,
        "lat": lat,
        "lng": lng,
        "km": km
    }

    authToken = "kl5WOZbtvjPcPpLLnKYABpyQ22DnWav7ORT4ARat"
    headers = {
            "Authorization": "Bearer " + authToken,
            "Content-Type": "application/json"
        }
  
    respons = requests.get(url, parametere, headers=headers)
    data = respons.json()

    return data
