
let placeholder = "";
const tekst = "Søk etter produkt, varemerke eller begge deler";
const soekefelt = document.getElementById("soekefeltet");

let i = 0;

function skriv() {
    placeholder += tekst.charAt(i);  // legger til indexen av teksten til placeholderen
    soekefelt.setAttribute("placeholder", placeholder);  // Endrer/oppdaterer placeholderen 
    i++;

    setTimeout(skriv, 40); // venter 40 ms før funksjonen kjører igjen.
};

skriv();
