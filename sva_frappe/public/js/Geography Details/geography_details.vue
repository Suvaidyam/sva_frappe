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
                            <div>{{ __("States") }}</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy !== 'State'"
                            :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
                            <div class="step-number">2</div>
                            <div>{{ __("Districts") }}</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy !== 'State' && lowest_hierarchy !== 'District'"
                            :class="{ 'active': currentStep >= 3, 'completed': currentStep > 3 }">
                            <div class="step-number">3</div>
                            <div>{{ __("Blocks") }}</div>
                        </div>
                        <div class="step"
                            v-if="lowest_hierarchy !== 'State' && lowest_hierarchy !== 'District' && lowest_hierarchy !== 'Block'"
                            :class="{ 'active': currentStep >= 4, 'completed': currentStep > 4 }">
                            <div class="step-number">4</div>
                            <div>{{ __("Gram Panchayats") }}</div>
                        </div>
                        <div class="step" v-if="lowest_hierarchy === 'Village'"
                            :class="{ 'active': currentStep >= 5, 'completed': currentStep > 5 }">
                            <div class="step-number">5</div>
                            <div>{{ __("Villages") }}</div>
                        </div>
                    </div>

                    <div v-if="currentStep === 1">
                        <h4>Available States</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input type="checkbox" :id="`select-all-states`" :checked="allStatesSelected"
                                    @change="toggleAllStates" class="form-check-input" :disabled="read_only">
                                <label class="form-check-label" :for="`select-all-states`" @click.prevent="toggleAllStates">
                                    Select All {{ __("States") }}
                                </label>
                            </div>
                        </div>
                        <div class="checkbox-container">
                            <div class="checkbox-item" v-for="(state, index) in states" :key="state.id">
                                <div class="form-check">
                                    <input type="checkbox" :id="`state-${state.id}`" :value="state.id"
                                        v-model="selectedStates" @change="updateDistricts" class="form-check-input"
                                        :disabled="read_only || isStatePreserved(state.id)">
                                    <label class="form-check-label" :for="`state-${state.id}`" @click.prevent="toggleState(state.id)">
                                        {{ state.name }}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 2">
                        <h4>Available {{ __("Districts") }}</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input type="checkbox" :id="`select-all-districts`" :checked="allDistrictsSelected"
                                    @change="toggleAllDistricts" class="form-check-input" :disabled="read_only">
                                <label class="form-check-label" :for="`select-all-districts`" @click.prevent="toggleAllDistricts">
                                    Select All {{ __("Districts") }}
                                </label>
                            </div>
                        </div>
                        <div v-for="stateId in selectedStates" :key="stateId" class="state-district-group mb-4">
                            <div class="state-header mb-2">
                                <div class="hierarchy-path">
                                    <span class="path-item">{{ getStateName(stateId) }}</span>
                                </div>
                                <div class="form-check">
                                    <input type="checkbox" :id="`select-all-districts-${stateId}`"
                                        :checked="isAllDistrictsSelectedForState(stateId)"
                                        @change="toggleAllDistrictsForState(stateId)" class="form-check-input"
                                        :disabled="read_only">
                                    <label class="form-check-label" :for="`select-all-districts-${stateId}`" @click.prevent="toggleAllDistrictsForState(stateId)">
                                        Select All {{ __("Districts") }}
                                    </label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="district in getDistrictsForState(stateId)"
                                    :key="district.id">
                                    <div class="form-check">
                                        <input type="checkbox" :id="`district-${district.id}`" :value="district.id"
                                            v-model="selectedDistricts" @change="updateBlocks" class="form-check-input"
                                            :disabled="read_only || isDistrictPreserved(district.id)">
                                        <label class="form-check-label" :for="`district-${district.id}`" @click.prevent="toggleDistrict(district.id)">
                                            {{ district.name }}
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 3">
                        <h4>Available Blocks</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :id="`select-all-blocks`"
                                    :checked="allBlocksSelected" @change="toggleAllBlocks" :disabled="read_only">
                                <label class="form-check-label" :for="`select-all-blocks`">
                                    Select All {{ __("Blocks") }}
                                </label>
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
                                        :id="`select-all-blocks-${districtId}`"
                                        :checked="isAllBlocksSelectedForDistrict(districtId)"
                                        @change="toggleAllBlocksForDistrict(districtId)" :disabled="read_only">
                                    <label class="form-check-label" :for="`select-all-blocks-${districtId}`">
                                        Select All {{ __("Blocks") }}
                                    </label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="block in getBlocksForDistrict(districtId)"
                                    :key="block.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :id="`block-${block.id}`"
                                            :value="block.id" v-model="selectedBlocks" @change="updateGramPanchayats"
                                            :disabled="read_only || isBlockPreserved(block.id)">
                                        <label class="form-check-label" :for="`block-${block.id}`" @click.prevent="toggleBlock(block.id)">
                                            {{ block.name }}
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 4">
                        <h4>Available {{ __("Gram Panchayats") }}</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :id="`select-all-gps`"
                                    :checked="allGramPanchayatsSelected" @change="toggleAllGramPanchayats"
                                    :disabled="read_only">
                                <label class="form-check-label" :for="`select-all-gps`">
                                    Select All {{ __("Gram Panchayats") }}
                                </label>
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
                                    <input class="form-check-input" type="checkbox" :id="`select-all-gps-${blockId}`"
                                        :checked="isAllGramPanchayatsSelectedForBlock(blockId)"
                                        @change="toggleAllGramPanchayatsForBlock(blockId)" :disabled="read_only">
                                    <label class="form-check-label" :for="`select-all-gps-${blockId}`">
                                        Select All {{ __("Gram Panchayats") }}
                                    </label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="gp in getGramPanchayatsForBlock(blockId)"
                                    :key="gp.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :id="`gp-${gp.id}`"
                                            :value="gp.id" v-model="selectedGramPanchayats" @change="updateVillages"
                                            :disabled="read_only || isGramPanchayatPreserved(gp.id)">
                                        <label class="form-check-label" :for="`gp-${gp.id}`" @click.prevent="toggleGramPanchayat(gp.id)">
                                            {{ gp.name }}
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentStep === 5">
                        <h4>Available {{ __("Villages") }}</h4>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" :id="`select-all-villages`"
                                    :checked="allVillagesSelected" @change="toggleAllVillages" :disabled="read_only">
                                <label class="form-check-label" :for="`select-all-villages`">
                                    Select All {{ __("Villages") }}
                                </label>
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
                                    <span class="path-separator">></span>
                                    <span class="path-item">{{ getGramPanchayatName(gpId) }}</span>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" :id="`select-all-villages-${gpId}`"
                                        :checked="isAllVillagesSelectedForGP(gpId)"
                                        @change="toggleAllVillagesForGP(gpId)" :disabled="read_only">
                                    <label class="form-check-label" :for="`select-all-villages-${gpId}`">
                                        Select All {{ __("Villages") }}
                                    </label>
                                </div>
                            </div>
                            <div class="checkbox-container">
                                <div class="checkbox-item" v-for="village in getVillagesForGP(gpId)" :key="village.id">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" :id="`village-${village.id}`"
                                            :value="village.id" v-model="selectedVillages" 
                                            :disabled="read_only || isVillagePreserved(village.id)">
                                        <label class="form-check-label" :for="`village-${village.id}`" @click.prevent="toggleVillage(village.id)">
                                            {{ village.name }}
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="button-group">
                        <button class="btn btn-default" @click="goBack" v-if="currentStep > 1"
                            :disabled="isLoading">Back</button>
                        <button class="btn btn-primary" @click="saveSelection"
                            v-if="isAtLowestHierarchy && !read_only && !disable_save_btn"
                            :disabled="isLoading || isSaving">
                            <span v-if="isSaving" class="spinner-border spinner-border-sm me-2" role="status"
                                aria-hidden="true"></span>
                            <span v-if="!isSaving">Save</span>
                            <span v-else>Saving...</span>
                        </button>
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

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';

// ============ PROPS DEFINITION ============
const props = defineProps({
    filters: {
        type: Object,
        default: () => ({})
    },
    disable_save_btn: {
        type: Boolean,
        default: false
    },
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
    },
    preserve_data: {
        type: Object,
        default: {}
    },
    existing_data: {
        type: Array,
        default: []
    }
});

// ============ REACTIVE STATE ============
const currentStep = ref(1);
const states = ref([]);
const districts = reactive({});
const blocks = reactive({});
const gramPanchayats = reactive({});
const villages = reactive({});
const selectedStates = ref([]);
const selectedDistricts = ref([]);
const selectedBlocks = ref([]);
const selectedGramPanchayats = ref([]);
const selectedVillages = ref([]);
const availableDistricts = ref([]);
const availableBlocks = ref([]);
const availableGramPanchayats = ref([]);
const availableVillages = ref([]);
const isLoading = ref(false);
const expandedStateId = ref(null);
const current_docname = ref(null);
const lowest_hierarchy = ref('District');
const isDataLoaded = ref(false);
const expandedStates = reactive(new Set());
const expandedDistricts = reactive(new Set());
const expandedBlocks = reactive(new Set());
const expandedGPs = reactive(new Set());
const doctype = ref('Geography Details');
const isSaving = ref(false);

// ============ COMPUTED PROPERTIES ============
const totalSteps = computed(() => {
    switch (lowest_hierarchy.value) {
        case 'State': return 1;
        case 'District': return 2;
        case 'Block': return 3;
        case 'Gram Panchayat': return 4;
        case 'Village': return 5;
        default: return 2;
    }
});

const preserveData = computed(() => {
    let preservedStates = new Set();
    let preservedDistricts = new Set();
    let preservedBlocks = new Set();
    let preservedGramPanchayats = new Set();
    let preservedVillages = new Set();

    if (props.preserve_data?.geography_details) {
        props.preserve_data.geography_details.forEach(detail => {
            if (detail.state) preservedStates.add(detail.state);
            if (detail.district) preservedDistricts.add(detail.district);
            if (detail.block) preservedBlocks.add(detail.block);
            if (detail.gram_panchayat) preservedGramPanchayats.add(detail.gram_panchayat);
            if (detail.village) preservedVillages.add(detail.village);
        });
    }
    
    return {
        states: preservedStates,
        districts: preservedDistricts,
        blocks: preservedBlocks,
        gramPanchayats: preservedGramPanchayats,
        villages: preservedVillages
    };
});

const themeColors = computed(() => ({
    primary: frappe.boot.my_theme?.button_background_color || '#171717',
    primaryLight: getLightColor(frappe.boot.my_theme?.button_background_color || '#171717')
}));

const isAtLowestHierarchy = computed(() => {
    switch (lowest_hierarchy.value) {
        case 'State': return currentStep.value === 1;
        case 'District': return currentStep.value === 2;
        case 'Block': return currentStep.value === 3;
        case 'Gram Panchayat': return currentStep.value === 4;
        case 'Village': return currentStep.value === 5;
        default: return false;
    }
});

const allStatesSelected = computed(() =>
    states.value.length > 0 && selectedStates.value.length === states.value.length
);

const allDistrictsSelected = computed(() =>
    availableDistricts.value.length > 0 &&
    selectedDistricts.value.length === availableDistricts.value.length
);

const allBlocksSelected = computed(() =>
    availableBlocks.value.length > 0 &&
    selectedBlocks.value.length === availableBlocks.value.length
);

const allGramPanchayatsSelected = computed(() =>
    availableGramPanchayats.value.length > 0 &&
    selectedGramPanchayats.value.length === availableGramPanchayats.value.length
);

const allVillagesSelected = computed(() =>
    availableVillages.value.length > 0 &&
    selectedVillages.value.length === availableVillages.value.length
);

// ============ CORE METHODS ============
const loadDefaultLowestHierarchy = async () => {
    lowest_hierarchy.value = props.frm.doc[props.hierarchy_level_field];
};

const loadExistingData = async () => {
    if (props.existing_data.length > 0) {
        const stateSet = new Set();
        const districtSet = new Set();
        const blockSet = new Set();
        const gpSet = new Set();
        const villageSet = new Set();
        props.existing_data.forEach((detail) => {
            if (detail.state && detail.state.trim()) stateSet.add(detail.state);
            if (detail.district && detail.district.trim()) districtSet.add(detail.district);
            if (detail.block && detail.block.trim()) blockSet.add(detail.block);
            if (detail.gram_panchayat && detail.gram_panchayat.trim()) gpSet.add(detail.gram_panchayat);
            if (detail.village && detail.village.trim()) villageSet.add(detail.village);
        });
        selectedStates.value = Array.from(stateSet);
        selectedDistricts.value = Array.from(districtSet);
        selectedBlocks.value = Array.from(blockSet);
        selectedGramPanchayats.value = Array.from(gpSet);
        selectedVillages.value = Array.from(villageSet);
        
        await loadStates();
        await updateAvailableItems();
        expandTreeBasedOnStep();
        return;
    }else{
        if (isLoading.value) return;
        await withLoading(async () => {
            if (!props.frm.doctype || !props.frm.docname) return;
    
            try {
                const doc = await frappe.xcall('sva_frappe.api.get_geography_details', {
                    filters: JSON.stringify({
                        document_type: props.frm.doctype,
                        docname: props.frm.docname
                    })
                });
                if (doc) {
                    await resetData();
                    if (props.frm.doc[props.hierarchy_level_field]) {
                        lowest_hierarchy.value = props.frm.doc[props.hierarchy_level_field];
                    }
                    
                    if (doc.geography_details) {
                        const stateSet = new Set();
                        const districtSet = new Set();
                        const blockSet = new Set();
                        const gpSet = new Set();
                        const villageSet = new Set();
                        doc.geography_details.forEach((detail) => {
                            if (detail.state && detail.state.trim()) stateSet.add(detail.state);
                            if (detail.district && detail.district.trim()) districtSet.add(detail.district);
                            if (detail.block && detail.block.trim()) blockSet.add(detail.block);
                            if (detail.gram_panchayat && detail.gram_panchayat.trim()) gpSet.add(detail.gram_panchayat);
                            if (detail.village && detail.village.trim()) villageSet.add(detail.village);
                        });
                        selectedStates.value = Array.from(stateSet);
                        selectedDistricts.value = Array.from(districtSet);
                        selectedBlocks.value = Array.from(blockSet);
                        selectedGramPanchayats.value = Array.from(gpSet);
                        selectedVillages.value = Array.from(villageSet);
    
                        await loadStates();
                        await updateAvailableItems();
                        expandTreeBasedOnStep();
                    }
                } else {
                    // Load states if no geography details exist
                    await loadStates();
                }
    
                // Ensure preserved items are selected
                if (props.preserve_data?.geography_details) {
                    props.preserve_data.geography_details.forEach((detail) => {
                        if (detail.state && !selectedStates.value.includes(detail.state)) {
                            selectedStates.value.push(detail.state);
                        }
                        if (detail.district && !selectedDistricts.value.includes(detail.district)) {
                            selectedDistricts.value.push(detail.district);
                        }
                        if (detail.block && !selectedBlocks.value.includes(detail.block)) {
                            selectedBlocks.value.push(detail.block);
                        }
                        if (detail.gram_panchayat && !selectedGramPanchayats.value.includes(detail.gram_panchayat)) {
                            selectedGramPanchayats.value.push(detail.gram_panchayat);
                        }
                        if (detail.village && !selectedVillages.value.includes(detail.village)) {
                            selectedVillages.value.push(detail.village);
                        }
                    });
                    await updateAvailableItems();
                }
            } catch (error) {
                console.error('Error loading existing data:', error);
                frappe.show_alert({
                    message: __('Error loading existing data'),
                    indicator: 'red'
                });
            }
        });
    }
};

const loadStates = async () => {
    let filters = props.filters.state || [];
    await withLoading(async () => {
        await frappe.call({
            method: 'sva_frappe.api.get_states',
            args: { filters: JSON.stringify(filters) },
            callback: (r) => {
                if (r.message) {
                    states.value = r.message.map(state => ({
                        id: state.name,
                        name: state.state_name,
                        code: state.state_code
                    }));
                    if (states.value.length > 0) {
                        expandedStateId.value = states.value[0].id;
                    }
                }
            }
        });
    });
};

const updateDistricts = async () => {
    const filters = props.filters.district || [];
    if (selectedStates.value.length === 0) {
        availableDistricts.value = [];
        selectedDistricts.value = [];
        await updateBlocks();
        return;
    }

    await withLoading(async () => {
        try {
            await frappe.call({
                method: 'sva_frappe.api.get_districts',
                args: {
                    state: selectedStates.value,
                    filters: JSON.stringify(filters)
                },
                callback: (r) => {
                    if (r.message) {
                        Object.keys(districts).forEach(key => delete districts[key]);

                        availableDistricts.value = r.message.map(district => ({
                            id: district.name,
                            name: district.district_name,
                            code: district.district_code,
                            state: district.state
                        }));

                        availableDistricts.value.forEach(district => {
                            if (!districts[district.state]) {
                                districts[district.state] = [];
                            }
                            districts[district.state].push(district);
                        });

                        selectedDistricts.value = selectedDistricts.value.filter(districtId => {
                            const district = availableDistricts.value.find(d => d.id === districtId);
                            return district && selectedStates.value.includes(district.state);
                        });
                    }
                }
            });
        } catch (error) {
            console.error('Error fetching districts:', error);
        }
    });
    await updateBlocks();
};

const updateBlocks = async () => {
    if (selectedDistricts.value.length === 0) {
        availableBlocks.value = [];
        selectedBlocks.value = [];
        await updateGramPanchayats();
        return;
    }

    await withLoading(async () => {
        await frappe.call({
            method: 'sva_frappe.api.get_blocks',
            args: {
                district: selectedDistricts.value,
                filters: JSON.stringify(props.filters.block || [])
            },
            callback: (r) => {
                if (r.message) {
                    Object.keys(blocks).forEach(key => delete blocks[key]);

                    availableBlocks.value = r.message.map(block => ({
                        id: block.name,
                        name: block.block_name,
                        code: block.block_code,
                        district: block.district,
                        state: block.state
                    }));

                    availableBlocks.value.forEach(block => {
                        if (!blocks[block.district]) {
                            blocks[block.district] = [];
                        }
                        blocks[block.district].push(block);
                    });

                    selectedBlocks.value = selectedBlocks.value.filter(blockId => {
                        const block = availableBlocks.value.find(b => b.id === blockId);
                        return block && selectedDistricts.value.includes(block.district);
                    });
                }
            }
        });
    });
    await updateGramPanchayats();
};

const updateGramPanchayats = async () => {
    if (selectedBlocks.value.length === 0) {
        availableGramPanchayats.value = [];
        selectedGramPanchayats.value = [];
        await updateVillages();
        return;
    }

    await withLoading(async () => {
        await frappe.call({
            method: 'sva_frappe.api.get_gram_panchayats',
            args: { block: selectedBlocks.value },
            callback: (r) => {
                if (r.message) {
                    Object.keys(gramPanchayats).forEach(key => delete gramPanchayats[key]);

                    availableGramPanchayats.value = r.message.map(gp => ({
                        id: gp.name,
                        name: gp.gram_pachayat_name,
                        code: gp.gram_panchayat_code,
                        block: gp.block,
                        district: gp.district,
                        state: gp.state
                    }));

                    availableGramPanchayats.value.forEach(gp => {
                        if (!gramPanchayats[gp.block]) {
                            gramPanchayats[gp.block] = [];
                        }
                        gramPanchayats[gp.block].push(gp);
                    });

                    selectedGramPanchayats.value = selectedGramPanchayats.value.filter(gpId => {
                        const gp = availableGramPanchayats.value.find(g => g.id === gpId);
                        return gp && selectedBlocks.value.includes(gp.block);
                    });
                }
            }
        });
    });
    await updateVillages();
};

const updateVillages = async () => {
    if (props.disable_save_btn) {
        props.frm.geography_data = await saveSelection();
    }

    if (selectedGramPanchayats.value.length === 0) {
        availableVillages.value = [];
        selectedVillages.value = [];
        return;
    }

    await withLoading(async () => {
        await frappe.call({
            method: 'sva_frappe.api.get_villages',
            args: { gram_panchayat: selectedGramPanchayats.value },
            callback: (r) => {
                if (r.message) {
                    Object.keys(villages).forEach(key => delete villages[key]);

                    availableVillages.value = r.message.map(village => ({
                        id: village.name,
                        name: village.village_name,
                        code: village.village_code,
                        gram_panchayat: village.gram_panchayat,
                        block: village.block,
                        district: village.district,
                        state: village.state
                    }));

                    availableVillages.value.forEach(village => {
                        if (!villages[village.gram_panchayat]) {
                            villages[village.gram_panchayat] = [];
                        }
                        villages[village.gram_panchayat].push(village);
                    });

                    selectedVillages.value = selectedVillages.value.filter(villageId => {
                        const village = availableVillages.value.find(v => v.id === villageId);
                        return village && selectedGramPanchayats.value.includes(village.gram_panchayat);
                    });
                }
            }
        });
    });
};

// ============ NAVIGATION & TREE METHODS ============
const expandTreeBasedOnStep = () => {
    expandedStates.clear();
    expandedDistricts.clear();
    expandedBlocks.clear();
    expandedGPs.clear();

    switch (currentStep.value) {
        case 1:
            selectedStates.value.forEach(stateId => expandedStates.add(stateId));
            break;
        case 2:
            selectedStates.value.forEach(stateId => {
                expandedStates.add(stateId);
                getSelectedDistrictsForState(stateId).forEach(district => {
                    expandedDistricts.add(district.id);
                });
            });
            break;
        case 3:
            selectedStates.value.forEach(stateId => {
                expandedStates.add(stateId);
                getSelectedDistrictsForState(stateId).forEach(district => {
                    expandedDistricts.add(district.id);
                    getSelectedBlocksForDistrict(district.id).forEach(block => {
                        expandedBlocks.add(block.id);
                    });
                });
            });
            break;
        case 4:
            selectedStates.value.forEach(stateId => {
                expandedStates.add(stateId);
                getSelectedDistrictsForState(stateId).forEach(district => {
                    expandedDistricts.add(district.id);
                    getSelectedBlocksForDistrict(district.id).forEach(block => {
                        expandedBlocks.add(block.id);
                        getSelectedGramPanchayatsForBlock(block.id).forEach(gp => {
                            expandedGPs.add(gp.id);
                        });
                    });
                });
            });
            break;
        case 5:
            selectedStates.value.forEach(stateId => {
                expandedStates.add(stateId);
                getSelectedDistrictsForState(stateId).forEach(district => {
                    expandedDistricts.add(district.id);
                    getSelectedBlocksForDistrict(district.id).forEach(block => {
                        expandedBlocks.add(block.id);
                        getSelectedGramPanchayatsForBlock(block.id).forEach(gp => {
                            expandedGPs.add(gp.id);
                        });
                    });
                });
            });
            break;
    }
};

const goNext = () => {
    if (currentStep.value >= totalSteps.value) return;

    const validationResult = validateCurrentStepSelection();
    if (!validationResult.isValid) {
        showValidationError(validationResult);
        return;
    }

    const canProceed = (() => {
        switch (currentStep.value) {
            case 1: return selectedStates.value.length > 0;
            case 2: return selectedDistricts.value.length > 0;
            case 3: return selectedBlocks.value.length > 0;
            case 4: return selectedGramPanchayats.value.length > 0;
            default: return true;
        }
    })();

    if (canProceed) {
        currentStep.value++;
        switch (currentStep.value) {
            case 2: updateBlocks(); break;
            case 3: updateGramPanchayats(); break;
            case 4: updateVillages(); break;
        }
        expandTreeBasedOnStep();
    }
};

const goBack = () => {
    if (currentStep.value > 1) {
        currentStep.value--;
        expandTreeBasedOnStep();
    }
};

// ============ SAVE FUNCTIONALITY ============
const saveSelection = async () => {
    isSaving.value = true;

    if (!props.disable_save_btn) {
        const validationResult = validateAllLevelsForSave();
        if (!validationResult.isValid) {
            showValidationError(validationResult);
            isSaving.value = false;
            return;
        }
    }

    const selectionMap = new Map();

    // Build selection map for all hierarchy levels
    selectedStates.value.forEach(stateId => {
        const state = states.value.find(s => s.id == stateId);
        if (state) {
            selectionMap.set(state.id, {
                state: { id: state.id, name: state.name, code: state.code }
            });
        }
    });

    selectedDistricts.value.forEach(districtId => {
        const district = availableDistricts.value.find(d => d.id === districtId);
        if (district) {
            const state = states.value.find(s => s.id === district.state);
            selectionMap.set(`${district.state}_${district.id}`, {
                state: { id: state.id, name: state.name, code: state.code },
                district: { id: district.id, name: district.name, code: district.code, state: district.state }
            });
        }
    });

    selectedBlocks.value.forEach(blockId => {
        const block = availableBlocks.value.find(b => b.id === blockId);
        if (block) {
            const state = states.value.find(s => s.id === block.state);
            const district = availableDistricts.value.find(d => d.id === block.district);
            selectionMap.set(`${block.state}_${block.district}_${block.id}`, {
                state: { id: state.id, name: state.name, code: state.code },
                district: { id: district.id, name: district.name, code: district.code, state: district.state },
                block: { id: block.id, name: block.name, code: block.code, district: block.district, state: block.state }
            });
        }
    });

    selectedGramPanchayats.value.forEach(gpId => {
        const gp = availableGramPanchayats.value.find(g => g.id === gpId);
        if (gp) {
            const state = states.value.find(s => s.id === gp.state);
            const district = availableDistricts.value.find(d => d.id === gp.district);
            const block = availableBlocks.value.find(b => b.id === gp.block);
            selectionMap.set(`${gp.state}_${gp.district}_${gp.block}_${gp.id}`, {
                state: { id: state.id, name: state.name, code: state.code },
                district: { id: district.id, name: district.name, code: district.code, state: district.state },
                block: { id: block.id, name: block.name, code: block.code, district: block.district, state: block.state },
                gramPanchayat: { id: gp.id, name: gp.name, code: gp.code, block: gp.block, district: gp.district, state: gp.state }
            });
        }
    });

    selectedVillages.value.forEach(villageId => {
        const village = availableVillages.value.find(v => v.id === villageId);
        if (village) {
            const state = states.value.find(s => s.id === village.state);
            const district = availableDistricts.value.find(d => d.id === village.district);
            const block = availableBlocks.value.find(b => b.id === village.block);
            const gp = availableGramPanchayats.value.find(g => g.id === village.gram_panchayat);
            selectionMap.set(`${village.state}_${village.district}_${village.block}_${village.gram_panchayat}_${village.id}`, {
                state: { id: state.id, name: state.name, code: state.code },
                district: { id: district.id, name: district.name, code: district.code, state: district.state },
                block: { id: block.id, name: block.name, code: block.code, district: block.district, state: block.state },
                gramPanchayat: { id: gp.id, name: gp.name, code: gp.code, block: gp.block, district: gp.district, state: gp.state },
                village: { id: village.id, name: village.name, code: village.code, gram_panchayat: village.gram_panchayat, block: village.block, district: village.district, state: village.state }
            });
        }
    });
    let selection = Array.from(selectionMap.values());
    // Filter based on lowest hierarchy
    switch (lowest_hierarchy.value) {
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

    if (!props.disable_save_btn) {
        try {
            const r = await frappe.xcall('sva_frappe.api.save_geography_details', {
                selection_data: JSON.stringify(selection),
                document_type: props.frm.doctype,
                docname: props.frm.docname,
                lowest_hierarchy: lowest_hierarchy.value
            });

            if (r.status === 'success') {
                frappe.show_alert({ message: r.message, indicator: 'green' });
            } else {
                frappe.show_alert({ message: r.message || __('Error saving geography details'), indicator: 'red' });
            }
        } catch (error) {
            frappe.show_alert({ message: error.message || __('Error saving geography details'), indicator: 'red' });
        } finally {
            isSaving.value = false;
        }
    }

    if (props.hierarchy_level_field && props.frm.doc[props.hierarchy_level_field] && props.frm.docname && !props.disable_save_btn) {
        await frappe.db.set_value(props.frm.doctype, props.frm.docname, props.hierarchy_level_field, props.frm.doc[props.hierarchy_level_field]);
    }

    return selection;
};

// ============ GETTER METHODS ============
const getHierarchyDisplayName = (hierarchy) => {
    const displayNames = {
        'State': __('States'),
        'District': __('Districts'),
        'Block': __('Blocks'),
        'Gram Panchayat': __('Gram Panchayats'),
        'Village': __('Villages')
    };
    return displayNames[hierarchy] || hierarchy;
};

const getStateName = (stateId) => {
    const state = states.value.find(s => s.id === stateId);
    return state ? state.name : '';
};

const getDistrictsForState = (stateId) => districts[stateId] || [];
const getBlocksForDistrict = (districtId) => blocks[districtId] || [];
const getGramPanchayatsForBlock = (blockId) => gramPanchayats[blockId] || [];
const getVillagesForGP = (gpId) => villages[gpId] || [];

const getDistrictName = (districtId) => {
    const district = availableDistricts.value.find(d => d.id === districtId);
    return district ? district.name : '';
};

const getBlockName = (blockId) => {
    const block = availableBlocks.value.find(b => b.id === blockId);
    return block ? block.name : '';
};

const getGramPanchayatName = (gpId) => {
    const gp = availableGramPanchayats.value.find(g => g.id === gpId);
    return gp ? gp.name : '';
};

// ============ SELECTION HELPER METHODS ============
const getSelectedDistrictsForState = (stateId) => {
    return getDistrictsForState(stateId).filter(district =>
        selectedDistricts.value.includes(district.id)
    );
};

const getSelectedBlocksForDistrict = (districtId) => {
    return getBlocksForDistrict(districtId).filter(block =>
        selectedBlocks.value.includes(block.id)
    );
};

const getSelectedGramPanchayatsForBlock = (blockId) => {
    return getGramPanchayatsForBlock(blockId).filter(gp =>
        selectedGramPanchayats.value.includes(gp.id)
    );
};

const getSelectedVillagesForGP = (gpId) => {
    return getVillagesForGP(gpId).filter(village =>
        selectedVillages.value.includes(village.id)
    );
};

const getSelectedBlocksForStateRecursive = (stateId) => {
    const selectedBlocksRecursive = [];
    const selectedDistrictsForState = getSelectedDistrictsForState(stateId);
    selectedDistrictsForState.forEach(district => {
        const blocksForDistrict = getSelectedBlocksForDistrict(district.id);
        selectedBlocksRecursive.push(...blocksForDistrict);
    });
    return selectedBlocksRecursive;
};

const getSelectedGPsForStateRecursive = (stateId) => {
    const selectedGPs = [];
    const selectedBlocksForState = getSelectedBlocksForStateRecursive(stateId);
    selectedBlocksForState.forEach(block => {
        const gpsForBlock = getSelectedGramPanchayatsForBlock(block.id);
        selectedGPs.push(...gpsForBlock);
    });
    return selectedGPs;
};

// ============ TOGGLE/SELECTION METHODS ============
const toggleState = (stateId) => {
    if (props.read_only || isStatePreserved(stateId)) return;
    
    const index = selectedStates.value.indexOf(stateId);
    if (index > -1) {
        selectedStates.value.splice(index, 1);
        // Remove related non-preserved items
        const stateDistricts = getDistrictsForState(stateId);
        stateDistricts.forEach(district => {
            if (!isDistrictPreserved(district.id)) {
                const districtIndex = selectedDistricts.value.indexOf(district.id);
                if (districtIndex > -1) selectedDistricts.value.splice(districtIndex, 1);
            }
        });
    } else {
        selectedStates.value.push(stateId);
    }
    updateDistricts();
};

const toggleDistrict = (districtId) => {
    if (props.read_only || isDistrictPreserved(districtId)) return;
    
    const index = selectedDistricts.value.indexOf(districtId);
    if (index > -1) {
        selectedDistricts.value.splice(index, 1);
    } else {
        selectedDistricts.value.push(districtId);
    }
    updateBlocks();
};

const toggleBlock = (blockId) => {
    if (props.read_only || isBlockPreserved(blockId)) return;
    
    const index = selectedBlocks.value.indexOf(blockId);
    if (index > -1) {
        selectedBlocks.value.splice(index, 1);
    } else {
        selectedBlocks.value.push(blockId);
    }
    updateGramPanchayats();
};

const toggleGramPanchayat = (gpId) => {
    if (props.read_only || isGramPanchayatPreserved(gpId)) return;
    
    const index = selectedGramPanchayats.value.indexOf(gpId);
    if (index > -1) {
        selectedGramPanchayats.value.splice(index, 1);
    } else {
        selectedGramPanchayats.value.push(gpId);
    }
    updateVillages();
};

const toggleVillage = (villageId) => {
    if (props.read_only || isVillagePreserved(villageId)) return;
    
    const index = selectedVillages.value.indexOf(villageId);
    if (index > -1) {
        selectedVillages.value.splice(index, 1);
    } else {
        selectedVillages.value.push(villageId);
    }
};

const isAllDistrictsSelectedForState = (stateId) => {
    const stateDistricts = getDistrictsForState(stateId);
    return stateDistricts.length > 0 && stateDistricts.every(district =>
        selectedDistricts.value.includes(district.id)
    );
};

const toggleAllDistrictsForState = (stateId) => {
    const stateDistricts = getDistrictsForState(stateId);
    const allSelected = isAllDistrictsSelectedForState(stateId);

    if (allSelected) {
        const districtIds = stateDistricts.map(d => d.id);
        selectedDistricts.value = selectedDistricts.value.filter(id => !districtIds.includes(id));

        const blocksToRemove = availableBlocks.value
            .filter(block => districtIds.includes(block.district))
            .map(block => block.id);
        selectedBlocks.value = selectedBlocks.value.filter(id => !blocksToRemove.includes(id));

        const gpsToRemove = availableGramPanchayats.value
            .filter(gp => blocksToRemove.includes(gp.block))
            .map(gp => gp.id);
        selectedGramPanchayats.value = selectedGramPanchayats.value.filter(id => !gpsToRemove.includes(id));

        const villagesToRemove = availableVillages.value
            .filter(village => gpsToRemove.includes(village.gram_panchayat))
            .map(village => village.id);
        selectedVillages.value = selectedVillages.value.filter(id => !villagesToRemove.includes(id));
    } else {
        const districtIds = stateDistricts.map(d => d.id);
        selectedDistricts.value = [...new Set([...selectedDistricts.value, ...districtIds])];
    }
    updateBlocks();
};

const isAllBlocksSelectedForDistrict = (districtId) => {
    const districtBlocks = getBlocksForDistrict(districtId);
    return districtBlocks.length > 0 && districtBlocks.every(block =>
        selectedBlocks.value.includes(block.id)
    );
};

const toggleAllBlocksForDistrict = (districtId) => {
    const districtBlocks = getBlocksForDistrict(districtId);
    const allSelected = isAllBlocksSelectedForDistrict(districtId);

    if (allSelected) {
        const blockIds = districtBlocks.map(b => b.id);
        selectedBlocks.value = selectedBlocks.value.filter(id => !blockIds.includes(id));

        const gpsToRemove = availableGramPanchayats.value
            .filter(gp => blockIds.includes(gp.block))
            .map(gp => gp.id);
        selectedGramPanchayats.value = selectedGramPanchayats.value.filter(id => !gpsToRemove.includes(id));

        const villagesToRemove = availableVillages.value
            .filter(village => gpsToRemove.includes(village.gram_panchayat))
            .map(village => village.id);
        selectedVillages.value = selectedVillages.value.filter(id => !villagesToRemove.includes(id));
    } else {
        const blockIds = districtBlocks.map(b => b.id);
        selectedBlocks.value = [...new Set([...selectedBlocks.value, ...blockIds])];
    }
    updateGramPanchayats();
};

const isAllGramPanchayatsSelectedForBlock = (blockId) => {
    const blockGPs = getGramPanchayatsForBlock(blockId);
    return blockGPs.length > 0 && blockGPs.every(gp =>
        selectedGramPanchayats.value.includes(gp.id)
    );
};

const toggleAllGramPanchayatsForBlock = (blockId) => {
    const blockGPs = getGramPanchayatsForBlock(blockId);
    const allSelected = isAllGramPanchayatsSelectedForBlock(blockId);

    if (allSelected) {
        const gpIds = blockGPs.map(gp => gp.id);
        selectedGramPanchayats.value = selectedGramPanchayats.value.filter(id => !gpIds.includes(id));

        const villagesToRemove = availableVillages.value
            .filter(village => gpIds.includes(village.gram_panchayat))
            .map(village => village.id);
        selectedVillages.value = selectedVillages.value.filter(id => !villagesToRemove.includes(id));
    } else {
        const gpIds = blockGPs.map(gp => gp.id);
        selectedGramPanchayats.value = [...new Set([...selectedGramPanchayats.value, ...gpIds])];
    }
    updateVillages();
};

const isAllVillagesSelectedForGP = (gpId) => {
    const gpVillages = getVillagesForGP(gpId);
    return gpVillages.length > 0 && gpVillages.every(village =>
        selectedVillages.value.includes(village.id)
    );
};

const toggleAllVillagesForGP = (gpId) => {
    const gpVillages = getVillagesForGP(gpId);
    const allSelected = isAllVillagesSelectedForGP(gpId);

    if (allSelected) {
        const villageIds = gpVillages.map(v => v.id);
        selectedVillages.value = selectedVillages.value.filter(id => !villageIds.includes(id));
    } else {
        const villageIds = gpVillages.map(v => v.id);
        selectedVillages.value = [...new Set([...selectedVillages.value, ...villageIds])];
    }
};

const toggleAllStates = () => {
    if (allStatesSelected.value) {
        // Keep preserved states when unselecting all
        const preservedStateIds = Array.from(preserveData.value.states);
        selectedStates.value = preservedStateIds;
        selectedDistricts.value = selectedDistricts.value.filter(districtId => 
            preserveData.value.districts.has(districtId)
        );
        selectedBlocks.value = selectedBlocks.value.filter(blockId => 
            preserveData.value.blocks.has(blockId)
        );
        selectedGramPanchayats.value = selectedGramPanchayats.value.filter(gpId => 
            preserveData.value.gramPanchayats.has(gpId)
        );
        selectedVillages.value = selectedVillages.value.filter(villageId => 
            preserveData.value.villages.has(villageId)
        );
    } else {
        selectedStates.value = states.value.map(state => state.id);
    }
    updateDistricts();
};

const toggleAllDistricts = () => {
    if (allDistrictsSelected.value) {
        const preservedDistrictIds = Array.from(preserveData.value.districts);
        selectedDistricts.value = preservedDistrictIds;
        selectedBlocks.value = selectedBlocks.value.filter(blockId => 
            preserveData.value.blocks.has(blockId)
        );
        selectedGramPanchayats.value = selectedGramPanchayats.value.filter(gpId => 
            preserveData.value.gramPanchayats.has(gpId)
        );
        selectedVillages.value = selectedVillages.value.filter(villageId => 
            preserveData.value.villages.has(villageId)
        );
    } else {
        selectedDistricts.value = availableDistricts.value.map(district => district.id);
    }
    updateBlocks();
};

const toggleAllBlocks = () => {
    if (allBlocksSelected.value) {
        selectedBlocks.value = [];
        selectedGramPanchayats.value = [];
        selectedVillages.value = [];
    } else {
        selectedBlocks.value = availableBlocks.value.map(block => block.id);
    }
    updateGramPanchayats();
};

const toggleAllGramPanchayats = () => {
    if (allGramPanchayatsSelected.value) {
        selectedGramPanchayats.value = [];
        selectedVillages.value = [];
    } else {
        selectedGramPanchayats.value = availableGramPanchayats.value.map(gp => gp.id);
    }
    updateVillages();
};

const toggleAllVillages = () => {
    if (allVillagesSelected.value) {
        selectedVillages.value = [];
    } else {
        selectedVillages.value = availableVillages.value.map(village => village.id);
    }
};

// ============ EXPANSION METHODS ============
const toggleStateExpansion = (stateId) => {
    if (expandedStates.has(stateId)) {
        expandedStates.delete(stateId);
    } else {
        expandedStates.clear();
        expandedStates.add(stateId);
        expandedDistricts.clear();
        expandedBlocks.clear();
        expandedGPs.clear();
    }
};

const toggleDistrictExpansion = (districtId) => {
    if (expandedDistricts.has(districtId)) {
        expandedDistricts.delete(districtId);
    } else {
        expandedDistricts.clear();
        expandedDistricts.add(districtId);
        expandedBlocks.clear();
        expandedGPs.clear();
    }
};

const toggleBlockExpansion = (blockId) => {
    if (expandedBlocks.has(blockId)) {
        expandedBlocks.delete(blockId);
    } else {
        expandedBlocks.clear();
        expandedBlocks.add(blockId);
        expandedGPs.clear();
    }
};

const toggleGPExpansion = (gpId) => {
    if (expandedGPs.has(gpId)) {
        expandedGPs.delete(gpId);
    } else {
        expandedGPs.clear();
        expandedGPs.add(gpId);
    }
};

const isStateExpanded = (stateId) => expandedStates.has(stateId);
const isDistrictExpanded = (districtId) => expandedDistricts.has(districtId);
const isBlockExpanded = (blockId) => expandedBlocks.has(blockId);
const isGPExpanded = (gpId) => expandedGPs.has(gpId);

// ============ UTILITY METHODS ============
const updateAvailableItems = async () => {
    updateDistricts();
    if (lowest_hierarchy.value !== 'State') {
        updateBlocks();
        if (lowest_hierarchy.value !== 'District') {
            updateGramPanchayats();
            if (lowest_hierarchy.value !== 'Block') {
                updateVillages();
            }
        }
    }
};

const withLoading = (callback) => {
    isLoading.value = true;
    try {
        return callback();
    } finally {
        isLoading.value = false;
    }
};

const resetData = async () => {
    Object.keys(districts).forEach(key => delete districts[key]);
    Object.keys(blocks).forEach(key => delete blocks[key]);
    Object.keys(gramPanchayats).forEach(key => delete gramPanchayats[key]);
    Object.keys(villages).forEach(key => delete villages[key]);
    selectedStates.value = [];
    selectedDistricts.value = [];
    selectedBlocks.value = [];
    selectedGramPanchayats.value = [];
    selectedVillages.value = [];
    availableDistricts.value = [];
    availableBlocks.value = [];
    availableGramPanchayats.value = [];
    availableVillages.value = [];
    isDataLoaded.value = false;
    expandedStates.clear();
    expandedDistricts.clear();
    expandedBlocks.clear();
    expandedGPs.clear();
};

const getLightColor = (color) => {
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);
    const lightR = Math.min(r + 40, 255);
    const lightG = Math.min(g + 40, 255);
    const lightB = Math.min(b + 40, 255);
    return `rgb(${lightR}, ${lightG}, ${lightB})`;
};

// ============ PRESERVE DATA HELPER METHODS ============
const isStatePreserved = (stateId) => preserveData.value.states.has(stateId);
const isDistrictPreserved = (districtId) => preserveData.value.districts.has(districtId);
const isBlockPreserved = (blockId) => preserveData.value.blocks.has(blockId);
const isGramPanchayatPreserved = (gpId) => preserveData.value.gramPanchayats.has(gpId);
const isVillagePreserved = (villageId) => preserveData.value.villages.has(villageId);

// ============ GETTER METHODS FOR RELATED DATA ============
const getDistrictState = (districtId) => {
    const district = availableDistricts.value.find(d => d.id === districtId);
    return district ? district.state : '';
};

const getBlockState = (blockId) => {
    const block = availableBlocks.value.find(b => b.id === blockId);
    return block ? block.state : '';
};

const getBlockDistrict = (blockId) => {
    const block = availableBlocks.value.find(b => b.id === blockId);
    return block ? block.district : '';
};

const getGPState = (gpId) => {
    const gp = availableGramPanchayats.value.find(g => g.id === gpId);
    return gp ? gp.state : '';
};

const getGPDistrict = (gpId) => {
    const gp = availableGramPanchayats.value.find(g => g.id === gpId);
    return gp ? gp.district : '';
};

const getGPBlock = (gpId) => {
    const gp = availableGramPanchayats.value.find(g => g.id === gpId);
    return gp ? gp.block : '';
};

// ============ VALIDATION METHODS ============
const validateCurrentStepSelection = () => {
    const validation = { isValid: true, message: '', missingItems: [] };

    switch (currentStep.value) {
        case 1:
            if (selectedStates.value.length === 0) {
                validation.isValid = false;
                validation.message = 'Please select at least one state to continue.';
            }
            break;

        case 2:
            if (lowest_hierarchy.value === 'State') break;
            const statesWithoutDistricts = [];
            selectedStates.value.forEach(stateId => {
                const stateName = getStateName(stateId);
                const districtsForState = getDistrictsForState(stateId);
                const selectedDistrictsForState = districtsForState.filter(d =>
                    selectedDistricts.value.includes(d.id)
                );
                if (selectedDistrictsForState.length === 0) {
                    statesWithoutDistricts.push(stateName);
                }
            });
            if (statesWithoutDistricts.length > 0) {
                validation.isValid = false;
                validation.missingItems = statesWithoutDistricts;
                validation.message = statesWithoutDistricts.length === 1
                    ? `Please select ${__("Districts").toLowerCase()} in ${statesWithoutDistricts[0]}.`
                    : `Please select ${__("Districts").toLowerCase()} all ${__("States").toLowerCase()}.`;
            }
            break;

        case 3:
            if (['State', 'District'].includes(lowest_hierarchy.value)) break;
            const districtsWithoutBlocks = [];
            selectedDistricts.value.forEach(districtId => {
                const district = availableDistricts.value.find(d => d.id === districtId);
                if (!district) return;
                const blocksForDistrict = getBlocksForDistrict(districtId);
                const selectedBlocksForDistrict = blocksForDistrict.filter(b =>
                    selectedBlocks.value.includes(b.id)
                );
                if (selectedBlocksForDistrict.length === 0) {
                    districtsWithoutBlocks.push(district.name);
                }
            });
            if (districtsWithoutBlocks.length > 0) {
                validation.isValid = false;
                validation.missingItems = districtsWithoutBlocks;
                validation.message = districtsWithoutBlocks.length === 1
                    ? `Please select ${__("Blocks").toLowerCase()} in ${districtsWithoutBlocks[0]}.`
                    : `Please select ${__("Blocks").toLowerCase()} all ${__("Districts").toLowerCase()}.`;
            }
            break;

        case 4:
            if (['State', 'District', 'Block'].includes(lowest_hierarchy.value)) break;
            const blocksWithoutGPs = [];
            selectedBlocks.value.forEach(blockId => {
                const block = availableBlocks.value.find(b => b.id === blockId);
                if (!block) return;
                const gpsForBlock = getGramPanchayatsForBlock(blockId);
                const selectedGPsForBlock = gpsForBlock.filter(gp =>
                    selectedGramPanchayats.value.includes(gp.id)
                );
                if (selectedGPsForBlock.length === 0) {
                    blocksWithoutGPs.push(block.name);
                }
            });
            if (blocksWithoutGPs.length > 0) {
                validation.isValid = false;
                validation.missingItems = blocksWithoutGPs;
                validation.message = blocksWithoutGPs.length === 1
                    ? `Please select ${__("Gram Panchayats").toLowerCase()} in ${blocksWithoutGPs[0]}.`
                    : `Please select ${__("Gram Panchayats").toLowerCase()} all ${__("Blocks").toLowerCase()}.`;
            }
            break;

        case 5:
            if (lowest_hierarchy.value !== 'Village') break;
            const gpsWithoutVillages = [];
            selectedGramPanchayats.value.forEach(gpId => {
                const gp = availableGramPanchayats.value.find(g => g.id === gpId);
                if (!gp) return;
                const villagesForGP = getVillagesForGP(gpId);
                const selectedVillagesForGP = villagesForGP.filter(village =>
                    selectedVillages.value.includes(village.id)
                );
                if (selectedVillagesForGP.length === 0) {
                    gpsWithoutVillages.push(gp.name);
                }
            });
            if (gpsWithoutVillages.length > 0) {
                validation.isValid = false;
                validation.missingItems = gpsWithoutVillages;
                validation.message = gpsWithoutVillages.length === 1
                    ? `Please select ${__("Villages").toLowerCase()} in ${gpsWithoutVillages[0]}.`
                    : `Please select ${__("Villages").toLowerCase()} all ${__("Gram Panchayats").toLowerCase()}.`;
            }
            break;
    }
    return validation;
};

const validateAllLevelsForSave = () => {
    const validation = { isValid: true, message: '', missingItems: [] };

    if (selectedStates.value.length === 0) {
        validation.isValid = false;
        validation.message = 'Please select at least one state to save.';
        return validation;
    }

    if (['District', 'Block', 'Gram Panchayat', 'Village'].includes(lowest_hierarchy.value)) {
        const statesWithoutDistricts = [];
        selectedStates.value.forEach(stateId => {
            const stateName = getStateName(stateId);
            const districtsForState = getDistrictsForState(stateId);
            const selectedDistrictsForState = districtsForState.filter(d =>
                selectedDistricts.value.includes(d.id)
            );
            if (selectedDistrictsForState.length === 0) {
                statesWithoutDistricts.push(stateName);
            }
        });
        if (statesWithoutDistricts.length > 0) {
            validation.isValid = false;
            validation.missingItems = statesWithoutDistricts;
            validation.message = statesWithoutDistricts.length === 1
                ? `Please select ${__("Districts").toLowerCase()} in ${statesWithoutDistricts[0]}.`
                : `Please select ${__("Districts").toLowerCase()} all ${__("States").toLowerCase()}.`;
            return validation;
        }
    }

    if (['Block', 'Gram Panchayat', 'Village'].includes(lowest_hierarchy.value)) {
        const districtsWithoutBlocks = [];
        selectedDistricts.value.forEach(districtId => {
            const district = availableDistricts.value.find(d => d.id === districtId);
            if (!district) return;
            const blocksForDistrict = getBlocksForDistrict(districtId);
            const selectedBlocksForDistrict = blocksForDistrict.filter(b =>
                selectedBlocks.value.includes(b.id)
            );
            if (selectedBlocksForDistrict.length === 0) {
                districtsWithoutBlocks.push(district.name);
            }
        });
        if (districtsWithoutBlocks.length > 0) {
            validation.isValid = false;
            validation.missingItems = districtsWithoutBlocks;
            validation.message = districtsWithoutBlocks.length === 1
                ? `Please select ${__("Blocks").toLowerCase()} in ${districtsWithoutBlocks[0]}.`
                : `Please select ${__("Blocks").toLowerCase()} all ${__("Districts").toLowerCase()}.`;
            return validation;
        }
    }

    if (['Gram Panchayat', 'Village'].includes(lowest_hierarchy.value)) {
        const blocksWithoutGPs = [];
        selectedBlocks.value.forEach(blockId => {
            const block = availableBlocks.value.find(b => b.id === blockId);
            if (!block) return;
            const gpsForBlock = getGramPanchayatsForBlock(blockId);
            const selectedGPsForBlock = gpsForBlock.filter(gp =>
                selectedGramPanchayats.value.includes(gp.id)
            );
            if (selectedGPsForBlock.length === 0) {
                blocksWithoutGPs.push(block.name);
            }
        });
        if (blocksWithoutGPs.length > 0) {
            validation.isValid = false;
            validation.missingItems = blocksWithoutGPs;
            validation.message = blocksWithoutGPs.length === 1
                ? `Please select ${__("Gram Panchayats").toLowerCase()} in ${blocksWithoutGPs[0]}.`
                : `Please select ${__("Gram Panchayats").toLowerCase()} all ${__("Blocks").toLowerCase()}.`;
            return validation;
        }
    }

    if (lowest_hierarchy.value === 'Village') {
        const gpsWithoutVillages = [];
        selectedGramPanchayats.value.forEach(gpId => {
            const gp = availableGramPanchayats.value.find(g => g.id === gpId);
            if (!gp) return;
            const villagesForGP = getVillagesForGP(gpId);
            const selectedVillagesForGP = villagesForGP.filter(village =>
                selectedVillages.value.includes(village.id)
            );
            if (selectedVillagesForGP.length === 0) {
                gpsWithoutVillages.push(gp.name);
            }
        });
        if (gpsWithoutVillages.length > 0) {
            validation.isValid = false;
            validation.missingItems = gpsWithoutVillages;
            validation.message = gpsWithoutVillages.length === 1
                ? `Please select ${__("Villages").toLowerCase()} in ${gpsWithoutVillages[0]}.`
                : `Please select ${__("Villages").toLowerCase()} all ${__("Gram Panchayats").toLowerCase()}.`;
            return validation;
        }
    }

    return validation;
};

const showValidationError = (validationResult) => {
    const { message, missingItems } = validationResult;
    let errorHtml = `
        <div style="text-align: left; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <div style="display: flex; align-items: flex-start; gap: 10px; padding: 15px; background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;">
                <span style="color: #e17055; font-size: 20px; flex-shrink: 0;">⚠️</span>
                <div style="flex: 1;">
                    <p style="margin: 0; font-size: 14px; color: #6c5700; line-height: 1.4;">
                        <strong>Selection Required:</strong> ${message}
                    </p>`;

    if (missingItems && missingItems.length > 1) {
        errorHtml += `
            <div style="margin-top: 10px; padding: 8px; background-color: #fff; border: 1px solid #ffeaa7; border-radius: 3px;">
                <div style="font-size: 12px; color: #6c5700; font-weight: 500; margin-bottom: 5px;">
                    Missing selections in:
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 5px;">`;

        missingItems.forEach(item => {
            errorHtml += `
                <span style="background-color: #ffeaa7; color: #6c5700; padding: 2px 6px; border-radius: 2px; font-size: 11px; font-weight: 500;">
                    ${item}
                </span>`;
        });

        errorHtml += `</div></div>`;
    }

    errorHtml += `</div></div></div>`;

    frappe.msgprint({
        title: __('Selection Required'),
        message: errorHtml,
        indicator: 'orange'
    });
};

// ============ LIFECYCLE & INITIALIZATION ============
const initializeComponent = async () => {
    doctype.value = props.frm.doctype;
    if (isDataLoaded.value) return;

    if (props.frm.doctype && props.frm.docname) {
        await loadExistingData();
    } else {
        await loadDefaultLowestHierarchy();
        await loadStates();
    }

    if (states.value.length > 0) {
        expandedStates.add(states.value[0].id);
    }
    isDataLoaded.value = true;
    expandTreeBasedOnStep();
};

onMounted(() => {
    loadDefaultLowestHierarchy();
    initializeComponent();
});

// ============ EXPOSE VALUES FOR TEMPLATE ACCESS ============
defineExpose({
    // Reactive state
    currentStep, states, districts, blocks, gramPanchayats, villages,
    selectedStates, selectedDistricts, selectedBlocks, selectedGramPanchayats, selectedVillages,
    availableDistricts, availableBlocks, availableGramPanchayats, availableVillages,
    isLoading, expandedStateId, current_docname, lowest_hierarchy, isDataLoaded,
    expandedStates, expandedDistricts, expandedBlocks, expandedGPs, doctype, isSaving,

    // Computed properties
    totalSteps, themeColors, isAtLowestHierarchy,
    allStatesSelected, allDistrictsSelected, allBlocksSelected,
    allGramPanchayatsSelected, allVillagesSelected,

    // Core methods
    loadDefaultLowestHierarchy, loadExistingData, loadStates,
    updateDistricts, updateBlocks, updateGramPanchayats, updateVillages,
    expandTreeBasedOnStep, goNext, goBack, saveSelection,

    // Preserve data helper methods
    isStatePreserved, isDistrictPreserved, isBlockPreserved, 
    isGramPanchayatPreserved, isVillagePreserved,

    // Getter methods
    getHierarchyDisplayName, getStateName, getDistrictName, getBlockName, getGramPanchayatName,
    getDistrictsForState, getBlocksForDistrict, getGramPanchayatsForBlock, getVillagesForGP,
    getSelectedDistrictsForState, getSelectedBlocksForDistrict,
    getSelectedGramPanchayatsForBlock, getSelectedVillagesForGP,
    getSelectedBlocksForStateRecursive, getSelectedGPsForStateRecursive,
    getDistrictState, getBlockState, getBlockDistrict, getGPState, getGPDistrict, getGPBlock,

    // Toggle/Selection methods  
    toggleState, toggleDistrict, toggleBlock, toggleGramPanchayat, toggleVillage,
    isAllDistrictsSelectedForState, toggleAllDistrictsForState,
    isAllBlocksSelectedForDistrict, toggleAllBlocksForDistrict,
    isAllGramPanchayatsSelectedForBlock, toggleAllGramPanchayatsForBlock,
    isAllVillagesSelectedForGP, toggleAllVillagesForGP,
    toggleAllStates, toggleAllDistricts, toggleAllBlocks, toggleAllGramPanchayats, toggleAllVillages,

    // Expansion methods
    toggleStateExpansion, toggleDistrictExpansion, toggleBlockExpansion, toggleGPExpansion,
    isStateExpanded, isDistrictExpanded, isBlockExpanded, isGPExpanded,

    // Utility methods
    updateAvailableItems, withLoading, resetData, getLightColor,

    // Validation methods
    validateCurrentStepSelection, validateAllLevelsForSave, showValidationError
});
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

/* Standardized Form Check Styles */
.form-check {
    display: flex;
    align-items: flex-start;
    padding-left: 0;
    margin-bottom: 0;
}

.form-check-input {
    margin-left: 0;
    margin-top: 2px;
    margin-right: 8px;
    flex-shrink: 0;
    cursor: pointer;
}

.form-check-label {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
    line-height: 1.4;
    margin-bottom: 0;
    cursor: pointer;
    user-select: none;
}

.form-check-label:hover {
    color: v-bind('themeColors.primary');
}

/* Disabled state styling */
.form-check-input:disabled {
    cursor: not-allowed;
}

.form-check-input:disabled+.form-check-label {
    color: var(--text-muted);
    cursor: not-allowed;
}

.form-check-input:disabled+.form-check-label:hover {
    color: var(--text-muted);
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

/* Tree Labels */
.tree-label {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    letter-spacing: 0.02em;
    color: var(--text-color);
}

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