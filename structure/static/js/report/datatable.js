let farmersTable = $("#report-table").DataTable({
    dom: '<"row mb-2"<"col-12"l>>rBftip',
    ajax: {url: "/api/logs"},
    processing: true,
    language: {
        processing: 'Loading reports...',
    },
    columns: [
        {
            data: 'timestamp',
        },
        {
            data: 'farmerName',
        },
        {
            data: 'number',
        },
        {
            data: null,
            render: function (data, type, row, meta) {
                return data.disposition.trim() === "200" ? "Yes" : "No";
            }
        },
        {
            data: null,
            render: function (data, type, row, meta) {
                console.log(data);
                if (data.smsDisposition === null || data.smsDisposition === undefined) {
                    return "Unknown";
                }

                const smsStatus = {
                    successful: "1701",
                    noCredit: "1025",
                    ipNotAuthenticated: "69",
                };

                switch (data.smsDisposition) {
                    case smsStatus.successful:
                        return "<span class='shadow font-weight-bold badge badge-pill badge-success'>Successful</span>";
                    case smsStatus.noCredit:
                        return `<span class="shadow font-weight-bold badge badge-pill badge-warning">Pending (${smsStatus.noCredit})</span>`;
                    case smsStatus.ipNotAuthenticated:
                        return `<span class="shadow font-weight-bold badge badge-pill badge-warning">Pending (${smsStatus.ipNotAuthenticated})</span>`;
                    default:
                        return "Unknown";
                }
            }
        },
    ],
    buttons: [
        'print',
        'pdf',
        'csv',
        {
            extend: '',
            text: 'Refresh Table',
            action: function (e, table, button, config) {
                table.ajax.reload(null, false);
            }
        },
    ],
});




