import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./geography_details.vue";
class GeographyDetails {
    constructor({ wrapper, hierarchy_level_field, geography_details_field, geography_title, frm, read_only, disable_save_btn = false, filters = [], preserve_data = {}, existing_data = [] }) {
        this.$wrapper = $(wrapper);
        this.app = null;
        this.hierarchy_level_field = hierarchy_level_field;
        this.geography_details_field = geography_details_field;
        this.geography_title = geography_title;
        this.frm = frm;
        this.read_only = read_only;
        this.filters = filters;
        this.disable_save_btn = disable_save_btn;
        this.preserve_data = preserve_data;
        this.existing_data = existing_data;
        this.init();
    }

    init(refresh) {
        !refresh && this.setup_app();
    }

    cleanup() {
        if (this.app) {
            try {
                this.app.unmount();
                this.app = null;
            } catch (e) {
                console.warn('Error during cleanup:', e);
            }
        }
    }

    refresh() {
        this.cleanup();
        this.setup_app();
    }

    setup_app() {
        // create a pinia instance
        let pinia = createPinia();
        // create a vue instance with dynamic props
        this.app = createApp(App, {
            hierarchy_level_field: this.hierarchy_level_field,
            geography_details_field: this.geography_details_field,
            geography_title: this.geography_title,
            frm: this.frm,
            read_only: this.read_only,
            disable_save_btn: this.disable_save_btn,
            filters: this.filters,
            preserve_data: this.preserve_data,
            existing_data: this.existing_data,
        });
        SetVueGlobals(this.app);
        this.app.use(pinia);


        // mount the app only if wrapper exists
        if (this.$wrapper && this.$wrapper.get(0)) {
            this.app.mount(this.$wrapper.get(0));
        } else {
            console.warn('Wrapper element not found for mounting Vue app');
        }
    }
}

frappe.provide("frappe.ui");
frappe.ui.GeographyDetails = GeographyDetails;
export default GeographyDetails;