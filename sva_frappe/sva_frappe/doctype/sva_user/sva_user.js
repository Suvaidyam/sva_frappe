// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt

let my_frm = null;
var settings = {}
var level = ''
let mobilePattern = /^[6-9]\d{9}$/;
const check_multiselect = async (setting, field) => {
    let result = false
    if (setting.length > 0) {
        let item = await setting.find((item) => { return item.level == field && item.role == level })
        result = (item && item.is_multiselect == 1) ? true : false
    } else {
        result = false
    }
    return result
}
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
    let additional_fields = level_option.map(async doctype => {
        return {
            "depends_on": `eval:doc.select_doctype=='${doctype}'`,
            "fieldname": `selected_option`,
            "fieldtype": await check_multiselect(setting.role_level, doctype) ? "Table MultiSelect" : 'Link',
            "label": `Select ${doctype}`,
            "options": await check_multiselect(setting.role_level, doctype) ? `${doctype} Child` : doctype
        }
    });
    let fields_json = await Promise.all(additional_fields);
    return await new frappe.ui.Dialog({
        title: "Add User Permission",
        fields: [
            {
                "fieldname": "select_doctype",
                "fieldtype": "Autocomplete",
                "label": "Assigned Location",
                "options": level_option,
            },
            ...fields_json
        ], 
        primary_action_label: 'Submit',
        async primary_action(values) {
            try {
                let doctype = values.select_doctype;
                let selected_option = values.selected_option;
                if (await check_multiselect(setting.role_level, doctype)) {
                    for (let item of selected_option) {
                        await set_permission(doctype, item.block, my_frm);
                    }
                } else {
                    await set_permission(doctype, selected_option, my_frm);
                }
                _cb(cur_frm);
                this.hide();
            } catch (error) {
                console.error('Error setting permission:', error);
            }
        }
    })
}
//user settings
const get_level_option = (value) => {
    let data = value.filter((e) => {
        return e.role == level
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

// const render_tables = async (frm) => {
//     let list = await get_permission(frm.doc.email)
//     let tables = `<table class="table">
//     <thead>
//         <tr>
//             <th scope="col">Sr.No</th>
//             <th scope="col">User Level</th>
//             <th scope="col">Assigned Location</th>
//             <th scope="col">Action</th>
//         </tr>
//     </thead>
//     <tbody>
//     `
//     for (let i = 0; i < list?.length; i++) {
//         tables = tables + `
//         <tr>
//             <th scope="row">${i + 1}</th>
//             <td>${list?.[i].allow}</td>
//             <td>${list?.[i].name_value}</td>
//             <td class="text-danger"><a><i class="fa fa-trash-o delete-button" id="${list[i].name}" style="font-size:25px;"></i><a/></td>
//         </tr>
//             `
//     }
//     tables = tables + `</tbody>
//     </table>`;
//     document.getElementById('datatable').innerHTML = list?.length ? tables : '';
//     delete_button(frm)
// }
const render_tables = async (frm) => {
    my_frm = frm
    let list = await get_permission(frm.doc.email)
    // console.log(list);
    let tables = `
    <table class="table">
        <thead>
            <tr>
                <th scope="col"><input style="width: 15px !important; height: 15px !important;" type="checkbox" id="select-all"></th>
                <th scope="col">User Level</th>
                <th scope="col">Assigned Location</th>
                <th scope="col">Action</th>
            </tr>
        </thead>
        <tbody>
    `;
    for (let item of list) {
        tables += `
        <tr>
            <th scope="row"><input style="width: 15px !important; height: 15px !important;" type="checkbox" class="row-checkbox" data-name="${item.name}"></th>
            <td>${item.allow}</td>
            <td>${item.allow === "Company Profile" ? item.for_value : item.name_value}</td>
            <td class="text-danger"><a><i class="fa fa-trash-o delete-button" id="${item.name}" style="font-size:25px;"></i></a></td>
        </tr>
        `;
    }
    tables += `
        </tbody>
    </table>
    `
    document.getElementById('datatable').innerHTML = list?.length ? tables : '';

    const selectAllCheckbox = document.getElementById('select-all');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    const deleteSelectedButton = document.getElementById('delete-selected');

    const updateDeleteButtonVisibility = () => {
        const anyChecked = Array.from(rowCheckboxes).some(checkbox => checkbox.checked);
        deleteSelectedButton.style.display = anyChecked ? 'block' : 'none';
    };

    selectAllCheckbox.addEventListener('change', (event) => {
        const checked = event.target.checked;
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = checked;
        });
        updateDeleteButtonVisibility();
    });

    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDeleteButtonVisibility);
    });

    deleteSelectedButton.addEventListener('click', async () => {
        let selectedNames = Array.from(rowCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.dataset.name);
        if (selectedNames.length > 0) {
            await frappe.confirm('Are you sure you want to delete these permissions?',
                async () => {
                    deleteSelectedButton.style.display = 'none';
                    await multiple_delete(selectedNames)
                    selectedNames = []
                    selectAllCheckbox.checked = false;
                    rowCheckboxes.forEach(checkbox => {
                        checkbox.checked = false;
                    });
                },
                () => {
                    return
                }
            )
        }
    });
    delete_button(frm);
};

const multiple_delete = async (selectedNames) => {
    let response = await callAPI({
        method: 'sva_frappe.apis.user.delete_user_permissions',
        args: {
            permissions: selectedNames,
        },
    })
    if (response) {
        frappe.show_alert({ message: `${response} permissions deleted successfully.`, indicator: 'green' })
    }
    await render_tables(cur_frm)
}

const loop_values = async (selected_keys, doctype, frm, key) => {
    if (Array.isArray(selected_keys) && selected_keys.length > 0) {
        for (let item of selected_keys) {
            await set_permission(doctype, item[key], frm);
        }
    } else {
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
    async before_save(frm) {
        if (frm.doc.confirm_password === frm.doc.old_password) {
            !frm.is_new() && await frm.set_value('password', frm.doc.confirm_password);
        }
    },
    async refresh(frm) {
        frm.doc.old_password = frm.doc.confirm_password;
        let restricted_array = []
        let setting = await get_user_settings()
        // console.log(frappe.user_roles)
        if (setting.restriction_role_profile.length > 0) {
            if (!frappe.user.has_role("Administrator")) {
                restricted_array = setting.restriction_role_profile.map((item) => {
                    if (frappe.user_roles[0] == item.role_profile) {
                        return item.restriction_role_profile
                    }
                })
                frm.fields_dict['role_profile'].get_query = function () {
                    return {
                        filters: [
                            ['Role Profile', 'role_profile', 'NOT IN', restricted_array]
                        ],
                        page_length: 1000
                    };
                }
            }
        }
        level = frm.doc.role_profile
        !frm.is_new() && await render_tables(frm);
        if (frm.is_new()) {
            frm.set_df_property('add_permission', 'hidden', true);
        } else {
            frm.set_df_property('add_permission', 'hidden', false);
        }
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
    after_save: async function (frm) {
        let list = await get_permission(frm.doc.email)
        if (list.length == 0) {
            let d = await openDialog(async (_frm) => {
                await render_tables(_frm)
            }, frm.doc.role_profile)
            d.show()
        }
    },
    role_profile: async function (frm) {
        level = frm.doc.role_profile
    },
    validate: async function (frm) {
        if (frm.doc.mobile_number && !mobilePattern.test(frm.doc.mobile_number)) {
            frappe.throw("Please enter a valid mobile number");
        }
    },
});
