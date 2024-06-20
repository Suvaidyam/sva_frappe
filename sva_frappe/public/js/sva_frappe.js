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
async function set_value_by_role(frm) {
    let response = await get_user_permission()
    if(response['Zone']){
        await frm.set_value('zone', response['Zone'])
        setTimeout(async() => {
            await   frm.set_df_property('zone','read_only',1)
        }, 200);
    }
    if(response['State']){
        await frm.set_value('state', response['State'])
        setTimeout(async() => {
            await   frm.set_df_property('state','read_only',1)
        }, 200);
    }
    if(response['District']){
        await frm.set_value('district', response['District'])
        setTimeout(async() => {
            await   frm.set_df_property('district','read_only',1)
        }, 200);
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