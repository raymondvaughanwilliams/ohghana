document.addEventListener("DOMContentLoaded", function (e) {
    let smsRecipientGroupType = document.getElementById("sms-recipient-group");
    let smsRecipientCooperativeHolder = document.getElementById("sms-recipient-cooperative-holder");
    let smsRecipientSocietyHolder = document.getElementById("sms-recipient-society-holder");
    let smsRecipientCountryHolder = document.getElementById("sms-recipient-country-holder");
    let smsRecipientLanguageHolder = document.getElementById("sms-recipient-language-holder");

    function toggleRecipientGroup(groupHolders, groupName) {
        Object.values(groupHolders).map((value) => {
            value.hidden = true
        });

        if (!(groupName in groupHolders) || groupName === 'all') {
            return
        }
        groupHolders[groupName].hidden = false;
    }

    let recipientGroupHolders = {
        cooperative: smsRecipientCooperativeHolder,
        society: smsRecipientSocietyHolder,
        country: smsRecipientCountryHolder,
        language: smsRecipientLanguageHolder,
    }
    smsRecipientGroupType.addEventListener("change", function (e) {
        toggleRecipientGroup(recipientGroupHolders, this.value.trim().toLowerCase())
    });


    let templateVariables = document.getElementsByClassName("template-variable");
    let messageBody = document.getElementById("message-body");
    for (let i = 0; i < templateVariables.length; i++) {
        templateVariables[i].addEventListener("click", function (e) {
            messageBody.value = messageBody.value + `{${this.textContent.toLowerCase().trim()}}`;
            messageBody.focus();
        });
    }


    function populateGroupValues(dataSrc, attribute, holder) {
        let uniqueValues = new Set();
        for (let i = 0; i < dataSrc.length; i++) {
            if (dataSrc[i][attribute] === null) {
                continue;
            }
            uniqueValues.add(dataSrc[i][attribute].toUpperCase());
        }

        holder.innerHTML = null;
        holder.innerHTML = `<label>Select ${attribute.toLowerCase()}</label>`;
        uniqueValues.forEach((value) => {
            if (value.trim() === "") {
                value = "No value";
            }
            holder.innerHTML += `
        <div class="form-check">
             <input class="form-check-input" type="checkbox" name="selected-${attribute}" value="${value}" id="${value}" ${value.toLowerCase() === 'no value' ? 'disabled' : ''}>
                 <label class="form-check-label" for="${value}">
                     ${value}
                 </label>
         </div>
        `;
        });
    }

    let dataSrc = sessionStorage.getItem("allFarmers");
    if (dataSrc === null) {
        console.log("Fetching all farmers from session storage returned null");
        alert("Bulk sms might not work properly");
    } else {
        dataSrc = JSON.parse(dataSrc);
        populateGroupValues(dataSrc, "cooperative", smsRecipientCooperativeHolder)
        populateGroupValues(dataSrc, "society", smsRecipientSocietyHolder)
        populateGroupValues(dataSrc, "country", smsRecipientCountryHolder)
        populateGroupValues(dataSrc, "language", smsRecipientLanguageHolder)
    }


    let bulkSmsForm = document.forms["bulk-sms-form"];
    bulkSmsForm.addEventListener("reset", function (e) {
        toggleRecipientGroup(recipientGroupHolders, "");
        formFeedback.innerHTML = null;
    });

    let formFeedback = document.getElementById("bulk-sms-form-feedback");
    bulkSmsForm.addEventListener("submit", function (e) {
        e.preventDefault();
        formFeedback.innerHTML = null;

        // Contains the options selected for the recipient group
        let selectedGroupOptions = [];

        let recipientGroup = this.recipientGroup.value.trim();
        if (recipientGroup === "") {
            formFeedback.innerHTML = `<p class="alert alert-danger p-1"><i class="fa fa-exclamation-triangle"></i> Please select the recipient target group</p>`;
            return;
        }

        if (recipientGroup !== "all") {
            let checkBoxes = document.querySelectorAll(`input[name="selected-${recipientGroup}"]:checked`);
            checkBoxes.forEach((option) => {
                selectedGroupOptions.push(option.value);
            });

            if (selectedGroupOptions.length === 0) {
                formFeedback.innerHTML = `
                <p class="alert alert-danger p-1">
                <i class="fa fa-exclamation-triangle"></i> 
                You did not select any of the ${recipientGroup.toUpperCase()} options. Select at least one (1)
                </p>`;
                return;
            }
        }

        let messageBody = this.messageBody.value.trim();
        if (messageBody.length === 0 || messageBody === "") {
            formFeedback.innerHTML = `<p class="alert alert-danger p-1"><i class="fa fa-exclamation-triangle"></i> No message body supplied. Message body cannot be empty</p>`;
            return;
        }

        let templateStringRegex = /{([^}]+)}/g;
        let matches = messageBody.matchAll(templateStringRegex);
        let resultObject = {};
        for (const match of matches) {
            const extractedString = match[1];
            resultObject[extractedString] = true;
        }


        let payload = {
            recipientGroup,
            selectedGroupOptions,
            messageBody,
            templateStrings: Object.keys(resultObject),
        }

        formFeedback.innerHTML = `<p class="alert alert-info p-1"><i class="fa fa-check-circle"></i> Great! The SMS will be delivered to the recipients</p>`;

        setTimeout(() => {
            bulkSmsForm.reset();
        }, 3000)

        console.log(payload);
    });
});