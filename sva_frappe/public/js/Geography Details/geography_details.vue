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
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :checked="allStatesSelected"
                                    @change="toggleAllStates">
                                <label class="form-check-label">Select All States</label>
                            </div>
                        </div>
                        <div class="checkbox-container">
                            <div class="checkbox-item" v-for="(state, index) in states" :key="index">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" :value="state.id"
                                        v-model="selectedStates" @change="updateDistricts">
                                    <label class="form-check-label">{{ state.name }}</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 2">
                        <h4>Available Districts</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :checked="allDistrictsSelected"
                                    @change="toggleAllDistricts">
                                <label class="form-check-label">Select All Districts</label>
                            </div>
                        </div>
                        <div v-for="stateId in selectedStates" :key="stateId" class="state-district-group mb-4">
                            <div class="state-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(stateId) }}</span>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox"
                                        :checked="isAllDistrictsSelectedForState(stateId)"
                                        @change="toggleAllDistrictsForState(stateId)">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="district in getDistrictsForState(stateId)"
                                    :key="district.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="district.id"
                                            v-model="selectedDistricts" @change="updateBlocks">
                                        <label class="form-check-label">{{ district.name }}</label>
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
                                    @change="toggleAllBlocks">
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
                                        @change="toggleAllBlocksForDistrict(districtId)">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="block in getBlocksForDistrict(districtId)"
                                    :key="block.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="block.id"
                                            v-model="selectedBlocks" @change="updateGramPanchayats">
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
                                    @change="toggleAllGramPanchayats">
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
                                        @change="toggleAllGramPanchayatsForBlock(blockId)">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="gp in getGramPanchayatsForBlock(blockId)"
                                    :key="gp.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="gp.id"
                                            v-model="selectedGramPanchayats" @change="updateVillages">
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
                                    @change="toggleAllVillages">
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
                                        @change="toggleAllVillagesForGP(gpId)">
                                    <label class="form-check-label">Select All</label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="village in getVillagesForGP(gpId)" :key="village.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :value="village.id"
                                            v-model="selectedVillages">
                                        <label class="form-check-label">{{ village.name }}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="button-group">
                        <button class="btn btn-outline-secondary" @click="goBack" v-if="currentStep > 1"
                            :disabled="isLoading">Back</button>
                        <button class="btn btn-save" @click="saveSelection" v-if="isAtLowestHierarchy"
                            :disabled="isLoading">Save</button>
                        <button class="btn btn-next" @click="goNext" v-if="currentStep < totalSteps"
                            :disabled="isLoading">Next</button>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="geography-overview">
                    <div class="geography-header">
                        <h5>Geography Overview</h5>
                        <div class="view-summary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-diagram-3" viewBox="0 0 16 16">
                                <path fill-rule="evenodd"
                                    d="M6 3.5A1.5 1.5 0 0 1 7.5 2h1A1.5 1.5 0 0 1 10 3.5v1A1.5 1.5 0 0 1 8.5 6v1H14a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0V8h-5v.5a.5.5 0 0 1-1 0V8h-5v.5a.5.5 0 0 1-1 0v-1A.5.5 0 0 1 2 7h5.5V6A1.5 1.5 0 0 1 6 4.5v-1zM8.5 5a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1zM0 11.5A1.5 1.5 0 0 1 1.5 10h1A1.5 1.5 0 0 1 4 11.5v1A1.5 1.5 0 0 1 2.5 14h-1A1.5 1.5 0 0 1 0 12.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zm4.5.5A1.5 1.5 0 0 1 7.5 10h1a1.5 1.5 0 0 1 1.5 1.5v1A1.5 1.5 0 0 1 8.5 14h-1A1.5 1.5 0 0 1 6 12.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zm4.5.5a1.5 1.5 0 0 1 1.5-1.5h1a1.5 1.5 0 0 1 1.5 1.5v1a1.5 1.5 0 0 1-1.5 1.5h-1a1.5 1.5 0 0 1-1.5-1.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1z" />
                            </svg>
                            Hierarchy View
                        </div>
                    </div>
                    <div class="geography-tree">
                        <div v-for="stateId in selectedStates" :key="stateId" class="tree-item state-item">
                            <div class="tree-content"
                                @click="lowest_hierarchy !== 'State' && toggleStateExpansion(stateId)">
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
                                        @click="lowest_hierarchy !== 'District' && toggleDistrictExpansion(district.id)">
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
                                                @click="lowest_hierarchy !== 'Block' && toggleBlockExpansion(block.id)">
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
                                                        @click="lowest_hierarchy !== 'Gram Panchayat' && toggleGPExpansion(gp.id)">
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
    }
};
</script>

<style scoped>
/* Direct color values for better compatibility */
.primary-color {
    color: #8C1D40 !important;
}

.primary-bg {
    background-color: #8C1D40 !important;
}

.primary-border {
    border-color: #8C1D40 !important;
}

/* Form Controls */
.form-control {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 0.5rem;
    width: 100%;
    color: #495057;
}

.form-control:focus {
    border-color: #8C1D40 !important;
    box-shadow: 0 0 0 0.2rem rgba(140, 29, 64, 0.15) !important;
}

/* Form Labels */
.form-group label,
.form-check-label {
    color: #8C1D40 !important;
    font-weight: 500;
}

/* Buttons */
.btn-save,
.btn-next {
    background-color: #8C1D40 !important;
    color: white !important;
    border-color: #8C1D40 !important;
    margin-left: 10px;
}

.btn-save:hover,
.btn-next:hover {
    background-color: #6b1630 !important;
    border-color: #6b1630 !important;
    color: white !important;
}

.btn-outline-secondary {
    color: #8C1D40 !important;
    border-color: #8C1D40 !important;
}

.btn-outline-secondary:hover {
    background-color: #8C1D40 !important;
    color: white !important;
}

/* Checkboxes */
.form-check-input:checked {
    background-color: #8C1D40 !important;
    border-color: #8C1D40 !important;
}

.form-check-input:focus {
    border-color: #8C1D40 !important;
    box-shadow: 0 0 0 0.2rem rgba(140, 29, 64, 0.15) !important;
}

/* Select Dropdown */
select.form-control {
    color: #495057;
    background-color: white;
    height: auto;
    min-height: 38px;
    padding: 0.375rem 0.75rem;
    font-size: 14px;
    line-height: 1.5;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3E%3Cpath fill='%238C1D40' d='M2.5 0L1 1.5 3.5 4 1 6.5 2.5 8l4-4-4-4z' transform='rotate(90 4 4)'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 8px 10px;
    padding-right: 2rem;
}

select.form-control option {
    color: #495057;
    background-color: white;
    padding: 8px;
    font-size: 14px;
    min-height: 30px;
    display: block;
}

select.form-control:focus {
    border-color: #8C1D40 !important;
    box-shadow: 0 0 0 0.2rem rgba(140, 29, 64, 0.15) !important;
    outline: none;
}

/* Tree View */
.tree-content {
    color: #495057;
}

.tree-icon {
    color: #8C1D40 !important;
}

.tree-label {
    color: #495057;
}

.state-item .tree-content {
    background-color: #fff3f3;
    border: 1px solid #ffe0e0;
}

.state-item .tree-content:hover {
    background-color: #ffe6e6;
    border-color: #ffcccc;
}

/* Loading Spinner */
.loading-text {
    color: #8C1D40 !important;
}

.spinner-border {
    color: #8C1D40 !important;
}

/* Scrollbar */
.geography-tree::-webkit-scrollbar-thumb {
    background: #8C1D40 !important;
}

.geography-tree::-webkit-scrollbar-thumb:hover {
    background: #6b1630 !important;
}

/* Hierarchy Path */
.path-item {
    color: #8C1D40 !important;
    font-weight: 500;
}

/* Step Indicators */
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
    background: #e9ecef;
    transform: translateY(-50%);
    z-index: 0;
}

.step {
    display: flex;
    flex-direction: row;
    align-items: center;
    position: relative;
    z-index: 1;
    background: white;
    padding: 0 8px;
    min-width: 80px;
    gap: 6px;
}

.step-number {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #fff;
    border: 1.5px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 11px;
    transition: all 0.3s ease;
    flex-shrink: 0;
}

.step>div:last-child {
    font-size: 14px;
    color: #495057;
    font-weight: 500;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.step.active .step-number {
    background-color: #8C1D40 !important;
    border-color: #8C1D40 !important;
    color: white !important;
    box-shadow: 0 0 0 2px rgba(140, 29, 64, 0.1);
}

.step.active>div:last-child {
    color: #8C1D40 !important;
    font-weight: 600;
    font-size: 14px;
}

.step.completed .step-number {
    background-color: #8C1D40 !important;
    border-color: #8C1D40 !important;
    color: white !important;
}

.step.completed>div:last-child {
    color: #8C1D40 !important;
    font-size: 14px;
}

/* Updated progress line styles */
.step-container::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: #8C1D40;
    transform: translateY(-50%);
    z-index: 0;
    width: 0;
    transition: width 0.3s ease;
}

/* Calculate width based on current step and total steps */
.step-container[data-progress="1"]::after {
    width: 0%;
}

.step-container[data-progress="2"]::after {
    width: 33.33%;
}

.step-container[data-progress="3"]::after {
    width: 66.66%;
}

.step-container[data-progress="4"]::after {
    width: 100%;
}

.step-container[data-progress="5"]::after {
    width: 100%;
}

/* Add dynamic step width calculation */
.step-container[data-total-steps="1"]::after {
    width: 0%;
}

.step-container[data-total-steps="2"][data-progress="1"]::after {
    width: 0%;
}

.step-container[data-total-steps="2"][data-progress="2"]::after {
    width: 100%;
}

.step-container[data-total-steps="3"][data-progress="1"]::after {
    width: 0%;
}

.step-container[data-total-steps="3"][data-progress="2"]::after {
    width: 50%;
}

.step-container[data-total-steps="3"][data-progress="3"]::after {
    width: 100%;
}

.step-container[data-total-steps="4"][data-progress="1"]::after {
    width: 0%;
}

.step-container[data-total-steps="4"][data-progress="2"]::after {
    width: 33.33%;
}

.step-container[data-total-steps="4"][data-progress="3"]::after {
    width: 66.66%;
}

.step-container[data-total-steps="4"][data-progress="4"]::after {
    width: 100%;
}

.step-container[data-total-steps="5"][data-progress="1"]::after {
    width: 0%;
}

.step-container[data-total-steps="5"][data-progress="2"]::after {
    width: 25%;
}

.step-container[data-total-steps="5"][data-progress="3"]::after {
    width: 50%;
}

.step-container[data-total-steps="5"][data-progress="4"]::after {
    width: 75%;
}

.step-container[data-total-steps="5"][data-progress="5"]::after {
    width: 100%;
}

/* Keep existing layout styles */
.container {
    max-width: 1200px;
}

.row {
    margin-left: -15px;
    margin-right: -15px;
}

.col-md-6,
.col-md-8,
.col-md-4 {
    padding-left: 15px;
    padding-right: 15px;
}

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
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.main-container {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin-bottom: 20px;
}

.button-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}

.geography-overview {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
}

.geography-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.view-summary {
    color: #8C1D40 !important;
    display: flex;
    align-items: center;
}

.view-summary svg {
    margin-right: 5px;
}

.state-district-group {
    border: 1px solid #eee;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 20px;
}

.state-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    margin-bottom: 15px;
}

.state-header h5 {
    margin: 0;
    color: #8C1D40 !important;
}

.district-block-group,
.block-gp-group,
.gp-village-group {
    border: 1px solid #eee;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 20px;
}

.district-header,
.block-header,
.gp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    margin-bottom: 15px;
}

.district-header h5,
.block-header h5,
.gp-header h5 {
    margin: 0;
    color: #8C1D40 !important;
}

.form-group {
    margin-bottom: 1.5rem;
    position: relative;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #8C1D40 !important;
}

.form-control:disabled {
    background-color: var(--hover-bg);
    cursor: not-allowed;
}

.main-container.loading {
    opacity: 0.7;
    pointer-events: none;
}

.btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.main-container {
    transition: opacity 0.3s ease;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.spinner-border {
    width: 3rem;
    height: 3rem;
    border: 0.25em solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
}

.form-check {
    display: flex;
    align-items: center;
    white-space: nowrap;
    margin-bottom: 0;
}

.form-check-label {
    color: #000000 !important;
    margin-left: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

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

.state-header,
.district-header,
.block-header,
.gp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    margin-bottom: 15px;
    flex-wrap: nowrap;
}

.state-header h5,
.district-header h5,
.block-header h5,
.gp-header h5 {
    margin: 0;
    color: #8C1D40 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 10px;
}

.state-header .form-check,
.district-header .form-check,
.block-header .form-check,
.gp-header .form-check {
    flex-shrink: 0;
}

.hierarchy-path {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
    font-size: 0.9rem;
    color: #666;
}

.path-item {
    color: #8C1D40 !important;
    font-weight: 500;
}

.path-separator {
    color: #999;
    margin: 0 5px;
}

.state-header,
.district-header,
.block-header,
.gp-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 10px;
}

.state-header .hierarchy-path,
.district-header .hierarchy-path,
.block-header .hierarchy-path,
.gp-header .hierarchy-path {
    flex: 1;
    min-width: 200px;
}

.state-header .form-check,
.district-header .form-check,
.block-header .form-check,
.gp-header .form-check {
    flex-shrink: 0;
}

.geography-tree {
    max-height: 600px;
    overflow-y: auto;
    padding-right: 10px;
}

.tree-item {
    margin-bottom: 5px;
}

.tree-content {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 4px;
    background-color: #f8f9fa;
    transition: all 0.2s ease;
    cursor: pointer;
    user-select: none;
}

.tree-content:hover {
    background-color: #e9ecef;
}

.tree-icon {
    margin-right: 8px;
    font-size: 10px;
    color: #8C1D40 !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 14px;
    height: 14px;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: bold;
}

.tree-label {
    flex: 1;
    font-size: 0.9rem;
    color: #495057;
}

.tree-count {
    font-size: 0.8rem;
    color: #6c757d;
    margin-left: 8px;
}

.tree-children {
    margin-left: 20px;
    padding-left: 10px;
    border-left: 2px solid #dee2e6;
    transition: all 0.3s ease;
}

.state-item .tree-content {
    background-color: #fff3f3;
    border: 1px solid #ffe0e0;
}

.state-item .tree-content:hover {
    background-color: #ffe6e6;
    border-color: #ffcccc;
}

.district-item .tree-content {
    background-color: #f8f9fa;
}

.block-item .tree-content {
    background-color: #f0f7ff;
}

.gp-item .tree-content {
    background-color: #f0fff4;
}

.village-item .tree-content {
    background-color: #fffaf0;
}

.geography-overview {
    position: sticky;
    top: 20px;
}

.geography-tree::-webkit-scrollbar {
    width: 6px;
}

.geography-tree::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.geography-tree::-webkit-scrollbar-thumb {
    background: #8C1D40 !important;
    border-radius: 3px;
}

.geography-tree::-webkit-scrollbar-thumb:hover {
    background: #6b1630 !important;
}

/* .toggle-icon.expanded {
    transform: rotate(90deg);
} */

/* Ensure container has proper width */
.container-fluid {
    padding-left: 15px;
    padding-right: 15px;
}

.col-md-6 {
    width: 100%;
    max-width: 400px;
}

/* Add new styles for collapsible tree */
.tree-content {
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s ease;
}

.tree-content:hover {
    background-color: rgba(140, 29, 64, 0.05);
}

.toggle-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    margin-right: 4px;
    transition: transform 0.2s ease;
}

/* .toggle-icon.expanded {
    transform: rotate(90deg);
} */

.tree-children {
    margin-left: 20px;
    padding-left: 10px;
    border-left: 2px solid #dee2e6;
    transition: all 0.3s ease;
}

.tree-item {
    margin-bottom: 4px;
}

.tree-content {
    padding: 8px 12px;
    border-radius: 4px;
    display: flex;
    align-items: center;
}

/* Hierarchy-specific styles */
.state-item .tree-content {
    background-color: #fff3f3;
    border: 1px solid #ffe0e0;
}

.district-item .tree-content {
    background-color: #f8f9fa;
}

.block-item .tree-content {
    background-color: #f0f7ff;
}

.gp-item .tree-content {
    background-color: #f0fff4;
}

.village-item .tree-content {
    background-color: #fffaf0;
}

/* Headers */
.state-header h5,
.district-header h5,
.block-header h5,
.gp-header h5 {
    color: #8C1D40 !important;
}

/* Keep other existing styles but update colors */
.header {
    color: #8C1D40 !important;
    font-size: 16px !important;
    font-weight: 500;
}

/* Add !important to all color-related properties */
</style>