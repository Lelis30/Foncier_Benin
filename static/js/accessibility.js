document.addEventListener("DOMContentLoaded", function () {


    // VALIDATION DES FORMULAIRES - FRANCAIS / ANGLAIS


    const language =
        document.documentElement.lang || "fr";


    const messages = {

        fr: {
            required:
                "Veuillez renseigner ce champ.",

            email:
                "Veuillez saisir une adresse e-mail valide, par exemple : nom@exemple.com.",

            url:
                "Veuillez saisir une adresse URL valide.",

            tooShort:
                "La valeur saisie est trop courte.",

            tooLong:
                "La valeur saisie est trop longue.",

            tooSmall:
                "La valeur saisie est trop petite.",

            tooLarge:
                "La valeur saisie est trop grande.",

            pattern:
                "Le format saisi n'est pas valide."
        },


        en: {
            required:
                "Please fill out this field.",

            email:
                "Please enter a valid email address, for example: name@example.com.",

            url:
                "Please enter a valid URL.",

            tooShort:
                "The value entered is too short.",

            tooLong:
                "The value entered is too long.",

            tooSmall:
                "The value entered is too small.",

            tooLarge:
                "The value entered is too large.",

            pattern:
                "The format entered is not valid."
        }
    };


    const currentMessages =
        messages[language] || messages.fr;


    const fields =
        document.querySelectorAll(
            "input, select, textarea"
        );


    fields.forEach(function (field) {

        // Effacer le message personnalisé
        // lorsque l'utilisateur modifie le champ.

        field.addEventListener(
            "input",
            function () {
                this.setCustomValidity("");
            }
        );


        field.addEventListener(
            "change",
            function () {
                this.setCustomValidity("");
            }
        );


        // Messages personnalisés de validation.

        field.addEventListener(
            "invalid",
            function () {

                this.setCustomValidity("");


                if (this.validity.valueMissing) {

                    this.setCustomValidity(
                        currentMessages.required
                    );

                }

                else if (
                    this.type === "email" &&
                    this.validity.typeMismatch
                ) {

                    this.setCustomValidity(
                        currentMessages.email
                    );

                }

                else if (
                    this.type === "url" &&
                    this.validity.typeMismatch
                ) {

                    this.setCustomValidity(
                        currentMessages.url
                    );

                }

                else if (this.validity.tooShort) {

                    this.setCustomValidity(
                        currentMessages.tooShort
                    );

                }

                else if (this.validity.tooLong) {

                    this.setCustomValidity(
                        currentMessages.tooLong
                    );

                }

                else if (
                    this.validity.rangeUnderflow
                ) {

                    this.setCustomValidity(
                        currentMessages.tooSmall
                    );

                }

                else if (
                    this.validity.rangeOverflow
                ) {

                    this.setCustomValidity(
                        currentMessages.tooLarge
                    );

                }

                else if (
                    this.validity.patternMismatch
                ) {

                    this.setCustomValidity(
                        currentMessages.pattern
                    );

                }

            }
        );

    });


    // RESTAURER LES PREFERENCES D'ACCESSIBILITE


    applyFontSize();


    const highContrast =
        localStorage.getItem(
            "foncierHighContrast"
        );


    if (highContrast === "true") {

        document.body.classList.add(
            "high-contrast"
        );

    }

});


// ACCESSIBILITE - FONCIER BENIN


// Taille du texte enregistrée.
// Valeur normale : 100 %

let fontSize = parseInt(
    localStorage.getItem("foncierFontSize")
) || 100;


// APPLIQUER LA TAILLE DU TEXTE


function applyFontSize() {

    document.documentElement.style.fontSize =
        fontSize + "%";

}


// AGRANDIR LE TEXTE


function increaseFontSize() {

    if (fontSize < 140) {

        fontSize += 10;


        localStorage.setItem(
            "foncierFontSize",
            fontSize
        );


        applyFontSize();

    }

}


// REDUIRE LE TEXTE


function decreaseFontSize() {

    if (fontSize > 80) {

        fontSize -= 10;


        localStorage.setItem(
            "foncierFontSize",
            fontSize
        );


        applyFontSize();

    }

}


// CONTRASTE ELEVE


function toggleHighContrast() {

    document.body.classList.toggle(
        "high-contrast"
    );


    const enabled =
        document.body.classList.contains(
            "high-contrast"
        );


    localStorage.setItem(
        "foncierHighContrast",
        enabled ? "true" : "false"
    );

}


// LECTURE VOCALE


function readPage() {

    if (!("speechSynthesis" in window)) {

        alert(
            "La lecture vocale n'est pas disponible dans ce navigateur."
        );

        return;

    }


    // Arrêter une éventuelle lecture en cours.

    window.speechSynthesis.cancel();


    // Lire principalement le contenu de la page.

    const main =
        document.querySelector("main") ||
        document.querySelector(".container") ||
        document.body;


    const text =
        main.innerText.trim();


    if (!text) {

        return;

    }


    const speech =
        new SpeechSynthesisUtterance(text);


    const language =
        document.documentElement.lang || "fr";


    if (language.startsWith("en")) {

        speech.lang = "en-US";

    }

    else {

        speech.lang = "fr-FR";

    }


    speech.rate = 0.9;

    speech.pitch = 1;

    speech.volume = 1;


    window.speechSynthesis.speak(
        speech
    );

}


// ARRETER LA LECTURE VOCALE


function stopReading() {

    if ("speechSynthesis" in window) {

        window.speechSynthesis.cancel();

    }

}