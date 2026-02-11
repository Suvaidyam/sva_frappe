module.exports = {
	env: {
		browser: true,
		es2021: true,
	},
	globals: {
		role_and_permission_popup: "readonly",
		set_permission: "readonly",
		depended_dropdown: "readonly",
		action_items: "readonly",
		set_value_by_role: "readonly",
		callAPI: "readonly",
	},
	rules: {
		"no-undef": "error",
		"no-unsafe-optional-chaining": "warn",
	},
};
