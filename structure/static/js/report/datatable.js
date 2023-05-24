let farmersTable = $("#report-table").DataTable({
    dom: '<"row mb-2"<"col-12"l>>rBftip',
    ajax: {url: "/api/logs"},
    // ordering: false,
    order: [],
    processing: true,
    language: {
        processing: 'Loading reports...',
    },
    columns: [
        {
            data: 'timestamp',
        },
        {
            data: null,
            render: function (data, type, row, meta) {
                return data.farmerName.toUpperCase();
            }
        },
        {
            data: 'number',
        },
        {
            data: null,
            render: function (data, type, row, meta) {
                if (data.disposition === null || data.disposition === undefined) {
                    return "<span class='badge-pill badge-secondary'>Unknown</span>";
                }
                return data.disposition.trim() === "200" ? "<span class='badge-pill badge-success'>Yes</span>" : "<span class='badge-pill badge-danger'>No</span>";
            }
        },
        {
            data: null,
            render: function (data, type, row, meta) {
                if (data.smsDisposition === null || data.smsDisposition === undefined) {
                    return "Unknown";
                }

                const smsStatus = {
                    successful: "1701",
                    noCredit: "1025",
                    ipNotAuthenticated: "69",
                    noSmsSent: "no sms sent"
                };

                switch (data.smsDisposition.toLowerCase()) {
                    case smsStatus.successful:
                        return "<span class='shadow font-weight-bold badge badge-pill badge-success'>Successful</span>";
                    case smsStatus.noCredit:
                        return `<span class="shadow font-weight-bold badge badge-pill badge-warning">Pending (${smsStatus.noCredit})</span>`;
                    case smsStatus.ipNotAuthenticated:
                        return `<span class="shadow font-weight-bold badge badge-pill badge-warning">Pending (${smsStatus.ipNotAuthenticated})</span>`;
                    case smsStatus.noSmsSent:
                        return "<span class='shadow font-weight-bold badge badge-pill badge-dark'>No SMS sent</span>";
                    default:
                        return "<span class='shadow font-weight-bold badge badge-pill badge-secondary'>Unknown</span>";
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




