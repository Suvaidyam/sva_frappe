// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt


var settings = {}
var level = ''

const openDialog = async (_cb, role_profile) => {
    var doctypes = settings?.role_doctype_mapping?.filter((e) => e.doctyperef && e.role_profile == role_profile);
    const doctypes_arr = settings?.role_doctype_mapping
        ?.filter(e => e.doctyperef && e.role_profile === role_profile)
        .map(e => e.doctyperef) || [];
    if (!doctypes) {
        doctypes = settings?.doctype_which_is_shown_in_user_permission?.split(",").map(e => e.trim()).filter(f => f).join("\n");
    }
    let setting = await get_user_settings()
    let level_option = get_level_option(setting.role_level)
    return new frappe.ui.Dialog({
        title: "Add User Permission",
        fields: [
            {
                "fieldname": "select_doctype",
                "fieldtype": "Autocomplete",
                "label": "Select Doctype",
                "options": level_option,
            },
            {
                "depends_on": "eval:doc.select_doctype==\"Zone\"",
                "fieldname": "select_zones",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select Zone",
                "options": setting.is_multiselect?"Zone Child":"Zone"
            },
            {
                "depends_on": "eval:doc.select_doctype==\"State\"",
                "fieldname": "select_states",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select States",
                "options": setting.is_multiselect?"State Child":"State"
            },
            {
                "depends_on": "eval:doc.select_doctype==\"Center Location\"",
                "fieldname": "select_center_locations",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select Center Location",
                "options": setting.is_multiselect?"District Child":"Center Location"
            },
            {
                "depends_on": "eval:doc.select_doctype==\"District\"",
                "fieldname": "select_districts",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select Districts",
                "options": setting.is_multiselect?"District Child":"District"
            },
            {
                "depends_on": "eval:doc.select_doctype==\"Block\"",
                "fieldname": "select_block",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select Blocks",
                "options": setting.is_multiselect?"Block Child":"Block"
            },
            {
                "depends_on": "eval:doc.select_doctype==\"Village\"",
                "fieldname": "select_villages",
                "fieldtype": setting.is_multiselect?"Table MultiSelect":'Link',
                "label": "Select Villages",
                "options": setting.is_multiselect?"Village Child":"Village"
            },
        ],
        primary_action_label: 'Submit',
        async primary_action(values) {
            let doctype = values.select_doctype;
            var selected_keys;
            switch (doctype) {
                case "Zone":
                    selected_keys = values.select_zones;
                    await loop_values(selected_keys, doctype, cur_frm, 'zone',setting.is_multiselect)
                    break;
                case "State":
                    selected_keys = values.select_states;
                    await loop_values(selected_keys, doctype, cur_frm, 'state',setting.is_multiselect)
                    break;
                case "District":
                    selected_keys = values.select_districts;
                    await loop_values(selected_keys, doctype, cur_frm, 'district',setting.is_multiselect)
                    break;
                case "Center Location":
                    selected_keys = values.select_center_locations;
                    await loop_values(selected_keys, doctype, cur_frm, 'center_location',setting.is_multiselect)
                    break;
                case "Block":
                    selected_keys = values.select_block;
                    await loop_values(selected_keys, doctype, cur_frm, 'block',setting.is_multiselect)
                    break;
                case "Grampanchayat":
                    selected_keys = values.select_grampanchayats;
                    await loop_values(selected_keys, doctype, cur_frm, 'grampanchayat',setting.is_multiselect)
                    break;
                case "Village":
                    selected_keys = values.select_villages;
                    await loop_values(selected_keys, doctype, cur_frm, 'village',setting.is_multiselect)
                    break
                default:
                    break;
            }
            _cb(cur_frm)
            this.hide();
        }
    })
}
//user settings
const get_level_option = (value)=>{
    let data = value.filter((e)=>{
        return e.role==level
    })
    return data.map(item => item.level);
}
const get_user_settings = async () => {
    try {
        let list = await callAPI({
            method: 'sva_frappe.apis.user.get_user_settings',
            freeze: true,
            args: {
                doctype: "User Settings",
                view: "List",
                order_by: "",
                group_by: '',
            },
    
            freeze_message: __("Getting Permissions"),
        })
        return list
    } catch (error) {
        console.error(error)
    }
}
const delete_button = async (frm) => {
    document.querySelectorAll(".delete-button").forEach(element => {
        element.onclick = async (e) => {
            frappe.confirm('Are you sure you want to delete this permission?',
                async () => {
                    let list = await callAPI({
                        method: 'frappe.desk.reportview.delete_items',
                        freeze: true,
                        args: {
                            items: [e.target.id],
                            doctype: "User Permission",
                        },
                        freeze_message: __("Deleting Data ..."),
                    })
                    await render_tables(frm)
                },
                () => {
                    return
                }
            )
        };
    });
}

const render_tables = async (frm) => {
    let list = await get_permission(frm.doc.email)
    let tables = `<table class="table">
    <thead>
        <tr>
            <th scope="col">Sr.No</th>
            <th scope="col">Doctype</th>
            <th scope="col">Value</th>
            <th scope="col">Action</th>
        </tr>
    </thead>
    <tbody>
    `
    for (let i = 0; i < list?.length; i++) {
        tables = tables + `
        <tr>
            <th scope="row">${i + 1}</th>
            <td>${list?.[i].allow}</td>
            <td>${list?.[i].name_value}</td>
            <td class="text-danger"><a><i class="fa fa-trash-o delete-button" id="${list[i].name}" style="font-size:25px;"></i><a/></td>
        </tr>
            `
    }
    tables = tables + `</tbody>
    </table>`;
    document.getElementById('datatable').innerHTML = list?.length ? tables : '';
    delete_button(frm)
}
const loop_values = async (selected_keys, doctype, frm, key,is_multiselect) => {
    if(is_multiselect){
        if (Array.isArray(selected_keys) && selected_keys.length) {
            for (let i = 0; i < selected_keys.length; i++) {
                await set_permission(doctype, selected_keys[i][key], frm);
            }
        } else {
            console.error('selected_keys is not an array or is empty');
        }
    }else{
        await set_permission(doctype, selected_keys, frm);
    }
}

// Calling APIs Common function
function callAPI(options) {
    return new Promise((resolve, reject) => {
        frappe.call({
            ...options,
            callback: async function (response) {
                resolve(response?.message || response?.value)
            }
        });
    })
}

// get scheme lists
const set_permission = async (doctype, values, frm) => {
    let list = await callAPI({
        method: 'sva_frappe.apis.user_permissions.create_user_permissions',
        freeze: true,
        args: {
            doc: {
                "doctype": "User Permission",
                "user": frm.doc.email,
                "allow": doctype,
                "for_value": values
            },
            action: "Save",
        },
        freeze_message: __("Saving Data"),
    })
    return list
}

//   get permissions

const get_permission = async (user) => {
    let list = await callAPI({
        method: 'sva_frappe.apis.user.get_user_permission',
        freeze: true,
        args: {
            doctype: "User Permission",
            user: user,
            view: "List",
            order_by: "",
            group_by: '',
        },

        freeze_message: __("Getting Permissions"),
    })
    return list
}

function defult_filter(field_name, filter_on, frm) {
    frm.fields_dict[field_name].get_query = function (doc) {
        return {
            filters: {
                [filter_on]: frm.doc.filter_on || `please select ${filter_on}`,
            },
        };
    }
};

function apply_filter(field_name, filter_on, frm, filter_value) {
    frm.fields_dict[field_name].get_query = function (doc) {
        return {
            filters: {
                [filter_on]: filter_value,
            },
            page_length: 1000
        };
    }
};

function extend_options_length(frm, fields) {
    fields.forEach((field) => {
        frm.set_query(field, () => {
            return { page_length: 1000 };
        });
    })
};
function hide_advance_search(frm, list) {
    for (item of list) {
        frm.set_df_property(item, 'only_select', true);
    }
};

frappe.ui.form.on("SVA User", {
    async refresh(frm) {
        level = frm.doc.role_profile
        !frm.is_new() && await render_tables(frm);
        if (frm.is_new()) {
            frm.set_df_property('add_permission', 'hidden', true);
        } else {
            frm.set_df_property('add_permission', 'hidden', false);
        }
        frm.doc.password = frm.doc.confirm_password
        hide_advance_search(frm, ["role_profile"])
    },
    state: function (frm) {
        if (frm.doc.state) {
            apply_filter("centre", "state", frm, frm.doc.state)
        } else {
            defult_filter('centre', "state", frm)
        }
    },
    add_permission: async function (frm) {
        let d = await openDialog(async (_frm) => {
            await render_tables(_frm)
        }, frm.doc.role_profile)
        d.show()
    },
    role_profile: async function (frm) {
        level = frm.doc.role_profile
    },
   
});
