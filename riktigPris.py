
def riktig_pris(pris):
    
    # Sjekker om komma er på riktig plass
    if pris[-3] != ".": 
        if "." not in pris: # Sjekker om det finnes komma
            return pris + ".00"
        elif pris[-2] == ".": # Sjekker om det bare er én desimal.
            return pris + "0"
        
    return pris
