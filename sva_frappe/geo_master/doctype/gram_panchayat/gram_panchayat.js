// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gram Panchayat", {
    refresh(frm) {
        depended_dropdown(frm, frm.doc.country, 'state', 'country')
    },
    country(frm) {
        depended_dropdown(frm, frm.doc.country, 'state', 'country')
        frm.set_value('state')
    },
});
