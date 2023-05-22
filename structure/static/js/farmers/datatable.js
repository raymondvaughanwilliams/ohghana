// $('#farmers-table-dt thead tr')
//     .clone(true)
//     .addClass('filters')
//     .appendTo('#farmers-table-dt thead');


let farmersTable = $("#farmers-table-dt").DataTable({
    dom: 'Bfltirp',
    // fixedHeader: true,
    // fixedColumns: {
    //     left: 2,
    // },
    autoWidth: false,
    // orderCellsTop: true,
    deferRender: true,
    scrollY: 500,
    scroller: true,
    // select: true,
    ajax: {url: "/farmersapi"},
    // responsive: {
    //     breakpoints: [
    //         {name: 'bigdesktop', width: Infinity},
    //         {name: 'meddesktop', width: 1480},
    //         {name: 'smalldesktop', width: 1280},
    //         {name: 'medium', width: 1188},
    //         {name: 'tabletl', width: 1024},
    //         {name: 'btwtabllandp', width: 848},
    //         {name: 'tabletp', width: 768},
    //         {name: 'mobilel', width: 480},
    //         {name: 'mobilep', width: 320}
    //     ]
    // },
    columns: [
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
    initComplete: function () {
        var api = this.api();

        // For each column
        api
            .columns()
            .eq(0)
            .each(function (colIdx) {
                // Set the header cell to contain the input element
                var cell = $('.filters th').eq(
                    $(api.column(colIdx).header()).index()
                );
                var title = $(cell).text();
                $(cell).html('<input type="text" placeholder="' + title + '" />');

                // On every keypress in this input
                $(
                    'input',
                    $('.filters th').eq($(api.column(colIdx).header()).index())
                )
                    .off('keyup change')
                    .on('change', function (e) {

                        // Get the search value
                        $(this).attr('title', $(this).val());
                        var regexr = '({search})'; //$(this).parents('th').find('select').val();

                        var cursorPosition = this.selectionStart;
                        // Search the column for that value
                        api
                            .column(colIdx)
                            .search(
                                this.value != ''
                                    ? regexr.replace('{search}', '(((' + this.value + ')))')
                                    : '',
                                this.value != '',
                                this.value == ''
                            )
                            .draw();
                    })
                    .on('keyup', function (e) {
                        e.stopPropagation();

                        $(this).trigger('change');
                        $(this)
                            .focus()[0]
                            .setSelectionRange(cursorPosition, cursorPosition);
                    });
            });
    },
});


