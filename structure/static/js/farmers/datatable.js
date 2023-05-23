// $('#farmers-table-dt thead tr')
//     .clone(true)
//     .addClass('filters')
//     .appendTo('#farmers-table-dt thead');


let farmersTable = $("#farmers-table-dt").DataTable({
    dom: 'lBftirp',
    buttons: [
        'pdf',
        'csv',
        {
            extend: 'selected',
            text: 'Delete',
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true}).indexes();
                Array.from(selectedRows).forEach((value, index) => {
                    console.log(table.row(value).data());
                    table.row(value).remove().draw();
                })
            }
        }
    ],

    columnDefs: [{
        orderable: false,
        className: 'select-checkbox',
        targets: 0
    }],
    select: {
        style: 'os',
        selector: 'td:first-child'
    },
    ajax: {url: "/farmersapi"},
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
        },
        {
            data: null,
            render: function render(data, type, row, meta) {
                return `<span class="shadow btn btn-sm btn-outline-danger text-danger"><i class="fa fa-trash-o"></i></span>`;
            },
        }
    ],
});


