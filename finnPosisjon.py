import requests

# Denne finner posisjonen til ip-adressen til serveren

def finn_posisjon():
    url = "https://api.ipregistry.co"

    authToken = "ilveqm4mug3vrkyu"
    headers = {
            "Authorization": "ApiKey " + authToken,
            "Content-Type": "application/json"
        }
  
    respons = requests.get(url, headers=headers)
    data = respons.json()

    return data
