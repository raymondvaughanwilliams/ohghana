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
             <input class="form-check-input" type="checkbox" value="${value}" id="${value}" ${value.toLowerCase() === 'no value'? 'disabled': ''}>
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
    bulkSmsForm.addEventListener("submit", function (e) {
        e.preventDefault();
        let recipientGroup = this.recipientGroup.value.trim();
        console.log(recipientGroup);
    });
});