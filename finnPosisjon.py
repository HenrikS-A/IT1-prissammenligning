import requests

# Jeg vet at denne finner posisjonen til serveren, men tenker det er bra nok for dette prosjektet 
# siden du kjører serveren på pc-en din. 

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
