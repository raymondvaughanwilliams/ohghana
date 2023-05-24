let farmersTable = $("#farmers-table-dt").DataTable({
    dom: '<"row mb-2"<"col-12"l>>rBftip',
    ajax: {url: "/farmersapi"},
    processing: true,
    language: {
        processing: 'Loading farmers...',
    },
    columnDefs: [{
        orderable: false,
        className: 'select-checkbox',
        targets: 0
    }],
    select: {
        style: 'multi+shift',
        selector: 'td:first-child',
        info: true,
    },
    columns: [
        {
            data: null,
            render: function render(data, type, row, meta) {
                return '';
            }
        },
        {
            data: 'cooperative',
        },
        {
            data: 'farmerName',
        },
        {
            data: 'number',
        },
        {
            data: 'premiumAmount',
        },
        {
            data: 'cashcode',
        },
        {
            data: 'country',
        },
        {
            data: 'society',
        },
        {
            data: 'language',
        }
    ],
    buttons: [
        'print',
        'pdf',
        'csv',
        {
            extend: 'selectNone',
            name: 'selectNone',
        },
        {
            extend: '',
            text: 'Refresh Table',
            action: function (e, table, button, config) {
                table.ajax.reload(null, false);
            }
        },
        {
            extend: 'selected',
            text: 'Edit Farmer',
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true});
                if (selectedRows.count() !== 1) {
                    alert("Sorry, you can only edit one farmer. Kindly select only one farmer");
                    return;
                }
                let data = table.row(selectedRows.indexes()[0]).data();
                $("#edit-farmer-cooperative").val(data.cooperative);
                $("#edit-farmer-last-name").val(data.farmerName);
                $("#edit-farmer-number").val(data.number);
                $("#edit-farmer-premium-amount").val(data.premiumAmount);
                $("#edit-farmer-cash-code").val(data.cashcode);
                $("#edit-farmer-language").val(data.language);
                $("#edit-farmer-society").val(data.society);
                $("#edit-farmer-country").val(data.country);
                $('#editFarmerModal').modal('show');
            }
        },
        {
            extend: 'selected',
            text: 'Delete',
            attr: {
                class: 'ml-2 btn btn-sm btn-danger',
            },
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true}).indexes();
                let farmerIds = [];
                Array.from(selectedRows).forEach((rowIndex) => {
                    let data = table.row(rowIndex).data();
                    farmerIds.push(data.id);
                });

                if (confirm("Are you sure you want to delete?")) {
                    fetch(`/api/delete_farmers?farmers=${farmerIds.join(',')}`)
                        .then(res => res.json())
                        .then(payload => {
                            Array.from(selectedRows).forEach((row) => {
                                table.row(row).remove().draw();
                                table.ajax.reload(null, false);
                            });
                        });
                }
            }
        },

    ],
});




