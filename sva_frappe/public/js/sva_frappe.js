function depended_dropdown(frm, filters, child, parent) {
    frm.fields_dict[child].get_query = function () {
        if (filters) {
            return {
                filters: { [parent]: filters },
                page_length: 1000
            };
        } else {
            return { filters: { [parent]: `Please select ${[parent]}` } };
        }
    }
}
async function set_value_by_role(frm,mapper) {
    let response = await get_user_permission()
    for(let item of mapper){
        if(response[item['allow']]){
            await frm.set_value(item.fieldname, response[item['allow']])
            setTimeout(async() => {
                await frm.set_df_property(item.fieldname,'read_only',1)
            }, 200);
        }
    }
}
const get_user_permission=async()=>{
    try {
        let list = await callAPI({
            method: 'sva_frappe.apis.user.get_user_role_permission',
            freeze: true,
            freeze_message: __("Getting Permissions"),
        })
        return list
    } catch (error) {
        console.error(error)
    }
}
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