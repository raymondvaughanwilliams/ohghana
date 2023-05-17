document.addEventListener("DOMContentLoaded", function (e) {
    let smsRecipientGroupType = document.getElementById("sms-recipient-group");
    let smsRecipientCooperativeHolder = document.getElementById("sms-recipient-cooperative-holder");
    let smsRecipientSocietyHolder = document.getElementById("sms-recipient-society-holder");
    let smsRecipientCountryHolder = document.getElementById("sms-recipient-country-holder");
    let smsRecipientLanguageHolder = document.getElementById("sms-recipient-language-holder");


    function toggleRecipientGroup(groups, groupName) {
        Object.values(groups).map((value) => {
            value.hidden = true
        });

        if (!(groupName in groups) || groupName === 'all') {
            return
        }
        groups[groupName].hidden = false;
    }

    let recipientGroups = {
        cooperative: smsRecipientCooperativeHolder,
        society: smsRecipientSocietyHolder,
        country: smsRecipientCountryHolder,
        language: smsRecipientLanguageHolder,
    }

    smsRecipientGroupType.addEventListener("change", function (e) {
        toggleRecipientGroup(recipientGroups, this.value.trim().toLowerCase())
    });


    let templateVariables = document.getElementsByClassName("template-variable");
    let messageBody = document.getElementById("message-body");
    for (let i = 0; i < templateVariables.length; i++) {
        templateVariables[i].addEventListener("click", function (e) {
            messageBody.value = messageBody.value + `{${this.textContent.toLowerCase().trim()}}`;
            messageBody.focus();
        });
    }


    function populateGroupValues(groupName, holder, columnNumber) {
        let uniqueValues = new Set();
        let valuesFromTableColumn = document.querySelectorAll(`#farmers-table > tbody > tr > td:nth-child(${columnNumber})`);
        valuesFromTableColumn.forEach((element, index) => {
            uniqueValues.add(element.innerText.trim().toUpperCase());
        });

        holder.innerHTML = null;
        holder.innerHTML = `<label>Select ${groupName.toLowerCase()}</label>`;
        uniqueValues.forEach((value) => {
            holder.innerHTML += `
        <div class="form-check">
             <input class="form-check-input" type="checkbox" value="${value}" id="${value}">
                 <label class="form-check-label" for="${value}">
                     ${value}
                 </label>
         </div>
        `;
        });
    }

    populateGroupValues("cooperatives", smsRecipientCooperativeHolder, 2)
    populateGroupValues("societies", smsRecipientSocietyHolder, 8)
    populateGroupValues("countries", smsRecipientCountryHolder, 7)
    populateGroupValues("languages", smsRecipientLanguageHolder, 9)
});