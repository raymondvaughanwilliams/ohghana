document.addEventListener("DOMContentLoaded", function (e) {
    let smsRecipientGroupType = document.getElementById("sms-recipient-group");
    let smsRecipientCooperativeHolder = document.getElementById("sms-recipient-cooperative-holder");
    let smsRecipientCooperative = document.getElementById("sms-recipient-cooperative");

    let smsRecipientSocietyHolder = document.getElementById("sms-recipient-society-holder");
    let smsRecipientSociety = document.getElementById("sms-recipient-society");

    let smsRecipientCountryHolder = document.getElementById("sms-recipient-country-holder");
    let smsRecipientCountry = document.getElementById("sms-recipient-country");

    let smsRecipientLanguageHolder = document.getElementById("sms-recipient-language-holder");
    let smsRecipientLanguage = document.getElementById("sms-recipient-language");

    smsRecipientGroupType.addEventListener("change", function (e) {
        switch (this.value.toLowerCase().trim()) {
            case "cooperative":
                smsRecipientCooperative.required = true;
                smsRecipientCooperativeHolder.hidden = false;

                smsRecipientSociety.required = false;
                smsRecipientSocietyHolder.hidden = true

                smsRecipientCountry.required = false;
                smsRecipientCountryHolder.hidden = true;

                smsRecipientLanguage.required = false;
                smsRecipientLanguageHolder.hidden = true;
                break;

            case "society":
                smsRecipientCooperative.required = false;
                smsRecipientCooperativeHolder.hidden = true;

                smsRecipientSociety.required = true;
                smsRecipientSocietyHolder.hidden = false

                smsRecipientCountry.required = false;
                smsRecipientCountryHolder.hidden = true;

                smsRecipientLanguage.required = false;
                smsRecipientLanguageHolder.hidden = true;
                break

            case "country":
                smsRecipientCooperative.required = false;
                smsRecipientCooperativeHolder.hidden = true;

                smsRecipientSociety.required = false;
                smsRecipientSocietyHolder.hidden = true

                smsRecipientCountry.required = true;
                smsRecipientCountryHolder.hidden = false;

                smsRecipientLanguage.required = false;
                smsRecipientLanguageHolder.hidden = true;
                break;

            case "language":
                smsRecipientCooperative.required = false;
                smsRecipientCooperativeHolder.hidden = true;

                smsRecipientSociety.required = false;
                smsRecipientSocietyHolder.hidden = true

                smsRecipientCountry.required = false;
                smsRecipientCountryHolder.hidden = true;

                smsRecipientLanguage.required = true;
                smsRecipientLanguageHolder.hidden = false;
                break;

            default:
                alert("unknown recipient group");
                return;
        }
    });

    let variableSelector = document.getElementById("sms-variables");
    let variables = document.getElementsByClassName("variable");
    let messageTemplate = document.getElementById("message-body");
    let insertVariableBtn = document.getElementById("insert-variable-btn");

    variableSelector.addEventListener("change", function (e) {
        if (this.value.trim() === "") {
            return;
        }
        messageTemplate.value = messageTemplate.value + `{${this.value}}`;
        messageTemplate.focus();
    });

    insertVariableBtn.addEventListener("click", function (e) {
        e.preventDefault();
        if (variableSelector.value.trim() === "") {
            return;
        }
        messageTemplate.value = messageTemplate.value + `{${variableSelector.value.trim()}}`;
        messageTemplate.focus();
    });

    for (let i = 0; i < variables.length; i++) {
        variables[i].addEventListener("click", function(e) {
           messageTemplate.value = messageTemplate.value + `{${this.textContent.toLowerCase().trim()}}`;
           messageTemplate.focus();
        });
    }
});