<script>
    import { onMount, onDestroy } from "svelte";
    import { createGrid, ModuleRegistry, AllCommunityModule, themeQuartz } from "ag-grid-community";

    if (typeof window !== 'undefined') {
        ModuleRegistry.registerModules([AllCommunityModule]);
    }

    let {
        columnDefs = [],
        rowData = [],
        defaultColDef = {},
        onGridReady = null,
        pagination = false,
        paginationPageSize = 10,
        paginationPageSizeSelector = [10, 20, 50],
        enableCellTextSelection = false
    } = $props();

    let gridDiv = $state();
    let gridApi = $state();

    onMount(() => {
        const gridOptions = {
            columnDefs,
            rowData,
            defaultColDef,
            pagination,
            paginationPageSize,
            paginationPageSizeSelector,
            enableCellTextSelection,
            theme: themeQuartz,
            onGridReady: (params) => {
                gridApi = params.api;
                if (onGridReady) {
                    onGridReady(params);
                }
            }
        };

        createGrid(gridDiv, gridOptions);
    });

    onDestroy(() => {
        if (gridApi) {
            gridApi.destroy();
        }
    });

    $effect(() => {
        if (gridApi) {
            gridApi.setGridOption('rowData', rowData);
        }
    });
</script>

<div bind:this={gridDiv} style="width: 100%; height: 100%;"></div>
