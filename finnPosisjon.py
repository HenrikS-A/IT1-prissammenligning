import requests

# Finner posisjonen til ip-adressen til serveren
# Jeg vet at denne er veldig dårlig, ihvertfall hjemme hos meg, men på skolen fungerer den helt greit. 
# Men jeg synes at dette er helt bra nok for dette prosjektet som ikke handler om dette her, 
# synes bare det var en litt gøy funksjon ;)

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
