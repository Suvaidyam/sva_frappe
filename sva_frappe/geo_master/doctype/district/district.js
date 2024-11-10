// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt
const tabContent = async (frm, tab_field) => {
    let field = frm.meta?.fields?.find(f => f.fieldname == tab_field)
    let _fields = frm.meta?.fields?.filter(f => field?.default?.split(',')?.includes(f.fieldname))
    for (let _f of _fields) {
        let link = frm.meta.links?.find(f => f.link_doctype == _f.default)
        if (link) {
            new SvaDataTable({
                wrapper: document.querySelector(`#${_f.fieldname}`), // Wrapper element
                doctype: link.link_doctype, // Doctype name
                crud: true,      // Enable CRUD operations (optional)
                frm: frm,       // Pass the current form object (optional)
                options: {
                    connection: link,
                    serialNumberColumn: true, // Enable serial number column (optional)
                    editable: false,      // Enable editing (optional),
                }
            });
        }
    }
}
frappe.ui.form.on("District", {
    async refresh(frm) {
        let tab_field = frm.get_active_tab()?.df?.fieldname;
        tabContent(frm, tab_field)
        $('a[data-toggle="tab"]').on('shown.bs.tab', async function (e) {
            let tab_field = frm.get_active_tab()?.df?.fieldname;
            tabContent(frm, tab_field)
        });
        // role by permission
        set_value_by_role(frm, [{ fieldname: "zone", allow: "Zone" }, { fieldname: "state", allow: "State" }])
        if (frm.doc.district_code != undefined && frm.doc.__unsaved != 1) {
            frm.set_df_property('district_code', 'read_only', 1)
        }
        if (frm.fields_dict.zone.df.reqd) {
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
    },
    zone: function (frm) {
        if (frm.fields_dict.zone.df.reqd) {
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
        frm.set_value('state', '')
    },
    after_save: function (frm) {
        if (frm.doc.district_code != undefined && frm.doc.__unsaved != 1) {
            frm.set_df_property('district_code', 'read_only', 1)
        }
    },
});
