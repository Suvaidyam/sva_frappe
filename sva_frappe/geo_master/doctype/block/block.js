// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt

frappe.ui.form.on("Block", {
	refresh(frm) {
        if (frm.doc.block_code != undefined && frm.doc.__unsaved!=1) {
            frm.set_df_property('block_code', 'read_only', 1)
        }
        if(frm.fields_dict.zone.df.reqd){
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
        depended_dropdown(frm, frm.doc.state, 'district', 'state')
	},
    zone:function(frm){
        if(frm.fields_dict.zone.df.reqd){
            depended_dropdown(frm, frm.doc.zone, 'state', 'zone')
        }
        frm.set_value('state','')
    },
    state:function(frm){
        depended_dropdown(frm, frm.doc.state, 'district', 'state')
        frm.set_value('district')
    },
    after_save: function (frm) {
        if (frm.doc.block_code != undefined && frm.doc.__unsaved!=1) {
            frm.set_df_property('block_code', 'read_only', 1)
        }
    },
});
