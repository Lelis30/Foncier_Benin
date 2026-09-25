document.addEventListener("DOMContentLoaded", function () {

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


    const fields = document.querySelectorAll(
        "input, select, textarea"
    );


    fields.forEach(function (field) {

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

                else if (this.validity.rangeUnderflow) {

                    this.setCustomValidity(
                        currentMessages.tooSmall
                    );

                }

                else if (this.validity.rangeOverflow) {

                    this.setCustomValidity(
                        currentMessages.tooLarge
                    );

                }

                else if (this.validity.patternMismatch) {

                    this.setCustomValidity(
                        currentMessages.pattern
                    );

                }

            }
        );

    });

});