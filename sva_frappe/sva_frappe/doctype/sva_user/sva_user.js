// Copyright (c) 2024, suvaidyam and contributors
// For license information, please see license.txt

let my_frm = null;
var settings = {};
var level = "";
let mobilePattern = /^[6-9]\d{9}$/;

const get_level_option = (value) => {
	let data = value.filter((e) => {
		return e.role == level;
	});
	return data.map((item) => item.level);
};
const get_user_settings = async () => {
	try {
		let list = await callAPI({
			method: "sva_frappe.apis.user.get_user_settings",
			freeze: true,
			args: {
				doctype: "User Settings",
				view: "List",
				order_by: "",
				group_by: "",
			},

			freeze_message: __("Getting Permissions"),
		});
		return list;
	} catch (error) {
		console.error(error);
	}
};

const loop_values = async (selected_keys, doctype, frm, key) => {
	if (Array.isArray(selected_keys) && selected_keys.length > 0) {
		for (const item of selected_keys) {
			await set_permission(doctype, item[key], frm);
		}
	} else {
		await set_permission(doctype, selected_keys, frm);
	}
};

// Calling APIs Common function
function callAPI(options) {
	return new Promise((resolve, reject) => {
		frappe.call({
			...options,
			callback: async function (response) {
				resolve(response?.message || response?.value);
			},
		});
	});
}

const get_permission = async (user) => {
	let list = await callAPI({
		method: "sva_frappe.apis.user.get_user_permission",
		freeze: true,
		args: {
			doctype: "User Permission",
			user: user,
			view: "List",
			order_by: "",
			group_by: "",
		},
		freeze_message: __("Getting Permissions"),
	});
	return list;
};

function defult_filter(field_name, filter_on, frm) {
	frm.fields_dict[field_name].get_query = function (doc) {
		return {
			filters: {
				[filter_on]: frm.doc.filter_on || `please select ${filter_on}`,
			},
		};
	};
}

function apply_filter(field_name, filter_on, frm, filter_value) {
	frm.fields_dict[field_name].get_query = function (doc) {
		return {
			filters: {
				[filter_on]: filter_value,
			},
			page_length: 1000,
		};
	};
}

function extend_options_length(frm, fields) {
	fields.forEach((field) => {
		frm.set_query(field, () => {
			return { page_length: 1000 };
		});
	});
}
function hide_advance_search(frm, list) {
	for (const item of list) {
		frm.set_df_property(item, "only_select", true);
	}
}

frappe.ui.form.on("SVA User", {
	async refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Impersonate"), () => {
				if (frm.doc.restrict_ip) {
					frappe.msgprint({
						title: __("IP restriction is enabled"),
						message: __(
							"There's IP restriction for this user, you cannot impersonate as this user."
						),
					});
					return;
				}

				frappe.prompt(
					[
						{
							fieldname: "reason",
							fieldtype: "Small Text",
							label: __("Reason for impersonating"),
							description: __("Note: This will be shared with the user."),
							reqd: 1,
						},
					],
					(values) => {
						frappe
							.xcall("frappe.core.doctype.user.user.impersonate", {
								user: frm.doc.email,
								reason: values.reason,
							})
							.then(() => {
								window.location.reload();
							});
					},
					__("Impersonate as {0}", [frm.doc.name]),
					__("Confirm")
				);
			});
			frm.add_custom_button(
				__("Reset Password"),
				function () {
					frappe.call({
						method: "frappe.core.doctype.user.user.reset_password",
						args: {
							user: frm.doc.email,
						},
					});
				},
				__("Password")
			);
		}

		if (frm.doc.role_profile) {
			role_and_permission_popup(frm);
		}
		let restricted_array = [];
		let setting = await get_user_settings();
		// console.log(frappe.user_roles)
		if (setting.restriction_role_profile.length > 0) {
			if (!frappe.user.has_role("Administrator")) {
				restricted_array = setting.restriction_role_profile.map((item) => {
					if (frappe.user_roles[0] == item.role_profile) {
						return item.restriction_role_profile;
					}
				});
				frm.fields_dict["role_profile"].get_query = function () {
					return {
						filters: [["Role Profile", "role_profile", "NOT IN", restricted_array]],
						page_length: 1000,
					};
				};
			}
		}
		level = frm.doc.role_profile;
		hide_advance_search(frm, ["role_profile"]);
		let level_option = await get_level_option(setting.role_level);
		frm.fields_dict["table_pdop"].grid.get_field("module").get_query = function (
			doc,
			cdt,
			cdn
		) {
			return {
				filters: {
					name: ["in", level_option],
				},
			};
		};
	},

	state: function (frm) {
		if (frm.doc.state) {
			apply_filter("centre", "state", frm, frm.doc.state);
		} else {
			defult_filter("centre", "state", frm);
		}
	},

	role_profile: async function (frm) {
		level = frm.doc.role_profile;
		role_and_permission_popup(frm);
	},

	validate: async function (frm) {
		if (frm.doc.mobile_number && !mobilePattern.test(frm.doc.mobile_number)) {
			frappe.throw("Please enter a valid mobile number");
		}
	},
});
