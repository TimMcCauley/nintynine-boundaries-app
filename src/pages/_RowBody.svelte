<script>
    import { Button } from "svelma";
    import CopyToClipboard from "svelte-copy-to-clipboard";

    import { getOverpassQuery, getOverpassQueryLandOnly } from "../utils.js";
    export let country;
    export let adminLevel;
    export let landOnly;

    const alpha2Lower = country["alpha-2"].toLowerCase();
    const alpha2 = country["alpha-2"];
    const countryCode = country["country-code"];
    const baseUrl = "https://files.99boundaries.com";
    const basePath = adminLevel + "/" + alpha2;

    let baseFileName = alpha2 + "_" + adminLevel;
    let overpassQuery;
    if (landOnly) {
        baseFileName += "_land";
        overpassQuery = getOverpassQueryLandOnly(2, alpha2);
    } else {
        overpassQuery = getOverpassQuery(2, alpha2);
    }

    const handleSuccessfullyCopied = (e) => {
        console.info(`successfully copied to clipboard! ${e}`);
    };
    const handleFailedCopy = () => {
        console.info("failed to copy :(");
    };
</script>

<tr>
    <td><span class="fi fi-{alpha2Lower}" /></td>
    <td style="width: 50px; word-wrap: break-word;"
        ><a href={"./country/" + alpha2}>
            {country.name}
        </a></td
    >
    <td><span class="tag is-success is-light">2</span></td>
    <td
        ><a
            href="{baseUrl}/{basePath}/{baseFileName}.geojson.zip"
            target="_blank"
            ><span class="tag is-link is-light">{baseFileName}.geojson.zip</span
            ></a
        ></td
    >
    <td
        ><a href="{baseUrl}/{basePath}/{baseFileName}.shp.zip" target="_blank"
            ><span class="tag is-link is-light">{baseFileName}.shp.zip</span></a
        ></td
    >
    <td
        ><a
            href="{baseUrl}/{basePath}/{baseFileName}.mapinfo.zip"
            target="_blank"
            ><span class="tag is-link is-light">{baseFileName}.mapinfo.zip</span
            ></a
        ></td
    >
    <td
        ><a href="{baseUrl}/{basePath}/{baseFileName}.gpkg.zip" target="_blank"
            ><span class="tag is-link is-light">{baseFileName}.gpkg.zip</span
            ></a
        ></td
    >
    <td
        ><a href="{baseUrl}/{basePath}/{baseFileName}.csv.zip" target="_blank"
            ><span class="tag is-link is-light">{baseFileName}.csv.zip</span></a
        ></td
    >
    <td>
        <CopyToClipboard
            text={overpassQuery}
            on:copy={handleSuccessfullyCopied}
            on:fail={handleFailedCopy}
            let:copy
        >
            <Button size="is-small" on:click={copy}>Copy</Button>
        </CopyToClipboard>
    </td>
</tr>
