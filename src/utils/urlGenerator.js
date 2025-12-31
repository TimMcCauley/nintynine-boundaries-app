/**
 * Utility functions to generate download and OSM URLs dynamically
 * from minimal boundary data.
 */

const FILES_BASE_URL = import.meta.env.VITE_FILES_BASE_URL || 'https://files.99boundaries.com';
const OSM_BASE_URL = import.meta.env.VITE_OSM_BASE_URL || 'https://www.openstreetmap.org';

/**
 * Generate the base path for a boundary file
 * @param {string} isoCode - ISO country code (e.g., "AD", "US")
 * @param {number} adminLevel - Admin level (e.g., 2, 4, 6)
 * @param {string} relationId - OSM relation ID
 * @param {string} slug - URL-friendly name slug
 * @returns {string} Base path
 */
function getBasePath(isoCode, adminLevel, relationId, slug) {
    const folderName = `relation_${relationId}_${slug}`;
    return `${FILES_BASE_URL}/${isoCode}/${adminLevel}/${folderName}/${folderName}`;
}

/**
 * Generate GeoJSON download link
 * @param {Object} boundary - Boundary data object
 * @returns {string|null} GeoJSON download URL or null if not available
 */
export function getGeoJsonLink(boundary) {
    if (!boundary.has_geojson) return null;
    const { iso_code, admin_level, relation_id, slug, type } = boundary;
    const basePath = getBasePath(iso_code, admin_level, relation_id, slug);
    const landSuffix = type === 'l' ? '_land' : '';
    return `${basePath}${landSuffix}.geojson.zip`;
}

/**
 * Generate Shapefile download link
 * @param {Object} boundary - Boundary data object
 * @returns {string|null} Shapefile download URL or null if not available
 */
export function getShpLink(boundary) {
    if (!boundary.has_shp) return null;
    const { iso_code, admin_level, relation_id, slug, type } = boundary;
    const basePath = getBasePath(iso_code, admin_level, relation_id, slug);
    const landSuffix = type === 'l' ? '_land' : '';
    return `${basePath}${landSuffix}.shp.zip`;
}

/**
 * Generate GeoPackage download link
 * @param {Object} boundary - Boundary data object
 * @returns {string|null} GeoPackage download URL or null if not available
 */
export function getGpkgLink(boundary) {
    if (!boundary.has_gpkg) return null;
    const { iso_code, admin_level, relation_id, slug, type } = boundary;
    const basePath = getBasePath(iso_code, admin_level, relation_id, slug);
    const landSuffix = type === 'l' ? '_land' : '';
    return `${basePath}${landSuffix}.gpkg.zip`;
}

/**
 * Generate MapInfo download link
 * @param {Object} boundary - Boundary data object
 * @returns {string|null} MapInfo download URL or null if not available
 */
export function getMapInfoLink(boundary) {
    if (!boundary.has_mapinfo) return null;
    const { iso_code, admin_level, relation_id, slug, type } = boundary;
    const basePath = getBasePath(iso_code, admin_level, relation_id, slug);
    const landSuffix = type === 'l' ? '_land' : '';
    return `${basePath}${landSuffix}.tab.zip`;
}

/**
 * Generate OSM relation link
 * @param {Object} boundary - Boundary data object
 * @returns {string} OSM relation URL
 */
export function getOsmRelationLink(boundary) {
    const { relation_id } = boundary;
    return `${OSM_BASE_URL}/relation/${relation_id}`;
}

/**
 * Enhance a boundary object with all generated URLs
 * @param {Object} boundary - Minimal boundary data object
 * @returns {Object} Boundary object with all URLs added
 */
export function enhanceBoundaryWithUrls(boundary) {
    return {
        ...boundary,
        // Expand 'type' to 'polygon_type' for backward compatibility
        polygon_type: boundary.type === 'l' ? 'land' : 'maritime',
        geojson_dl_link: getGeoJsonLink(boundary),
        shp_dl_link: getShpLink(boundary),
        geopackage_dl_link: getGpkgLink(boundary),
        mapinfo_dl_link: getMapInfoLink(boundary),
        osm_relation_link_id: getOsmRelationLink(boundary)
    };
}
