// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt

frappe.ui.form.on("District", {
   async refresh(frm) { 
        // role by permission
        set_value_by_role(frm)
        if (frm.doc.district_code != undefined && frm.doc.__unsaved!=1) {
            frm.set_df_property('district_code', 'read_only', 1)
        }
        if(frm.fields_dict.zone.df.reqd){
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
	},
    zone:function(frm){
        if(frm.fields_dict.zone.df.reqd){
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
        frm.set_value('state','')
    },
    after_save: function (frm) {
        if (frm.doc.district_code != undefined && frm.doc.__unsaved!=1) {
            frm.set_df_property('district_code', 'read_only', 1)
        }
    },
});
