frappe.listview_settings['SVA User'] = {
    onload:async function (listview) {
        if(!frappe.user_roles.includes('Administrator')){
            action_items(listview, ['Export', 'Delete'])
        }
        let setting = await get_user_settings()
        $('.layout-side-section').hide();
        $('.sidebar-section.filter-section').hide();
        $('.sidebar-section.save-filter-section').hide();
        if(setting.hide_user_table_view_settings){
            $(".custom-actions").hide();
        }
    },
    refresh:async function (listview) {
        let setting = await get_user_settings()
        $(".list-row-activity").hide();
        $("use.like-icon").hide();
        if(setting.hide_user_table_view_settings){
            $(".custom-actions").hide();
        }
    }
};

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