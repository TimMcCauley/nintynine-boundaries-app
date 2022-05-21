export const isIterable = (obj) => {
    if (obj == null) {
        return false;
    }
    return typeof obj[Symbol.iterator] === "function";
};

export const getOverpassQuery = (adminLevel, alpha2) => {
    return `[out:json];
    relation["boundary"="administrative"]["admin_level"="2"]["ISO3166-1"=${alpha2}];
    (._;>;);
    out;`;
}

export const getOverpassQueryLandOnly = (adminLevel, alpha2) => {
    return `[timeout:600][out:json];
    area["ISO3166-1"="${alpha2}"]->.country;
    rel["ISO3166-1"="${alpha2}"]["type"="boundary"]["admin_level"="2"];
    (
        way(r)["maritime" != "yes"];
        way(area.country)["natural"="coastline"];
    );
    (._;>;);
    out;`
}