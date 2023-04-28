const innhold = document.getElementsByClassName("merInnhold");

var lukket = [1, 1, 1]

function skjul_vis(element) {
    if (lukket[element]) {
        innhold[element].style.display = "block";
        lukket[element] = 0;
        document.getElementById("pil" + String(element)).style.transform = "translate(0, 5px) rotate(225deg)"; // Roterer pilen til knappen du trykka på, og flytter den litt ned
    } else {
        innhold[element].style.display = "none";
        lukket[element] = 1;
        document.getElementById("pil" + String(element)).style.transform = "rotate(45deg)"; // Den vil flytte opp igjen siden jeg endrer transform igjen.
    }
};
