
# Gjør at prisen vises på vanlig måte med 2 desimaler for øre.
def riktig_pris(pris):
    # Sjekker om dette fungerer først, men kan få indexerror hvis prisen er liten (har ikke 3 tegn)
    try:
        # Sjekker om komma er på riktig plass
        if pris[-3] != ".": 
            if "." not in pris: # Sjekker om det finnes komma
                return pris + ".00"
            elif pris[-2] == ".": # Sjekker om det bare er én desimal.
                return pris + "0"
        return pris
    except IndexError:
            if "." not in pris: # Sjekker om det finnes komma
                return pris + ".00"
            elif pris[-2] == ".": # Sjekker om det bare er én desimal.
                return pris + "0"
