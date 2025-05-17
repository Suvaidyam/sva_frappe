<template>
    <div class="container-fluid mt-4">
        <h1 class="header text-center">Watershed Management</h1>

        <!-- Add loading overlay -->
        <div class="loading-overlay" v-if="isLoading">
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="loading-text">Loading...</div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="hierarchyLevel">Select Lowest Hierarchy Level</label>
                    <select id="hierarchyLevel" class="form-control" v-model="selectedHierarchyLevel"
                        @change="handleHierarchyLevelChange" :disabled="isLoading">
                        <option value="state">State</option>
                        <option value="district">District</option>
                        <option value="block">Block</option>
                        <option value="gramPanchayat">Gram Panchayat</option>
                        <option value="village">Village</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <div class="main-container" :class="{ 'loading': isLoading }">
                    <div class="step-container">
                        <div class="step" :class="{ active: currentStep >= 1 }">
                            <div class="step-number">1</div>
                            <div>States</div>
                        </div>
                        <div class="step" v-if="selectedHierarchyLevel !== 'state'"
                            :class="{ active: currentStep >= 2 }">
                            <div class="step-number">2</div>
                            <div>Districts</div>
                        </div>
                        <div class="step"
                            v-if="selectedHierarchyLevel !== 'state' && selectedHierarchyLevel !== 'district'"
                            :class="{ active: currentStep >= 3 }">
                            <div class="step-number">3</div>
                            <div>Blocks</div>
                        </div>
                        <div class="step"
                            v-if="selectedHierarchyLevel !== 'state' && selectedHierarchyLevel !== 'district' && selectedHierarchyLevel !== 'block'"
                            :class="{ active: currentStep >= 4 }">
                            <div class="step-number">4</div>
                            <div>Gram Panchayats</div>
                        </div>
                        <div class="step" v-if="selectedHierarchyLevel === 'village'"
                            :class="{ active: currentStep >= 5 }">
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
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getBlockName(blockId) }}</span>
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
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getBlockName(getGPBlock(gpId)) }}</span>
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
                        <button class="btn btn-save" @click="saveSelection" :disabled="isLoading">Save</button>
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
                            <div class="tree-content" @click="toggleStateExpansion(stateId)">
                                <span class="tree-icon toggle-icon" :class="{ 'expanded': isStateExpanded(stateId) }">
                                    {{ isStateExpanded(stateId) ? '▼' : '▶' }}
                                </span>
                                <span class="tree-icon">📌</span>
                                <span class="tree-label">{{ getStateName(stateId) }}</span>
                                <span class="tree-count" v-if="getDistrictsForState(stateId).length">
                                    ({{ getDistrictsForState(stateId).length }})
                                </span>
                            </div>
                            <div class="tree-children" v-show="selectedDistricts.length && isStateExpanded(stateId)">
                                <div v-for="district in getDistrictsForState(stateId)" :key="district.id"
                                    class="tree-item district-item" v-show="selectedDistricts.includes(district.id)">
                                    <div class="tree-content">
                                        <span class="tree-icon">📍</span>
                                        <span class="tree-label">{{ district.name }}</span>
                                        <span class="tree-count" v-if="getBlocksForDistrict(district.id).length">
                                            ({{ getBlocksForDistrict(district.id).length }})
                                        </span>
                                    </div>
                                    <div class="tree-children" v-if="selectedBlocks.length">
                                        <div v-for="block in getBlocksForDistrict(district.id)" :key="block.id"
                                            class="tree-item block-item" v-show="selectedBlocks.includes(block.id)">
                                            <div class="tree-content">
                                                <span class="tree-icon">🏘️</span>
                                                <span class="tree-label">{{ block.name }}</span>
                                                <span class="tree-count"
                                                    v-if="getGramPanchayatsForBlock(block.id).length">
                                                    ({{ getGramPanchayatsForBlock(block.id).length }})
                                                </span>
                                            </div>
                                            <div class="tree-children" v-if="selectedGramPanchayats.length">
                                                <div v-for="gp in getGramPanchayatsForBlock(block.id)" :key="gp.id"
                                                    class="tree-item gp-item"
                                                    v-show="selectedGramPanchayats.includes(gp.id)">
                                                    <div class="tree-content">
                                                        <span class="tree-icon">🏛️</span>
                                                        <span class="tree-label">{{ gp.name }}</span>
                                                        <span class="tree-count" v-if="getVillagesForGP(gp.id).length">
                                                            ({{ getVillagesForGP(gp.id).length }})
                                                        </span>
                                                    </div>
                                                    <div class="tree-children" v-if="selectedVillages.length">
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
    name: 'WatershedManagement',
    data() {
        return {
            currentStep: 1,
            selectedHierarchyLevel: 'village',
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
            expandedStateId: null
        };
    },
    async created() {
        await this.loadStates();
    },
    computed: {
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
        totalSteps() {
            switch (this.selectedHierarchyLevel) {
                case 'state':
                    return 1;
                case 'district':
                    return 2;
                case 'block':
                    return 3;
                case 'gramPanchayat':
                    return 4;
                case 'village':
                    return 5;
                default:
                    return 5;
            }
        }
    },
    methods: {
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
                            // Set the first state as expanded by default if there are states
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

            console.log('Selected states:', this.selectedStates);
            console.log('States data:', this.states);
            console.log('Selected states details:', this.selectedStates.map(stateId => {
                const state = this.states.find(s => s.id === stateId);
                return state ? { id: state.id, name: state.name } : null;
            }));

            await this.withLoading(async () => {
                try {
                    const response = await frappe.call({
                        method: 'sva_frappe.api.get_districts',
                        args: {
                            state: this.selectedStates
                        },
                        callback: (r) => {
                            console.log('API Response:', r);
                            console.log('API Response message:', r.message);
                            if (r.message) {
                                // Group districts by state
                                this.districts = {};
                                this.availableDistricts = r.message.map(district => {
                                    console.log('Processing district:', district);
                                    return {
                                        id: district.name,
                                        name: district.district_name,
                                        code: district.district_code,
                                        state: district.state
                                    };
                                });

                                console.log('Processed districts:', this.availableDistricts);

                                this.availableDistricts.forEach(district => {
                                    if (!this.districts[district.state]) {
                                        this.districts[district.state] = [];
                                    }
                                    this.districts[district.state].push(district);
                                });

                                console.log('Grouped districts:', this.districts);
                                console.log('Districts by state:', Object.keys(this.districts).map(stateId => ({
                                    stateId,
                                    count: this.districts[stateId].length,
                                    districts: this.districts[stateId]
                                })));

                                // Filter out districts that don't belong to selected states
                                this.selectedDistricts = this.selectedDistricts.filter(districtId => {
                                    const district = this.availableDistricts.find(d => d.id === districtId);
                                    return district && this.selectedStates.includes(district.state);
                                });

                                console.log('Final selected districts:', this.selectedDistricts);
                            } else {
                                console.error('No message in API response');
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
                            // Group blocks by district
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

                            // Filter out blocks that don't belong to selected districts
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
                            // Group gram panchayats by block
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

                            // Filter out gram panchayats that don't belong to selected blocks
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
                            // Group villages by gram panchayat
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

                            // Filter out villages that don't belong to selected gram panchayats
                            this.selectedVillages = this.selectedVillages.filter(villageId => {
                                const village = this.availableVillages.find(v => v.id === villageId);
                                return village && this.selectedGramPanchayats.includes(village.gram_panchayat);
                            });
                        }
                    }
                });
            });
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
            }
        },
        goBack() {
            if (this.currentStep > 1) {
                this.currentStep--;
            }
        },
        async saveSelection() {
            // Create a map to store unique combinations
            const selectionMap = new Map();

            // Process states
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

            // Process districts
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

            // Process blocks
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

            // Process gram panchayats
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

            // Process villages
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

            // Convert map to array and filter based on hierarchy level
            let selection = Array.from(selectionMap.values());

            // Filter based on hierarchy level
            switch (this.selectedHierarchyLevel) {
                case 'state':
                    selection = selection.filter(item => item.state && !item.district);
                    break;
                case 'district':
                    selection = selection.filter(item => item.state && item.district && !item.block);
                    break;
                case 'block':
                    selection = selection.filter(item => item.state && item.district && item.block && !item.gramPanchayat);
                    break;
                case 'gramPanchayat':
                    selection = selection.filter(item => item.state && item.district && item.block && item.gramPanchayat && !item.village);
                    break;
                case 'village':
                    selection = selection.filter(item => item.state && item.district && item.block && item.gramPanchayat && item.village);
                    break;
            }

            // Here you can add code to save the selection to your database
            console.log('Selected Hierarchy Level:', this.selectedHierarchyLevel);
            console.log('Selection:', selection);

            frappe.show_alert({
                message: __('Selection saved successfully'),
                indicator: 'green'
            });

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
                const districtIds = stateDistricts.map(d => d.id);
                this.selectedDistricts = this.selectedDistricts.filter(id => !districtIds.includes(id));

                this.selectedBlocks = this.selectedBlocks.filter(blockId => {
                    const block = this.availableBlocks.find(b => b.id === blockId);
                    return block && !districtIds.includes(Math.floor(blockId / 100));
                });

                this.updateGramPanchayats();
                this.updateVillages();
            } else {
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
                const blockIds = districtBlocks.map(b => b.id);
                this.selectedBlocks = this.selectedBlocks.filter(id => !blockIds.includes(id));

                this.selectedGramPanchayats = this.selectedGramPanchayats.filter(gpId => {
                    const gp = this.availableGramPanchayats.find(g => g.id === gpId);
                    return gp && !blockIds.includes(Math.floor(gpId / 100));
                });

                this.updateVillages();
            } else {
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
                const gpIds = blockGPs.map(gp => gp.id);
                this.selectedGramPanchayats = this.selectedGramPanchayats.filter(id => !gpIds.includes(id));

                this.selectedVillages = this.selectedVillages.filter(villageId => {
                    const village = this.availableVillages.find(v => v.id === villageId);
                    return village && !gpIds.includes(Math.floor(villageId / 100));
                });
            } else {
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
                const villageIds = gpVillages.map(v => v.id);
                this.selectedVillages = this.selectedVillages.filter(id => !villageIds.includes(id));
            } else {
                const villageIds = gpVillages.map(v => v.id);
                this.selectedVillages = [...new Set([...this.selectedVillages, ...villageIds])];
            }
        },
        handleHierarchyLevelChange() {
            if (this.currentStep > this.totalSteps) {
                this.currentStep = 1;
            }

            switch (this.selectedHierarchyLevel) {
                case 'state':
                    this.selectedDistricts = [];
                    this.selectedBlocks = [];
                    this.selectedGramPanchayats = [];
                    this.selectedVillages = [];
                    break;
                case 'district':
                    this.selectedBlocks = [];
                    this.selectedGramPanchayats = [];
                    this.selectedVillages = [];
                    break;
                case 'block':
                    this.selectedGramPanchayats = [];
                    this.selectedVillages = [];
                    break;
                case 'gramPanchayat':
                    this.selectedVillages = [];
                    break;
            }

            this.updateAvailableItems();
        },
        updateAvailableItems() {
            this.updateDistricts();
            if (this.selectedHierarchyLevel !== 'state') {
                this.updateBlocks();
                if (this.selectedHierarchyLevel !== 'district') {
                    this.updateGramPanchayats();
                    if (this.selectedHierarchyLevel !== 'block') {
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
            this.expandedStateId = this.expandedStateId === stateId ? null : stateId;
        },
        isStateExpanded(stateId) {
            return this.expandedStateId === stateId;
        }
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
.step.active .step-number {
    background-color: #8C1D40 !important;
    border-color: #8C1D40 !important;
    color: white !important;
}

.step.active>div:last-child {
    color: #8C1D40 !important;
}

/* Geography Header */
.geography-header h5 {
    color: #8C1D40 !important;
}

.view-summary {
    color: #8C1D40 !important;
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
.form-group label {
    color: #8C1D40 !important;
}

.tree-icon {
    color: #8C1D40 !important;
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

.step-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    position: relative;
    padding: 0 15px;
}

.step-container::before {
    content: '';
    position: absolute;
    top: 12px;
    left: 0;
    right: 0;
    height: 1px;
    background: #ccc;
    z-index: 0;
}

.step {
    display: flex;
    align-items: center;
    position: relative;
    z-index: 1;
    background: white;
    padding: 0 8px;
}

.step-number {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: #fff;
    border: 1px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 8px;
    font-weight: 500;
    font-size: 12px;
}

.step.active .step-number {
    background-color: #8C1D40 !important;
    border-color: #8C1D40 !important;
    color: white !important;
}

.step>div:last-child {
    font-size: 13px;
    color: #666;
}

.step.active>div:last-child {
    color: #8C1D40 !important;
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

.toggle-icon.expanded {
    transform: rotate(90deg);
}

/* Ensure container has proper width */
.container-fluid {
    padding-left: 15px;
    padding-right: 15px;
}

.col-md-6 {
    width: 100%;
    max-width: 400px;
}
</style>