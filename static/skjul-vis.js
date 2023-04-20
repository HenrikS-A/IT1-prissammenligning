const innhold = document.getElementsByClassName("merInnhold");

for (let i = 0; i < 4; i++) {
    innhold[i].style.display = "none";
};

// ER JEG BLIND??
var lukket1 = 1;
var lukket2 = 1;
var lukket3 = 1;


function skjul_vis1() {
    if (lukket1) {
        innhold[0].style.display = "none";
        lukket1 = 0;
    } else {
        innhold[0].style.display = "block";
        lukket1 = 1;
    }
};
function skjul_vis2() {
    if (lukket2) {
        innhold[1].style.display = "none";
        lukket2 = 0;
    } else {
        innhold[1].style.display = "block";
        lukket2 = 1;
    }
};
function skjul_vis3() {
    if (lukket3) {
        innhold[2].style.display = "none";
        lukket3 = 0;
    } else {
        innhold[2].style.display = "block";
        lukket3 = 1;
    }
};