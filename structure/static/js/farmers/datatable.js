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
                            });
                        });
                }
            }
        }
    ],

});


