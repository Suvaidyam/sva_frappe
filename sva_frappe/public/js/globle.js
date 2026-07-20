const assign_UP = async (frm, role_names) => {
	const d = new frappe.ui.Dialog({
		title: "Assign To",
		size: "large",
		fields: [
			{
				fieldname: "assigned_roles",
				label: "",
				fieldtype: "Table",
				cannot_add_rows: 0,
				cannot_delete_rows: 0,
				in_place_edit: 1,
				data: [],
				fields: [
					{
						fieldname: "role",
						label: "Role",
						fieldtype: "Link",
						options: "Role",
						in_list_view: 1,
						reqd: 1,
						get_query() {
							let selected_roles = d?.fields_dict?.assigned_roles?.grid
								?.get_data()
								?.map((r) => r.role)
								?.filter((r) => r);
							let filtered_role = role_names?.filter(
								(r) => !selected_roles?.includes(r)
							);
							return {
								filters: {
									role_name: ["in", filtered_role ? filtered_role : [""]],
								},
							};
						},
					},
					{
						fieldname: "user",
						label: "User",
						fieldtype: "Link",
						options: "SVA User",
						in_list_view: 1,
						reqd: 1,
						get_query(doc) {
							return {
								filters: {
									role_profile: ["=", doc.role || ""],
									status: "Active",
								},
							};
						},
						onchange() {
							// This will be called when user field changes in grid
							const grid = d?.fields_dict?.assigned_roles?.grid;
							if (!grid || !this.doc) return;

							const user_id = this.get_value();
							if (!user_id) {
								this.doc.user_title = "";
								this.doc.user_email = "";
								grid.refresh();
								return;
							}

							frappe.db
								.get_value("SVA User", user_id, ["full_name", "email"])
								.then((r) => {
									if (r.message && this.doc) {
										this.doc.user_title = r.message.full_name || user_id;
										this.doc.user_email = r.message.email || "";
										grid.refresh();
									}
								});
						},
					},
					{
						fieldname: "user_title",
						label: "User Name",
						fieldtype: "Data",
						read_only: 1,
						in_list_view: 1,
					},
					{
						fieldname: "user_email",
						label: "User Email",
						fieldtype: "Data",
						read_only: 1,
						in_list_view: 1,
					},
				],
			},
		],
		primary_action_label: "Proceed",
		primary_action: async function (values) {
			let data = d.fields_dict.assigned_roles.grid.get_data();

			for (let row of data) {
				if (!row.role || !row.user) {
					frappe.msgprint("All rows must have Role and User filled.");
					return;
				}
			}
			await frappe.xcall("sva_frappe.api.set_assigned_user_permission", {
				parent: frm.doc.name,
				assigned_roles: data,
				allow_doctype: frm.doctype,
			});
			frappe.show_alert({
				message: "Assigned Successfully",
				indicator: "green",
			});

			d.hide();
			frm.reload_doc();
		},
	});
	let existing = await frappe.xcall("sva_frappe.api.get_assigned_user_permission", {
		allow: frm.doctype,
		for_value: frm.doc.name,
	});
	if (existing?.length > 0) {
		d?.set_df_property(
			"assigned_roles",
			"data",
			existing.map((item) => ({
				role: item.role,
				user: item.user,
				user_title: item.user_title || item.user,
				user_email: item.user_email,
			}))
		);
	} else {
		d.fields_dict.assigned_roles.grid.add_new_row();
	}
	d.show();
};

frappe.ui.form.on("*", {
	refresh: async function (frm) {
		let user_settings = await frappe.xcall("sva_frappe.api.get_user_settings");
		let role_names = user_settings?.role_level
			?.filter((item) => item.level == frm.doctype)
			?.map((item) => item.role);
		let allowed_assign_to = user_settings?.visible_assign_to?.map((item) => item.role);
		if (
			role_names?.length > 0 &&
			(!allowed_assign_to?.length ||
				allowed_assign_to?.some((item) => frappe.user.has_role(item)) ||
				frappe.user.has_role("Administrator"))
		) {
			frm.page.add_menu_item(__("Assign To"), () => {
				assign_UP(frm, role_names);
			});
		}
	},
});
