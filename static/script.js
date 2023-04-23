
let placeholder = "";
const tekst = "Søk etter produkt, varemerke eller begge deler";
const soekefelt = document.getElementById("soekefeltet");

let i = 0;

function skriv() {

    placeholder += tekst.charAt(i);
    soekefelt.setAttribute("placeholder", placeholder);
    i++;

    setTimeout(skriv, 40);
    
};

skriv();
