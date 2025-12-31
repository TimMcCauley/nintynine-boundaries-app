<script>
    import AgGrid from "./components/AgGrid.svelte";

    import Fa from "svelte-fa";
    import { faGithub } from "@fortawesome/free-brands-svg-icons";
    import { faGlobe } from "@fortawesome/free-solid-svg-icons";

    import boundariesDataRaw from "./boundary_catalog.json";
    import { enhanceBoundaryWithUrls } from "./utils/urlGenerator.js";
    import Select from "svelte-select";

    // Enhance boundary data with generated URLs
    const boundariesData = boundariesDataRaw.map(enhanceBoundaryWithUrls);

    let gridApi = $state();

    const uniqueParents = [...new Set(boundariesDataRaw.map(item => item.parent))].sort();
    const uniqueIsoCodes = [...new Set(boundariesDataRaw.map(item => item.iso_code))].sort();
    const uniqueAdminLevels = [...new Set(boundariesDataRaw.map(item => item.admin_level))].sort();
    // Map 'l' and 'm' to full names for unique values
    const uniquePolygonTypes = [...new Set(boundariesDataRaw.map(item => item.type === 'l' ? 'land' : 'maritime'))].sort();

    let selectedParents = $state([]);
    let selectedIsoCodes = $state([]);
    let selectedAdminLevels = $state([]);
    let selectedPolygonTypes = $state([]);

    let filteredData = $derived(boundariesData.filter(item => {
        if (selectedParents && selectedParents.length > 0 && !selectedParents.some(p => p && p.value === item.parent)) return false;
        if (selectedIsoCodes && selectedIsoCodes.length > 0 && !selectedIsoCodes.some(iso => iso && iso.value === item.iso_code)) return false;
        if (selectedAdminLevels && selectedAdminLevels.length > 0 && !selectedAdminLevels.some(al => al && al.value === item.admin_level)) return false;
        if (selectedPolygonTypes && selectedPolygonTypes.length > 0 && !selectedPolygonTypes.some(pt => pt && pt.value === item.polygon_type)) return false;
        return true;
    }));

    const flagCellRenderer = (params) => {
        const alpha2Lower = params.data.iso_code.toLowerCase();
        return `<span class="fi fi-${alpha2Lower}" style="filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));"></span>`;
    };

    const downloadLinkRenderer = (params) => {
        const url = params.value;
        // If URL is null or empty, don't render anything
        if (!url) {
            return '<span class="text-gray-400 text-xs">—</span>';
        }
        return `<a href="${url}" target="_blank" class="btn btn-xs btn-info btn-outline">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="w-3 h-3" fill="currentColor">
                <path d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 242.7-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7 288 32zM64 352c-35.3 0-64 28.7-64 64l0 32c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-32c0-35.3-28.7-64-64-64l-101.5 0-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352 64 352zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/>
            </svg>
        </a>`;
    };

    const adminLevelRenderer = (params) => {
        const level = params.value;
        const badgeColors = {
            2: 'badge-primary',
            3: 'badge-secondary',
            4: 'badge-accent',
            5: 'badge-info',
            6: 'badge-success'
        };
        const colorClass = badgeColors[level] || 'badge-neutral';
        return `<span class="badge ${colorClass}">${level}</span>`;
    };

    const osmLinkRenderer = (params) => {
        const url = params.value;
        const match = url.match(/relation\/(\d+)/);
        const relationId = match ? match[1] : 'View';
        return `<a href="${url}" target="_blank" class="btn btn-xs btn-info btn-outline">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="w-3 h-3" fill="currentColor">
                <path d="M352 256c0 22.2-1.2 43.6-3.3 64l-185.3 0c-2.2-20.4-3.3-41.8-3.3-64s1.2-43.6 3.3-64l185.3 0c2.2 20.4 3.3 41.8 3.3 64zm28.8-64l123.1 0c5.3 20.5 8.1 41.9 8.1 64s-2.8 43.5-8.1 64l-123.1 0c2.1-20.6 3.2-42 3.2-64s-1.1-43.4-3.2-64zm112.6-32l-116.7 0c-10-63.9-29.8-117.4-55.3-151.6c78.3 20.7 142 77.5 171.9 151.6zm-149.1 0l-176.6 0c6.1-36.4 15.5-68.6 27-94.7c10.5-23.6 22.2-40.7 33.5-51.5C239.4 3.2 248.7 0 256 0s16.6 3.2 27.8 13.8c11.3 10.8 23 27.9 33.5 51.5c11.6 26 20.9 58.2 27 94.7zm-209 0L18.6 160C48.6 85.9 112.2 29.1 190.6 8.4C165.1 42.6 145.3 96.1 135.3 160zM8.1 192l123.1 0c-2.1 20.6-3.2 42-3.2 64s1.1 43.4 3.2 64L8.1 320C2.8 299.5 0 278.1 0 256s2.8-43.5 8.1-64zM194.7 446.6c-11.6-26-20.9-58.2-27-94.6l176.6 0c-6.1 36.4-15.5 68.6-27 94.6c-10.5 23.6-22.2 40.7-33.5 51.5C272.6 508.8 263.3 512 256 512s-16.6-3.2-27.8-13.8c-11.3-10.8-23-27.9-33.5-51.5zM135.3 352c10 63.9 29.8 117.4 55.3 151.6C112.2 482.9 48.6 426.1 18.6 352l116.7 0zm358.1 0c-30 74.1-93.6 130.9-171.9 151.6c25.5-34.2 45.2-87.7 55.3-151.6l116.7 0z"/>
            </svg>
            ${relationId}
        </a>`;
    };

    const columnDefs = [
        {
            field: 'iso_code',
            headerName: '',
            width: 60,
            cellRenderer: flagCellRenderer,
            filter: false,
            sortable: false,
            pinned: 'left'
        },
        {
            field: 'name',
            headerName: 'Name',
            width: 250,
            pinned: 'left',
            filter: 'agTextColumnFilter'
        },
        {
            field: 'parent',
            headerName: 'Country',
            width: 200
        },
        {
            field: 'iso_code',
            headerName: 'ISO Code',
            width: 110
        },
        {
            field: 'admin_level',
            headerName: 'Admin Level',
            width: 130,
            cellRenderer: adminLevelRenderer
        },
        {
            field: 'polygon_type',
            headerName: 'Polygon Type',
            width: 140,
            cellStyle: params => {
                if (params.value === 'maritime') {
                    return { color: '#0891b2', fontWeight: '500' };
                } else if (params.value === 'land') {
                    return { color: '#16a34a', fontWeight: '500' };
                }
                return null;
            }
        },
        {
            field: 'geojson_dl_link',
            headerName: 'GeoJSON',
            width: 110,
            cellRenderer: downloadLinkRenderer,
            filter: false,
            sortable: false
        },
        {
            field: 'shp_dl_link',
            headerName: 'Shapefile',
            width: 110,
            cellRenderer: downloadLinkRenderer,
            filter: false,
            sortable: false
        },
        {
            field: 'mapinfo_dl_link',
            headerName: 'MapInfo',
            width: 110,
            cellRenderer: downloadLinkRenderer,
            filter: false,
            sortable: false
        },
        {
            field: 'geopackage_dl_link',
            headerName: 'GeoPackage',
            width: 110,
            cellRenderer: downloadLinkRenderer,
            filter: false,
            sortable: false
        },
        {
            field: 'osm_relation_link_id',
            headerName: 'OSM Relation',
            width: 130,
            cellRenderer: osmLinkRenderer,
            filter: false,
            sortable: false
        }
    ];

    const defaultColDef = {
        sortable: true,
        resizable: true
    };

    const onGridReady = (params) => {
        gridApi = params.api;
    };
</script>

<main class="container mx-auto px-4 h-screen flex flex-col">
        <div class="content flex flex-col flex-1 overflow-hidden">

        <div class="mb-6 flex-none">
            <div class="flex items-center justify-between mb-4">
                <a href="https://99boundaries.com">
                    <img src="logo.png" width="120" alt="logo" height="auto" />
                </a>
                <div class="flex gap-2">
                    <a
                        class="btn btn-primary btn-sm"
                        target="_blank"
                        href="https://overpass-turbo.eu/"
                    >
                        <Fa icon={faGlobe} />
                        <span><strong>Overpass Turbo</strong></span>
                    </a>
                    <a
                        class="btn btn-neutral btn-sm"
                        target="_blank"
                        href="https://github.com/TimMcCauley/nintynine-boundaries/"
                    >
                        <Fa icon={faGithub} />
                        <span><strong>GitHub</strong></span>
                    </a>
                </div>
            </div>

            <div class="mb-4">
                <div>
                    <span>
                        Boundaries are generated via <strong
                            ><a href="http://overpass-api.de/" target="_blank" class="link"
                                >Overpass</a
                            ></strong
                        >
                        &
                        <strong
                            ><a
                                href="https://osmdata.openstreetmap.de/data/land-polygons.html"
                                target="_blank"
                                class="link">OSM Land Polygons</a
                            ></strong
                        >
                        <a
                            href="https://www.openstreetmap.org/copyright"
                            rel="nofollow"
                            class="link">[© OpenStreetMap contributors]</a
                        >
                        and provided in <a href="https://epsg.io/4326" class="link"
                            >EPSG:4326</a
                        >.
                    </span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                <div class="form-control">
                    <div class="label py-1">
                        <span class="label-text text-sm font-semibold">Parent Country</span>
                    </div>
                    <Select
                        items={uniqueParents.map(p => ({ value: p, label: p }))}
                        bind:value={selectedParents}
                        multiple={true}
                        placeholder="Filter by parent..."
                        clearable={true}
                        --border-radius="0.5rem"
                        --height="2.5rem"
                        --font-size="0.875rem"
                        --padding="0.25rem 0.5rem"
                        --multi-item-height="1.5rem"
                        --list-background="white"
                        --list-z-index="1000"
                    />
                </div>

                <div class="form-control">
                    <div class="label py-1">
                        <span class="label-text text-sm font-semibold">ISO Code</span>
                    </div>
                    <Select
                        items={uniqueIsoCodes.map(iso => ({ value: iso, label: iso }))}
                        bind:value={selectedIsoCodes}
                        multiple={true}
                        placeholder="Filter by ISO code..."
                        clearable={true}
                        --border-radius="0.5rem"
                        --height="2.5rem"
                        --font-size="0.875rem"
                        --padding="0.25rem 0.5rem"
                        --multi-item-height="1.5rem"
                        --list-background="white"
                        --list-z-index="1000"
                    />
                </div>

                <div class="form-control">
                    <div class="label py-1">
                        <span class="label-text text-sm font-semibold">Admin Level</span>
                    </div>
                    <Select
                        items={uniqueAdminLevels.map(al => ({ value: al, label: `Level ${al}` }))}
                        bind:value={selectedAdminLevels}
                        multiple={true}
                        placeholder="Filter by admin level..."
                        clearable={true}
                        --border-radius="0.5rem"
                        --height="2.5rem"
                        --font-size="0.875rem"
                        --padding="0.25rem 0.5rem"
                        --multi-item-height="1.5rem"
                        --list-background="white"
                        --list-z-index="1000"
                    />
                </div>

                <div class="form-control">
                    <div class="label py-1">
                        <span class="label-text text-sm font-semibold">Polygon Type</span>
                    </div>
                    <Select
                        items={uniquePolygonTypes.map(pt => ({ value: pt, label: pt.charAt(0).toUpperCase() + pt.slice(1) }))}
                        bind:value={selectedPolygonTypes}
                        multiple={true}
                        placeholder="Filter by polygon type..."
                        clearable={true}
                        --border-radius="0.5rem"
                        --height="2.5rem"
                        --font-size="0.875rem"
                        --padding="0.25rem 0.5rem"
                        --multi-item-height="1.5rem"
                        --list-background="white"
                        --list-z-index="1000"
                    />
                </div>
            </div>
        </div>

        <div class="flex-1 w-full overflow-hidden">
            <AgGrid
                {columnDefs}
                rowData={filteredData}
                {defaultColDef}
                {onGridReady}
                pagination={true}
                paginationPageSize={20}
                paginationPageSizeSelector={[10, 20, 50, 100]}
                enableCellTextSelection={true}
            />
        </div>
    </div>
</main>
