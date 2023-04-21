const innhold = document.getElementsByClassName("merInnhold");

var lukket = [1, 1, 1]

function skjul_vis(element) {
    if (lukket[element]) {
        innhold[element].style.display = "block";
        lukket[element] = 0;
    } else {
        innhold[element].style.display = "none";
        lukket[element] = 1;
    }
};
