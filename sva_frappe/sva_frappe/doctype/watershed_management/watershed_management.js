// Copyright (c) 2025, suvaidyam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Watershed Management', {
    refresh(frm) {
        let layout_element = document.createElement('div');
        frm.set_df_property('layout', 'options', layout_element);
        frappe.require("geography_details.bundle.js").then(() => {
            new frappe.ui.GeographyDetails({
                wrapper: layout_element,
                hierarchy_level_field: 'lowest_hierarchy',
                geography_details_field: 'geography_details',
                geography_title: 'Geography Details',
                frm: frm
            });
        })

    },
});
