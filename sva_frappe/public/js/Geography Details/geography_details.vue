<template>
    <div class="container-fluid mt-4">
        <h1 class="header text-center">{{ geography_title }}</h1>

        <!-- Add loading overlay -->
        <div class="loading-overlay" v-if="isLoading">
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="loading-text">Loading...</div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <div class="main-container" :class="{ 'loading': isLoading }">
                    <div class="step-container" :data-progress="currentStep" :data-total-steps="totalSteps">
                        <div class="step" :class="{ 'active': currentStep >= 1, 'completed': currentStep > 1 }">
                            <div class="step-number">1</div>
                            <div>States</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy !== 'State'"
                            :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
                            <div class="step-number">2</div>
                            <div>Districts</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy !== 'State' && lowest_hierarchy !== 'District'"
                            :class="{ 'active': currentStep >= 3, 'completed': currentStep > 3 }">
                            <div class="step-number">3</div>
                            <div>Blocks</div>
                        </div>
                        <div class="step"
                            v-if="lowest_hierarchy !== 'State' && lowest_hierarchy !== 'District' && lowest_hierarchy !== 'Block'"
                            :class="{ 'active': currentStep >= 4, 'completed': currentStep > 4 }">
                            <div class="step-number">4</div>
                            <div>Gram Panchayats</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy === 'Village'"
                            :class="{ 'active': currentStep >= 5, 'completed': currentStep > 5 }">
                            <div class="step-number">5</div>
                            <div>Villages</div>
                        </div>
                    </div>

                    <div v-if="currentStep === 1">
                        <h4>Available States</h4>
                        <div class="mb-3">
                            <div class="checkbox">
                                <label>
                                    <span class="input-area">
                                        <input type="checkbox" :checked="allStatesSelected" @change="toggleAllStates"
                                            class="input-with-feedback" :disabled="read_only">
                                    </span>
                                    <span class="disp-area" style="display: none;">
                                        <input type="checkbox" disabled class="disabled-deselected">
                                    </span>
                                    <span class="label-area">Select All States</span>
                                    <span class="ml-1 help"></span>
                                </label>
                                <p class="help-box small text-extra-muted"></p>
                            </div>
                        </div>
                        <div class="checkbox-container">
                            <div class="checkbox-item" v-for="(state, index) in states" :key="index">
                                <div class="checkbox">
                                    <label>
                                        <span class="input-area">
                                            <input type="checkbox" :value="state.id" v-model="selectedStates"
                                                @change="updateDistricts" class="input-with-feedback"
                                                :disabled="read_only">
                                        </span>
                                        <span class="disp-area" style="display: none;">
                                            <input type="checkbox" disabled class="disabled-deselected">
                                        </span>
                                        <span class="label-area">{{ state.name }}</span>
                                        <span class="ml-1 help"></span>
                                    </label>
                                    <p class="help-box small text-extra-muted"></p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 2">
                        <h4>Available Districts</h4>
                        <div class="mb-3">
                            <div class="checkbox">
                                <label>
                                    <span class="input-area">
                                        <input type="checkbox" :checked="allDistrictsSelected"
                                            @change="toggleAllDistricts" class="input-with-feedback"
                                            :disabled="read_only">
                                    </span>
                                    <span class="disp-area" style="display: none;">
                                        <input type="checkbox" disabled class="disabled-deselected">
                                    </span>
                                    <span class="label-area">Select All Districts</span>
                                    <span class="ml-1 help"></span>
                                </label>
                                <p class="help-box small text-extra-muted"></p>
                            </div>
                        </div>
                        <div v-for="stateId in selectedStates" :key="stateId" class="state-district-group mb-4">
                            <div class="state-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(stateId) }}</span>
                                </div>
                                <div class="checkbox">
                                    <label>
                                        <span class="input-area">
                                            <input type="checkbox" :checked="isAllDistrictsSelectedForState(stateId)"
                                                @change="toggleAllDistrictsForState(stateId)"
                                                class="input-with-feedback" :disabled="read_only">
                                        </span>
                                        <span class="disp-area" style="display: none;">
                                            <input type="checkbox" disabled class="disabled-deselected">
                                        </span>
                                        <span class="label-area">Select All</span>
                                        <span class="ml-1 help"></span>
                                    </label>
                                    <p class="help-box small text-extra-muted"></p>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="district in getDistrictsForState(stateId)"
                                    :key="district.id">
                                    <div class="checkbox">
                                        <label>
                                            <span class="input-area">
                                                <input type="checkbox" :value="district.id" v-model="selectedDistricts"
                                                    @change="updateBlocks" class="input-with-feedback"
                                                    :disabled="read_only">
                                            </span>
                                            <span class="disp-area" style="display: none;">
                                                <input type="checkbox" disabled class="disabled-deselected">
                                            </span>
                                            <span class="label-area">{{ district.name }}</span>
                                            <span class="ml-1 help"></span>
                                        </label>
                                        <p class="help-box small text-extra-muted"></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 3">
                        <h4>Available Blocks</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :checked="allBlocksSelected"
                                    @change="toggleAllBlocks" :disabled="read_only">
                                <label class="form-check-label">Select All Blocks</label>
                            </div>
                        </div>
                        <div v-for="districtId in selectedDistricts" :key="districtId"
                            class="district-block-group mb-4">
                            <div class="district-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(getDistrictState(districtId)) }}</span>
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getDistrictName(districtId) }}</span>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox"
                                        :checked="isAllBlocksSelectedForDistrict(districtId)"
                                        @change="toggleAllBlocksForDistrict(districtId)" :disabled="read_only">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="block in getBlocksForDistrict(districtId)"
                                    :key="block.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="block.id"
                                            v-model="selectedBlocks" @change="updateGramPanchayats"
                                            :disabled="read_only">
                                        <label class="form-check-label">{{ block.name }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 4">
                        <h4>Available Gram Panchayats</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :checked="allGramPanchayatsSelected"
                                    @change="toggleAllGramPanchayats" :disabled="read_only">
                                <label class="form-check-label">Select All Gram Panchayats</label>
                            </div>
                        </div>
                        <div v-for="blockId in selectedBlocks" :key="blockId" class="block-gp-group mb-4">
                            <div class="block-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(getBlockState(blockId)) }}</span>
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getDistrictName(getBlockDistrict(blockId)) }}</span>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox"
                                        :checked="isAllGramPanchayatsSelectedForBlock(blockId)"
                                        @change="toggleAllGramPanchayatsForBlock(blockId)" :disabled="read_only">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="gp in getGramPanchayatsForBlock(blockId)"
                                    :key="gp.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="gp.id"
                                            v-model="selectedGramPanchayats" @change="updateVillages"
                                            :disabled="read_only">
                                        <label class="form-check-label">{{ gp.name }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 5">
                        <h4>Available Villages</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :checked="allVillagesSelected"
                                    @change="toggleAllVillages" :disabled="read_only">
                                <label class="form-check-label">Select All Villages</label>
                            </div>
                        </div>
                        <div v-for="gpId in selectedGramPanchayats" :key="gpId" class="gp-village-group mb-4">
                            <div class="gp-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(getGPState(gpId)) }}</span>
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getDistrictName(getGPDistrict(gpId)) }}</span>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox"
                                        :checked="isAllVillagesSelectedForGP(gpId)"
                                        @change="toggleAllVillagesForGP(gpId)" :disabled="read_only">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="village in getVillagesForGP(gpId)" :key="village.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="village.id"
                                            v-model="selectedVillages" :disabled="read_only">
                                        <label class="form-check-label">{{ village.name }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="button-group">
                        <button class="btn btn-default" @click="goBack" v-if="currentStep > 1"
                            :disabled="isLoading">Back</button>
                        <button class="btn btn-primary" @click="saveSelection" v-if="isAtLowestHierarchy && !read_only"
                            :disabled="isLoading">Save</button>
                        <button class="btn btn-primary" @click="goNext" v-if="currentStep < totalSteps"
                            :disabled="isLoading">Next</button>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="geography-overview">
                    <div class="geography-header">
                        <h5>Geography Overview</h5>
                    </div>
                    <div class="geography-tree">
                        <div v-for="stateId in selectedStates" :key="stateId" class="tree-item state-item">
                            <div class="tree-content"
                                @click="!read_only && lowest_hierarchy !== 'State' && toggleStateExpansion(stateId)">
                                <span class="tree-icon toggle-icon" v-if="lowest_hierarchy !== 'State'"
                                    :class="{ 'expanded': isStateExpanded(stateId) }">
                                    {{ isStateExpanded(stateId) ? '▼' : '▶' }}
                                </span>
                                <span class="tree-icon">📌</span>
                                <span class="tree-label">{{ getStateName(stateId) }}</span>
                                <span class="tree-count" v-if="lowest_hierarchy !== 'State'">
                                    ({{ getSelectedDistrictsForState(stateId).length }})
                                </span>
                            </div>
                            <div class="tree-children"
                                v-show="isStateExpanded(stateId) && lowest_hierarchy !== 'State'">
                                <div v-for="district in getDistrictsForState(stateId)" :key="district.id"
                                    class="tree-item district-item" v-show="selectedDistricts.includes(district.id)">
                                    <div class="tree-content"
                                        @click="!read_only && lowest_hierarchy !== 'District' && toggleDistrictExpansion(district.id)">
                                        <span class="tree-icon toggle-icon" v-if="lowest_hierarchy !== 'District'"
                                            :class="{ 'expanded': isDistrictExpanded(district.id) }">
                                            {{ isDistrictExpanded(district.id) ? '▼' : '▶' }}
                                        </span>
                                        <span class="tree-icon">📍</span>
                                        <span class="tree-label">{{ district.name }}</span>
                                        <span class="tree-count" v-if="lowest_hierarchy !== 'District'">
                                            ({{ getSelectedBlocksForDistrict(district.id).length }})
                                        </span>
                                    </div>
                                    <div class="tree-children"
                                        v-show="isDistrictExpanded(district.id) && lowest_hierarchy !== 'District'">
                                        <div v-for="block in getBlocksForDistrict(district.id)" :key="block.id"
                                            class="tree-item block-item" v-show="selectedBlocks.includes(block.id)">
                                            <div class="tree-content"
                                                @click="!read_only && lowest_hierarchy !== 'Block' && toggleBlockExpansion(block.id)">
                                                <span class="tree-icon toggle-icon" v-if="lowest_hierarchy !== 'Block'"
                                                    :class="{ 'expanded': isBlockExpanded(block.id) }">
                                                    {{ isBlockExpanded(block.id) ? '▼' : '▶' }}
                                                </span>
                                                <span class="tree-icon">🏘️</span>
                                                <span class="tree-label">{{ block.name }}</span>
                                                <span class="tree-count" v-if="lowest_hierarchy !== 'Block'">
                                                    ({{ getSelectedGramPanchayatsForBlock(block.id).length }})
                                                </span>
                                            </div>
                                            <div class="tree-children"
                                                v-show="isBlockExpanded(block.id) && lowest_hierarchy !== 'Block'">
                                                <div v-for="gp in getGramPanchayatsForBlock(block.id)" :key="gp.id"
                                                    class="tree-item gp-item"
                                                    v-show="selectedGramPanchayats.includes(gp.id)">
                                                    <div class="tree-content"
                                                        @click="!read_only && lowest_hierarchy !== 'Gram Panchayat' && toggleGPExpansion(gp.id)">
                                                        <span class="tree-icon toggle-icon"
                                                            v-if="lowest_hierarchy !== 'Gram Panchayat'"
                                                            :class="{ 'expanded': isGPExpanded(gp.id) }">
                                                            {{ isGPExpanded(gp.id) ? '▼' : '▶' }}
                                                        </span>
                                                        <span class="tree-icon">🏛️</span>
                                                        <span class="tree-label">{{ gp.name }}</span>
                                                        <span class="tree-count"
                                                            v-if="lowest_hierarchy !== 'Gram Panchayat'">
                                                            ({{ getSelectedVillagesForGP(gp.id).length }})
                                                        </span>
                                                    </div>
                                                    <div class="tree-children"
                                                        v-show="isGPExpanded(gp.id) && lowest_hierarchy !== 'Gram Panchayat'">
                                                        <div v-for="village in getVillagesForGP(gp.id)"
                                                            :key="village.id" class="tree-item village-item"
                                                            v-show="selectedVillages.includes(village.id)">
                                                            <div class="tree-content">
                                                                <span class="tree-icon">🏡</span>
                                                                <span class="tree-label">{{ village.name }}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GeographyDetails',
    props: {
        hierarchy_level_field: {
            type: String,
            required: true
        },
        geography_details_field: {
            type: String,
            required: true
        },
        frm: {
            type: Object,
            required: true
        },
        geography_title: {
            type: String,
            required: false
        },
        read_only: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            currentStep: 1,
            states: [],
            districts: {},
            blocks: {},
            gramPanchayats: {},
            villages: {},
            selectedStates: [],
            selectedDistricts: [],
            selectedBlocks: [],
            selectedGramPanchayats: [],
            selectedVillages: [],
            availableDistricts: [],
            availableBlocks: [],
            availableGramPanchayats: [],
            availableVillages: [],
            isLoading: false,
            expandedStateId: null,
            current_docname: null,
            lowest_hierarchy: 'District',
            isDataLoaded: false,
            expandedStates: new Set(),
            expandedDistricts: new Set(),
            expandedBlocks: new Set(),
            expandedGPs: new Set(),
            doctype: null
        };
    },
    computed: {
        totalSteps() {
            switch (this.lowest_hierarchy) {
                case 'State':
                    return 1;
                case 'District':
                    return 2;
                case 'Block':
                    return 3;
                case 'Gram Panchayat':
                    return 4;
                case 'Village':
                    return 5;
                default:
                    return 2;
            }
        },
        themeColors() {
            return {
                primary: frappe.boot.my_theme?.button_background_color || '#171717',
                primaryLight: this.getLightColor(frappe.boot.my_theme?.button_background_color || '#171717')
            };
        },
        isAtLowestHierarchy() {
            switch (this.lowest_hierarchy) {
                case 'State':
                    return this.currentStep === 1;
                case 'District':
                    return this.currentStep === 2;
                case 'Block':
                    return this.currentStep === 3;
                case 'Gram Panchayat':
                    return this.currentStep === 4;
                case 'Village':
                    return this.currentStep === 5;
                default:
                    return false;
            }
        },
        allStatesSelected() {
            return this.states.length > 0 && this.selectedStates.length === this.states.length;
        },
        allDistrictsSelected() {
            return this.availableDistricts.length > 0 &&
                this.selectedDistricts.length === this.availableDistricts.length;
        },
        allBlocksSelected() {
            return this.availableBlocks.length > 0 &&
                this.selectedBlocks.length === this.availableBlocks.length;
        },
        allGramPanchayatsSelected() {
            return this.availableGramPanchayats.length > 0 &&
                this.selectedGramPanchayats.length === this.availableGramPanchayats.length;
        },
        allVillagesSelected() {
            return this.availableVillages.length > 0 &&
                this.selectedVillages.length === this.availableVillages.length;
        },
    },
    async created() {
        // Get doctype from frm
        this.doctype = this.frm.doctype;

        if (this.isDataLoaded) return;

        const route = frappe.get_route();
        if (route[1] === this.doctype && route[2]) {
            this.current_docname = route[2];
            await this.loadExistingData();
        } else {
            await this.loadDefaultLowestHierarchy();
        }
        await this.loadStates();
        // Expand the first state by default if available
        if (this.states.length > 0) {
            this.expandedStates.add(this.states[0].id);
        }
        this.isDataLoaded = true;
        // Expand tree based on initial step
        this.expandTreeBasedOnStep();
    },
    watch: {
        '$route': {
            handler: async function (to, from) {
                const route = frappe.get_route();
                if (route[1] === this.doctype && route[2] && route[2] !== this.current_docname) {
                    this.resetData();
                    this.current_docname = route[2];
                    await this.loadExistingData();
                }
            },
            immediate: true
        }
    },
    methods: {
        async loadDefaultLowestHierarchy() {
            try {
                const response = await frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: this.doctype,
                        name: this.doctype
                    },
                    callback: (r) => {
                        if (r.message && r.message[this.hierarchy_level_field]) {
                            this.lowest_hierarchy = r.message[this.hierarchy_level_field];
                        }
                    }
                });
            } catch (error) {
                console.error('Error loading default lowest hierarchy:', error);
            }
        },
        async loadExistingData() {
            if (!this.current_docname || this.isLoading) return;

            await this.withLoading(async () => {
                try {
                    const doc = await frappe.get_doc(this.doctype, this.current_docname);
                    if (doc) {
                        this.resetData();

                        if (doc[this.hierarchy_level_field]) {
                            this.lowest_hierarchy = doc[this.hierarchy_level_field];
                        }

                        if (doc[this.geography_details_field]) {
                            const stateSet = new Set();
                            const districtSet = new Set();
                            const blockSet = new Set();
                            const gpSet = new Set();
                            const villageSet = new Set();

                            doc[this.geography_details_field].forEach(detail => {
                                if (detail.state) stateSet.add(detail.state);
                                if (detail.district) districtSet.add(detail.district);
                                if (detail.block) blockSet.add(detail.block);
                                if (detail.gram_panchayat) gpSet.add(detail.gram_panchayat);
                                if (detail.village) villageSet.add(detail.village);
                            });

                            this.selectedStates = Array.from(stateSet);
                            this.selectedDistricts = Array.from(districtSet);
                            this.selectedBlocks = Array.from(blockSet);
                            this.selectedGramPanchayats = Array.from(gpSet);
                            this.selectedVillages = Array.from(villageSet);

                            await this.updateAvailableItems();
                            // Expand tree based on current step after loading data
                            this.expandTreeBasedOnStep();
                        }
                    }
                } catch (error) {
                    console.error('Error loading existing data:', error);
                    frappe.show_alert({
                        message: __('Error loading existing data'),
                        indicator: 'red'
                    });
                }
            });
        },
        async loadStates() {
            await this.withLoading(async () => {
                const response = await frappe.call({
                    method: 'sva_frappe.api.get_states',
                    callback: (r) => {
                        if (r.message) {
                            this.states = r.message.map(state => ({
                                id: state.name,
                                name: state.state_name,
                                code: state.state_code
                            }));
                            if (this.states.length > 0) {
                                this.expandedStateId = this.states[0].id;
                            }
                        }
                    }
                });
            });
        },
        async updateDistricts() {
            if (this.selectedStates.length === 0) {
                this.availableDistricts = [];
                this.selectedDistricts = [];
                this.updateBlocks();
                return;
            }

            await this.withLoading(async () => {
                try {
                    const response = await frappe.call({
                        method: 'sva_frappe.api.get_districts',
                        args: {
                            state: this.selectedStates
                        },
                        callback: (r) => {
                            if (r.message) {
                                this.districts = {};
                                this.availableDistricts = r.message.map(district => ({
                                    id: district.name,
                                    name: district.district_name,
                                    code: district.district_code,
                                    state: district.state
                                }));

                                this.availableDistricts.forEach(district => {
                                    if (!this.districts[district.state]) {
                                        this.districts[district.state] = [];
                                    }
                                    this.districts[district.state].push(district);
                                });

                                this.selectedDistricts = this.selectedDistricts.filter(districtId => {
                                    const district = this.availableDistricts.find(d => d.id === districtId);
                                    return district && this.selectedStates.includes(district.state);
                                });
                            }
                        }
                    });
                } catch (error) {
                    console.error('Error fetching districts:', error);
                }
            });

            this.updateBlocks();
        },
        async updateBlocks() {
            if (this.selectedDistricts.length === 0) {
                this.availableBlocks = [];
                this.selectedBlocks = [];
                this.updateGramPanchayats();
                return;
            }

            await this.withLoading(async () => {
                const response = await frappe.call({
                    method: 'sva_frappe.api.get_blocks',
                    args: {
                        district: this.selectedDistricts
                    },
                    callback: (r) => {
                        if (r.message) {
                            this.blocks = {};
                            this.availableBlocks = r.message.map(block => ({
                                id: block.name,
                                name: block.block_name,
                                code: block.block_code,
                                district: block.district,
                                state: block.state
                            }));

                            this.availableBlocks.forEach(block => {
                                if (!this.blocks[block.district]) {
                                    this.blocks[block.district] = [];
                                }
                                this.blocks[block.district].push(block);
                            });

                            this.selectedBlocks = this.selectedBlocks.filter(blockId => {
                                const block = this.availableBlocks.find(b => b.id === blockId);
                                return block && this.selectedDistricts.includes(block.district);
                            });
                        }
                    }
                });
            });

            this.updateGramPanchayats();
        },
        async updateGramPanchayats() {
            if (this.selectedBlocks.length === 0) {
                this.availableGramPanchayats = [];
                this.selectedGramPanchayats = [];
                this.updateVillages();
                return;
            }

            await this.withLoading(async () => {
                const response = await frappe.call({
                    method: 'sva_frappe.api.get_gram_panchayats',
                    args: {
                        block: this.selectedBlocks
                    },
                    callback: (r) => {
                        if (r.message) {
                            this.gramPanchayats = {};
                            this.availableGramPanchayats = r.message.map(gp => ({
                                id: gp.name,
                                name: gp.gram_pachayat_name,
                                code: gp.gram_panchayat_code,
                                block: gp.block,
                                district: gp.district,
                                state: gp.state
                            }));

                            this.availableGramPanchayats.forEach(gp => {
                                if (!this.gramPanchayats[gp.block]) {
                                    this.gramPanchayats[gp.block] = [];
                                }
                                this.gramPanchayats[gp.block].push(gp);
                            });

                            this.selectedGramPanchayats = this.selectedGramPanchayats.filter(gpId => {
                                const gp = this.availableGramPanchayats.find(g => g.id === gpId);
                                return gp && this.selectedBlocks.includes(gp.block);
                            });
                        }
                    }
                });
            });

            this.updateVillages();
        },
        async updateVillages() {
            if (this.selectedGramPanchayats.length === 0) {
                this.availableVillages = [];
                this.selectedVillages = [];
                return;
            }

            await this.withLoading(async () => {
                const response = await frappe.call({
                    method: 'sva_frappe.api.get_villages',
                    args: {
                        gram_panchayat: this.selectedGramPanchayats
                    },
                    callback: (r) => {
                        if (r.message) {
                            this.villages = {};
                            this.availableVillages = r.message.map(village => ({
                                id: village.name,
                                name: village.village_name,
                                code: village.village_code,
                                gram_panchayat: village.gram_panchayat,
                                block: village.block,
                                district: village.district,
                                state: village.state
                            }));

                            this.availableVillages.forEach(village => {
                                if (!this.villages[village.gram_panchayat]) {
                                    this.villages[village.gram_panchayat] = [];
                                }
                                this.villages[village.gram_panchayat].push(village);
                            });

                            this.selectedVillages = this.selectedVillages.filter(villageId => {
                                const village = this.availableVillages.find(v => v.id === villageId);
                                return village && this.selectedGramPanchayats.includes(village.gram_panchayat);
                            });
                        }
                    }
                });
            });
        },
        expandTreeBasedOnStep() {
            // Clear all expansions first
            this.expandedStates.clear();
            this.expandedDistricts.clear();
            this.expandedBlocks.clear();
            this.expandedGPs.clear();

            // Expand based on current step
            switch (this.currentStep) {
                case 1: // States
                    // Expand all states
                    this.selectedStates.forEach(stateId => {
                        this.expandedStates.add(stateId);
                    });
                    break;
                case 2: // Districts
                    // Expand states and their districts
                    this.selectedStates.forEach(stateId => {
                        this.expandedStates.add(stateId);
                        this.getSelectedDistrictsForState(stateId).forEach(district => {
                            this.expandedDistricts.add(district.id);
                        });
                    });
                    break;
                case 3: // Blocks
                    // Expand states, districts and their blocks
                    this.selectedStates.forEach(stateId => {
                        this.expandedStates.add(stateId);
                        this.getSelectedDistrictsForState(stateId).forEach(district => {
                            this.expandedDistricts.add(district.id);
                            this.getSelectedBlocksForDistrict(district.id).forEach(block => {
                                this.expandedBlocks.add(block.id);
                            });
                        });
                    });
                    break;
                case 4: // Gram Panchayats
                    // Expand states, districts, blocks and their GPs
                    this.selectedStates.forEach(stateId => {
                        this.expandedStates.add(stateId);
                        this.getSelectedDistrictsForState(stateId).forEach(district => {
                            this.expandedDistricts.add(district.id);
                            this.getSelectedBlocksForDistrict(district.id).forEach(block => {
                                this.expandedBlocks.add(block.id);
                                this.getSelectedGramPanchayatsForBlock(block.id).forEach(gp => {
                                    this.expandedGPs.add(gp.id);
                                });
                            });
                        });
                    });
                    break;
                case 5: // Villages
                    // Expand everything
                    this.selectedStates.forEach(stateId => {
                        this.expandedStates.add(stateId);
                        this.getSelectedDistrictsForState(stateId).forEach(district => {
                            this.expandedDistricts.add(district.id);
                            this.getSelectedBlocksForDistrict(district.id).forEach(block => {
                                this.expandedBlocks.add(block.id);
                                this.getSelectedGramPanchayatsForBlock(block.id).forEach(gp => {
                                    this.expandedGPs.add(gp.id);
                                });
                            });
                        });
                    });
                    break;
            }
        },
        goNext() {
            if (this.currentStep >= this.totalSteps) return;

            const canProceed = (() => {
                switch (this.currentStep) {
                    case 1:
                        return this.selectedStates.length > 0;
                    case 2:
                        return this.selectedDistricts.length > 0;
                    case 3:
                        return this.selectedBlocks.length > 0;
                    case 4:
                        return this.selectedGramPanchayats.length > 0;
                    default:
                        return true;
                }
            })();

            if (canProceed) {
                this.currentStep++;
                switch (this.currentStep) {
                    case 2:
                        this.updateBlocks();
                        break;
                    case 3:
                        this.updateGramPanchayats();
                        break;
                    case 4:
                        this.updateVillages();
                        break;
                }
                // Expand tree based on new step
                this.expandTreeBasedOnStep();
            }
        },
        goBack() {
            if (this.currentStep > 1) {
                this.currentStep--;
                // Expand tree based on new step
                this.expandTreeBasedOnStep();
            }
        },
        async saveSelection() {
            const selectionMap = new Map();

            this.selectedStates.forEach(stateId => {
                const state = this.states.find(s => s.id === stateId);
                if (state) {
                    const key = `${state.id}`;
                    selectionMap.set(key, {
                        state: {
                            id: state.id,
                            name: state.name,
                            code: state.code
                        }
                    });
                }
            });

            this.selectedDistricts.forEach(districtId => {
                const district = this.availableDistricts.find(d => d.id === districtId);
                if (district) {
                    const state = this.states.find(s => s.id === district.state);
                    const key = `${district.state}_${district.id}`;
                    selectionMap.set(key, {
                        state: {
                            id: state.id,
                            name: state.name,
                            code: state.code
                        },
                        district: {
                            id: district.id,
                            name: district.name,
                            code: district.code,
                            state: district.state
                        }
                    });
                }
            });

            this.selectedBlocks.forEach(blockId => {
                const block = this.availableBlocks.find(b => b.id === blockId);
                if (block) {
                    const state = this.states.find(s => s.id === block.state);
                    const district = this.availableDistricts.find(d => d.id === block.district);
                    const key = `${block.state}_${block.district}_${block.id}`;
                    selectionMap.set(key, {
                        state: {
                            id: state.id,
                            name: state.name,
                            code: state.code
                        },
                        district: {
                            id: district.id,
                            name: district.name,
                            code: district.code,
                            state: district.state
                        },
                        block: {
                            id: block.id,
                            name: block.name,
                            code: block.code,
                            district: block.district,
                            state: block.state
                        }
                    });
                }
            });

            this.selectedGramPanchayats.forEach(gpId => {
                const gp = this.availableGramPanchayats.find(g => g.id === gpId);
                if (gp) {
                    const state = this.states.find(s => s.id === gp.state);
                    const district = this.availableDistricts.find(d => d.id === gp.district);
                    const block = this.availableBlocks.find(b => b.id === gp.block);
                    const key = `${gp.state}_${gp.district}_${gp.block}_${gp.id}`;
                    selectionMap.set(key, {
                        state: {
                            id: state.id,
                            name: state.name,
                            code: state.code
                        },
                        district: {
                            id: district.id,
                            name: district.name,
                            code: district.code,
                            state: district.state
                        },
                        block: {
                            id: block.id,
                            name: block.name,
                            code: block.code,
                            district: block.district,
                            state: block.state
                        },
                        gramPanchayat: {
                            id: gp.id,
                            name: gp.name,
                            code: gp.code,
                            block: gp.block,
                            district: gp.district,
                            state: gp.state
                        }
                    });
                }
            });

            this.selectedVillages.forEach(villageId => {
                const village = this.availableVillages.find(v => v.id === villageId);
                if (village) {
                    const state = this.states.find(s => s.id === village.state);
                    const district = this.availableDistricts.find(d => d.id === village.district);
                    const block = this.availableBlocks.find(b => b.id === village.block);
                    const gp = this.availableGramPanchayats.find(g => g.id === village.gram_panchayat);
                    const key = `${village.state}_${village.district}_${village.block}_${village.gram_panchayat}_${village.id}`;
                    selectionMap.set(key, {
                        state: {
                            id: state.id,
                            name: state.name,
                            code: state.code
                        },
                        district: {
                            id: district.id,
                            name: district.name,
                            code: district.code,
                            state: district.state
                        },
                        block: {
                            id: block.id,
                            name: block.name,
                            code: block.code,
                            district: block.district,
                            state: block.state
                        },
                        gramPanchayat: {
                            id: gp.id,
                            name: gp.name,
                            code: gp.code,
                            block: gp.block,
                            district: gp.district,
                            state: gp.state
                        },
                        village: {
                            id: village.id,
                            name: village.name,
                            code: village.code,
                            gram_panchayat: village.gram_panchayat,
                            block: village.block,
                            district: village.district,
                            state: village.state
                        }
                    });
                }
            });

            let selection = Array.from(selectionMap.values());

            switch (this.lowest_hierarchy) {
                case 'State':
                    selection = selection.filter(item => item.state && !item.district);
                    break;
                case 'District':
                    selection = selection.filter(item => item.state && item.district && !item.block);
                    break;
                case 'Block':
                    selection = selection.filter(item => item.state && item.district && item.block && !item.gramPanchayat);
                    break;
                case 'Gram Panchayat':
                    selection = selection.filter(item => item.state && item.district && item.block && item.gramPanchayat && !item.village);
                    break;
                case 'Village':
                    selection = selection.filter(item => item.state && item.district && item.block && item.gramPanchayat && item.village);
                    break;
            }

            try {
                const response = await frappe.call({
                    method: 'sva_frappe.api.save_geography_details',
                    args: {
                        selection_data: JSON.stringify(selection),
                        docname: this.current_docname,
                        lowest_hierarchy: this.lowest_hierarchy,
                        doctype: this.doctype,
                        hierarchy_level_field: this.hierarchy_level_field,
                        geography_details_field: this.geography_details_field
                    },
                    callback: (r) => {
                        if (r.message && r.message.status === 'success') {
                            if (!this.current_docname && r.message.docname) {
                                this.current_docname = r.message.docname;
                            }

                            frappe.show_alert({
                                message: r.message.message,
                                indicator: 'green'
                            });

                            if (!this.current_docname && r.message.docname) {
                                frappe.set_route('Form', this.doctype, r.message.docname);
                            }
                        } else {
                            frappe.show_alert({
                                message: r.message?.message || __('Error saving geography details'),
                                indicator: 'red'
                            });
                        }
                    }
                });
            } catch (error) {
                console.error('Error saving geography details:', error);
                frappe.show_alert({
                    message: __('Error saving geography details'),
                    indicator: 'red'
                });
            }

            return selection;
        },
        getStateName(stateId) {
            const state = this.states.find(s => s.id === stateId);
            return state ? state.name : '';
        },
        getDistrictsForState(stateId) {
            return this.districts[stateId] || [];
        },
        isAllDistrictsSelectedForState(stateId) {
            const stateDistricts = this.getDistrictsForState(stateId);
            if (!stateDistricts.length) return false;
            return stateDistricts.every(district =>
                this.selectedDistricts.includes(district.id)
            );
        },
        toggleAllDistrictsForState(stateId) {
            const stateDistricts = this.getDistrictsForState(stateId);
            const allSelected = this.isAllDistrictsSelectedForState(stateId);

            if (allSelected) {
                // If all districts for this state are selected, unselect them and their children
                const districtIds = stateDistricts.map(d => d.id);
                this.selectedDistricts = this.selectedDistricts.filter(id => !districtIds.includes(id));

                // Also remove any blocks, GPs, and villages that belong to these districts
                const blocksToRemove = this.availableBlocks
                    .filter(block => districtIds.includes(block.district))
                    .map(block => block.id);
                this.selectedBlocks = this.selectedBlocks.filter(id => !blocksToRemove.includes(id));

                const gpsToRemove = this.availableGramPanchayats
                    .filter(gp => blocksToRemove.includes(gp.block))
                    .map(gp => gp.id);
                this.selectedGramPanchayats = this.selectedGramPanchayats.filter(id => !gpsToRemove.includes(id));

                const villagesToRemove = this.availableVillages
                    .filter(village => gpsToRemove.includes(village.gram_panchayat))
                    .map(village => village.id);
                this.selectedVillages = this.selectedVillages.filter(id => !villagesToRemove.includes(id));
            } else {
                // If not all districts are selected, select all districts for this state
                const districtIds = stateDistricts.map(d => d.id);
                this.selectedDistricts = [...new Set([...this.selectedDistricts, ...districtIds])];
            }

            this.updateBlocks();
        },
        getDistrictName(districtId) {
            const district = this.availableDistricts.find(d => d.id === districtId);
            return district ? district.name : '';
        },
        getBlocksForDistrict(districtId) {
            return this.blocks[districtId] || [];
        },
        isAllBlocksSelected() {
            return this.availableBlocks.length > 0 &&
                this.availableBlocks.every(block =>
                    this.selectedBlocks.includes(block.id)
                );
        },
        isAllBlocksSelectedForDistrict(districtId) {
            const districtBlocks = this.getBlocksForDistrict(districtId);
            return districtBlocks.length > 0 &&
                districtBlocks.every(block =>
                    this.selectedBlocks.includes(block.id)
                );
        },
        toggleAllBlocksForDistrict(districtId) {
            const districtBlocks = this.getBlocksForDistrict(districtId);
            const allSelected = this.isAllBlocksSelectedForDistrict(districtId);

            if (allSelected) {
                // If all blocks for this district are selected, unselect them and their children
                const blockIds = districtBlocks.map(b => b.id);
                this.selectedBlocks = this.selectedBlocks.filter(id => !blockIds.includes(id));

                // Also remove any GPs and villages that belong to these blocks
                const gpsToRemove = this.availableGramPanchayats
                    .filter(gp => blockIds.includes(gp.block))
                    .map(gp => gp.id);
                this.selectedGramPanchayats = this.selectedGramPanchayats.filter(id => !gpsToRemove.includes(id));

                const villagesToRemove = this.availableVillages
                    .filter(village => gpsToRemove.includes(village.gram_panchayat))
                    .map(village => village.id);
                this.selectedVillages = this.selectedVillages.filter(id => !villagesToRemove.includes(id));
            } else {
                // If not all blocks are selected, select all blocks for this district
                const blockIds = districtBlocks.map(b => b.id);
                this.selectedBlocks = [...new Set([...this.selectedBlocks, ...blockIds])];
            }

            this.updateGramPanchayats();
        },
        getBlockName(blockId) {
            const block = this.availableBlocks.find(b => b.id === blockId);
            return block ? block.name : '';
        },
        getGramPanchayatsForBlock(blockId) {
            return this.gramPanchayats[blockId] || [];
        },
        isAllGramPanchayatsSelected() {
            return this.availableGramPanchayats.length > 0 &&
                this.availableGramPanchayats.every(gp =>
                    this.selectedGramPanchayats.includes(gp.id)
                );
        },
        isAllGramPanchayatsSelectedForBlock(blockId) {
            const blockGPs = this.getGramPanchayatsForBlock(blockId);
            return blockGPs.length > 0 &&
                blockGPs.every(gp =>
                    this.selectedGramPanchayats.includes(gp.id)
                );
        },
        toggleAllGramPanchayatsForBlock(blockId) {
            const blockGPs = this.getGramPanchayatsForBlock(blockId);
            const allSelected = this.isAllGramPanchayatsSelectedForBlock(blockId);

            if (allSelected) {
                // If all GPs for this block are selected, unselect them and their children
                const gpIds = blockGPs.map(gp => gp.id);
                this.selectedGramPanchayats = this.selectedGramPanchayats.filter(id => !gpIds.includes(id));

                // Also remove any villages that belong to these GPs
                const villagesToRemove = this.availableVillages
                    .filter(village => gpIds.includes(village.gram_panchayat))
                    .map(village => village.id);
                this.selectedVillages = this.selectedVillages.filter(id => !villagesToRemove.includes(id));
            } else {
                // If not all GPs are selected, select all GPs for this block
                const gpIds = blockGPs.map(gp => gp.id);
                this.selectedGramPanchayats = [...new Set([...this.selectedGramPanchayats, ...gpIds])];
            }

            this.updateVillages();
        },
        getGramPanchayatName(gpId) {
            const gp = this.availableGramPanchayats.find(g => g.id === gpId);
            return gp ? gp.name : '';
        },
        getVillagesForGP(gpId) {
            return this.villages[gpId] || [];
        },
        isAllVillagesSelected() {
            return this.availableVillages.length > 0 &&
                this.availableVillages.every(village =>
                    this.selectedVillages.includes(village.id)
                );
        },
        isAllVillagesSelectedForGP(gpId) {
            const gpVillages = this.getVillagesForGP(gpId);
            return gpVillages.length > 0 &&
                gpVillages.every(village =>
                    this.selectedVillages.includes(village.id)
                );
        },
        toggleAllVillagesForGP(gpId) {
            const gpVillages = this.getVillagesForGP(gpId);
            const allSelected = this.isAllVillagesSelectedForGP(gpId);

            if (allSelected) {
                // If all villages for this GP are selected, unselect them
                const villageIds = gpVillages.map(v => v.id);
                this.selectedVillages = this.selectedVillages.filter(id => !villageIds.includes(id));
            } else {
                // If not all villages are selected, select all villages for this GP
                const villageIds = gpVillages.map(v => v.id);
                this.selectedVillages = [...new Set([...this.selectedVillages, ...villageIds])];
            }
        },
        updateAvailableItems() {
            this.updateDistricts();
            if (this.lowest_hierarchy !== 'State') {
                this.updateBlocks();
                if (this.lowest_hierarchy !== 'District') {
                    this.updateGramPanchayats();
                    if (this.lowest_hierarchy !== 'Block') {
                        this.updateVillages();
                    }
                }
            }
        },
        withLoading(callback) {
            this.isLoading = true;
            try {
                return callback();
            } finally {
                this.isLoading = false;
            }
        },
        getDistrictState(districtId) {
            const district = this.availableDistricts.find(d => d.id === districtId);
            return district ? district.state : '';
        },
        getBlockState(blockId) {
            const block = this.availableBlocks.find(b => b.id === blockId);
            return block ? block.state : '';
        },
        getBlockDistrict(blockId) {
            const block = this.availableBlocks.find(b => b.id === blockId);
            return block ? block.district : '';
        },
        getGPState(gpId) {
            const gp = this.availableGramPanchayats.find(g => g.id === gpId);
            return gp ? gp.state : '';
        },
        getGPDistrict(gpId) {
            const gp = this.availableGramPanchayats.find(g => g.id === gpId);
            return gp ? gp.district : '';
        },
        getGPBlock(gpId) {
            const gp = this.availableGramPanchayats.find(g => g.id === gpId);
            return gp ? gp.block : '';
        },
        toggleStateExpansion(stateId) {
            if (this.expandedStates.has(stateId)) {
                this.expandedStates.delete(stateId);
            } else {
                this.expandedStates.clear();
                this.expandedStates.add(stateId);
                this.expandedDistricts.clear();
                this.expandedBlocks.clear();
                this.expandedGPs.clear();
            }
        },
        toggleDistrictExpansion(districtId) {
            if (this.expandedDistricts.has(districtId)) {
                this.expandedDistricts.delete(districtId);
            } else {
                this.expandedDistricts.clear();
                this.expandedDistricts.add(districtId);
                this.expandedBlocks.clear();
                this.expandedGPs.clear();
            }
        },
        toggleBlockExpansion(blockId) {
            if (this.expandedBlocks.has(blockId)) {
                this.expandedBlocks.delete(blockId);
            } else {
                this.expandedBlocks.clear();
                this.expandedBlocks.add(blockId);
                this.expandedGPs.clear();
            }
        },
        toggleGPExpansion(gpId) {
            if (this.expandedGPs.has(gpId)) {
                this.expandedGPs.delete(gpId);
            } else {
                this.expandedGPs.clear();
                this.expandedGPs.add(gpId);
            }
        },
        isStateExpanded(stateId) {
            return this.expandedStates.has(stateId);
        },
        isDistrictExpanded(districtId) {
            return this.expandedDistricts.has(districtId);
        },
        isBlockExpanded(blockId) {
            return this.expandedBlocks.has(blockId);
        },
        isGPExpanded(gpId) {
            return this.expandedGPs.has(gpId);
        },
        resetData() {
            this.states = [];
            this.districts = {};
            this.blocks = {};
            this.gramPanchayats = {};
            this.villages = {};
            this.selectedStates = [];
            this.selectedDistricts = [];
            this.selectedBlocks = [];
            this.selectedGramPanchayats = [];
            this.selectedVillages = [];
            this.availableDistricts = [];
            this.availableBlocks = [];
            this.availableGramPanchayats = [];
            this.availableVillages = [];
            this.isDataLoaded = false;
            this.expandedStates.clear();
            this.expandedDistricts.clear();
            this.expandedBlocks.clear();
            this.expandedGPs.clear();
        },
        getSelectedDistrictsForState(stateId) {
            return this.getDistrictsForState(stateId).filter(district =>
                this.selectedDistricts.includes(district.id)
            );
        },
        getSelectedBlocksForDistrict(districtId) {
            return this.getBlocksForDistrict(districtId).filter(block =>
                this.selectedBlocks.includes(block.id)
            );
        },
        getSelectedGramPanchayatsForBlock(blockId) {
            return this.getGramPanchayatsForBlock(blockId).filter(gp =>
                this.selectedGramPanchayats.includes(gp.id)
            );
        },
        getSelectedVillagesForGP(gpId) {
            return this.getVillagesForGP(gpId).filter(village =>
                this.selectedVillages.includes(village.id)
            );
        },
        toggleAllStates() {
            if (this.allStatesSelected) {
                // If all are selected, unselect all
                this.selectedStates = [];
                this.selectedDistricts = [];
                this.selectedBlocks = [];
                this.selectedGramPanchayats = [];
                this.selectedVillages = [];
            } else {
                // If not all are selected, select all states
                this.selectedStates = this.states.map(state => state.id);
            }
            this.updateDistricts();
        },
        toggleAllDistricts() {
            if (this.allDistrictsSelected) {
                // If all are selected, unselect all districts and their children
                this.selectedDistricts = [];
                this.selectedBlocks = [];
                this.selectedGramPanchayats = [];
                this.selectedVillages = [];
            } else {
                // If not all are selected, select all available districts
                this.selectedDistricts = this.availableDistricts.map(district => district.id);
            }
            this.updateBlocks();
        },
        toggleAllBlocks() {
            if (this.allBlocksSelected) {
                // If all are selected, unselect all blocks and their children
                this.selectedBlocks = [];
                this.selectedGramPanchayats = [];
                this.selectedVillages = [];
            } else {
                // If not all are selected, select all available blocks
                this.selectedBlocks = this.availableBlocks.map(block => block.id);
            }
            this.updateGramPanchayats();
        },
        toggleAllGramPanchayats() {
            if (this.allGramPanchayatsSelected) {
                // If all are selected, unselect all GPs and their children
                this.selectedGramPanchayats = [];
                this.selectedVillages = [];
            } else {
                // If not all are selected, select all available GPs
                this.selectedGramPanchayats = this.availableGramPanchayats.map(gp => gp.id);
            }
            this.updateVillages();
        },
        toggleAllVillages() {
            if (this.allVillagesSelected) {
                // If all are selected, unselect all villages
                this.selectedVillages = [];
            } else {
                // If not all are selected, select all available villages
                this.selectedVillages = this.availableVillages.map(village => village.id);
            }
        },
        getLightColor(color) {
            // Convert hex to RGB
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);

            // Create a lighter version
            const lightR = Math.min(r + 40, 255);
            const lightG = Math.min(g + 40, 255);
            const lightB = Math.min(b + 40, 255);

            return `rgb(${lightR}, ${lightG}, ${lightB})`;
        },
    }
};
</script>

<style scoped>
/* Core Layout */
.container-fluid {
    padding-left: 15px;
    padding-right: 15px;
}

/* Header */
.header {
    font-size: 20px;
    margin-bottom: 20px;
    color: v-bind('themeColors.primary');
    font-weight: 600;
}

/* Main Container */
.main-container {
    border: 1px solid var(--border-color);
    border-radius: 3px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: var(--bg-color);
    transition: opacity 0.3s ease;
}

.main-container h4 {
    font-size: var(--text-md);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
    margin-bottom: 15px;
}

.main-container.loading {
    opacity: 0.7;
    pointer-events: none;
}

/* Button Group */
.button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
    gap: 8px;
}

/* Geography Overview */
.geography-overview {
    border: 1px solid var(--border-color);
    border-radius: 3px;
    padding: 20px;
    background-color: var(--bg-color);
}

.geography-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.geography-header h5 {
    font-size: var(--text-md);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
}

/* Checkbox Styles */
.checkbox-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.checkbox-item {
    min-width: 200px;
    flex: 0 1 auto;
    margin-bottom: 10px;
}

.checkbox,
.form-check {
    display: flex;
    align-items: flex-start;
}

.checkbox label,
.form-check {
    display: flex;
    align-items: flex-start;
    margin: 0;
    cursor: pointer;
}

.checkbox .input-area,
.form-check-input {
    margin-top: 2px;
    /* margin-right: 4px; */
}

.checkbox .label-area,
.form-check-label {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
    line-height: 1.4;
}

.checkbox .help {
    margin-left: 4px;
}

.checkbox .help-box {
    margin-top: 4px;
    margin-bottom: 0;
}

/* Override Bootstrap form-check styles */
.form-check {
    padding-left: 0;
    margin-bottom: 0;
}

.form-check-input {
    margin-left: 0;
    margin-top: 2px;
    /* margin-right: 4px; */
}

.form-check-label {
    margin-bottom: 0;
}

/* Group Headers */
.state-district-group,
.district-block-group,
.block-gp-group,
.gp-village-group {
    border: 1px solid var(--border-color);
    border-radius: 3px;
    padding: 15px;
    margin-bottom: 20px;
}

.state-header,
.district-header,
.block-header,
.gp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 15px;
}

/* Hierarchy Path */
.hierarchy-path {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
    font-size: 0.9rem;
    color: var(--text-muted);
}

.path-item {
    color: v-bind('themeColors.primary');
    font-weight: 500;
}

.path-separator {
    color: var(--text-muted);
    margin: 0 5px;
}

/* Loading Overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.loading-spinner {
    text-align: center;
    background: var(--bg-color);
    padding: 2rem;
    border-radius: 3px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Tree View */
.geography-tree {
    max-height: 600px;
    overflow-y: auto;
    padding-right: 10px;
}

.tree-item {
    margin-bottom: 4px;
}

.tree-content {
    padding: 8px 12px;
    border-radius: 3px;
    display: flex;
    align-items: center;
    background-color: var(--bg-color);
    border: 1px solid var(--border-color);
    cursor: pointer;
    user-select: none;
}

.tree-children {
    margin-left: 20px;
    padding-left: 10px;
    border-left: 2px solid v-bind('themeColors.primary');
    transition: all 0.3s ease;
}

/* Tree Icons */
.tree-icon {
    margin-right: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.toggle-icon {
    color: v-bind('themeColors.primary');
    font-size: 12px;
    width: 16px;
    height: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
}

/* .toggle-icon.expanded {
    transform: rotate(0deg);
}

.toggle-icon:not(.expanded) {
    transform: rotate(-90deg);
} */

/* Tree Labels */
.tree-label {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
}

/* Remove hover effect for labels */
/* .tree-content:hover .tree-label {
    color: v-bind('themeColors.primary');
} */

/* Tree Count */
.tree-count {
    margin-left: auto;
    font-size: var(--text-sm);
    color: v-bind('themeColors.primary');
    opacity: 0.8;
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
}

/* Step Container */
.step-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    position: relative;
    padding: 0;
    width: 100%;
    margin-left: 0;
    margin-right: 0;
}

.step-container::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--border-color);
    transform: translateY(-50%);
    z-index: 0;
}

.step-container::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    height: 1px;
    background: v-bind('themeColors.primary');
    transform: translateY(-50%);
    z-index: 0;
    transition: width 0.3s ease;
    width: calc((100% / (v-bind('totalSteps') - 1)) * (v-bind('currentStep') - 1));
}

.step {
    display: flex;
    flex-direction: row;
    align-items: center;
    position: relative;
    z-index: 1;
    background: var(--bg-color);
    min-width: 80px;
    gap: 6px;
}

.step-number {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: var(--bg-color);
    border: 1.5px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 11px;
    transition: all 0.3s ease;
    flex-shrink: 0;
}

.step>div:last-child {
    font-size: var(--text-md);
    color: var(--text-color);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.step.active .step-number {
    background-color: v-bind('themeColors.primary');
    border-color: v-bind('themeColors.primary');
    color: white;
    box-shadow: 0 0 0 2px v-bind('themeColors.primaryLight');
}

.step.active>div:last-child {
    color: var(--text-color);
    font-weight: 600;
}

.step.completed .step-number {
    background-color: v-bind('themeColors.primary');
    border-color: v-bind('themeColors.primary');
    color: white;
}

.step.completed>div:last-child {
    color: var(--text-color);
}

/* Update other elements that use primary color */
.path-item {
    color: v-bind('themeColors.primary');
    font-weight: 500;
}

.geography-tree::-webkit-scrollbar-thumb {
    background: v-bind('themeColors.primary');
    border-radius: 3px;
}

.geography-tree::-webkit-scrollbar-thumb:hover {
    background: v-bind('themeColors.primaryLight');
}

/* Update button styles */
.btn-primary {
    background-color: v-bind('themeColors.primary');
    border-color: v-bind('themeColors.primary');
}

.btn-primary:hover {
    background-color: v-bind('themeColors.primaryLight');
    border-color: v-bind('themeColors.primaryLight');
}
</style>