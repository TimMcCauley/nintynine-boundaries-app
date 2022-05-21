<script>
    import "bulma/css/bulma.css";

    import Select from "svelte-select";

    import { Tabs, Tab } from "svelma";
    import { metatags } from "@roxi/routify";

    import Fa from "svelte-fa";
    import { faGithub } from "@fortawesome/free-brands-svg-icons";
    import { faGlobe } from "@fortawesome/free-solid-svg-icons";

    import countries from "../active-countries.json";
    import { isIterable } from "../utils.js";

    import RowBody from "./_RowBody.svelte";
    import RowHead from "./_RowHead.svelte";

    metatags.title = "Download OpenStreetMap Boundaries";
    metatags.description = "Free OSM Boundaries in different file formats.";

    const adminLevel = 2;

    let countrySelectItems = [];
    for (const country of countries) {
        countrySelectItems.push({
            value: country["alpha-2"],
            label: country.name,
        });
    }

    let selectedCountries = [];
    function handleSelect(event) {
        selectedCountries = [];
        if (isIterable(event.detail)) {
            for (const selectedCountry of event.detail) {
                selectedCountries.push(selectedCountry.value);
            }
        }
    }
</script>

<main>
    <div class="header">
        <nav class="navbar is-transparent" aria-label="main navigation">
            <div class="navbar-brand">
                <a class="navbar-item" href="https://99boundaries.com">
                    <img src="logo.png" width="120" alt="logo" height="auto" />
                </a>
            </div>
            <div class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href={"./about"}> About </a>
                </div>
                <div class="navbar-end">
                    <div
                        class="navbar-item"
                        style="padding-right: 5px !important;"
                    >
                        <div class="buttons">
                            <a
                                class="button is-primary is-small"
                                target="_blank"
                                href={"https://overpass-turbo.eu/"}
                            >
                                <Fa icon={faGlobe} />
                                <span style="padding-left: 5px;"
                                    ><strong>Overpass Turbo</strong></span
                                >
                            </a>
                        </div>
                    </div>
                    <div class="navbar-item">
                        <div class="buttons">
                            <a
                                class="button is-dark is-small"
                                target="_blank"
                                href={"https://github.com/TimMcCauley/nintynine_boundaries/"}
                            >
                                <Fa icon={faGithub} />
                                <span style="padding-left: 5px;"
                                    ><strong>GitHub</strong></span
                                >
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <div class="block">
            Boundaries are generated via <strong
                ><a href="http://overpass-api.de/" target="_blank">Overpass</a
                ></strong
            >
            &
            <strong
                ><a
                    href="https://osmdata.openstreetmap.de/data/land-polygons.html"
                    target="_blank">OSM Land Polygons</a
                ></strong
            >
            <a href="https://www.openstreetmap.org/copyright" rel="nofollow"
                >[© OpenStreetMap contributors]</a
            >
            and provided in <a href="https://epsg.io/4326">EPSG:4326</a>.
        </div>

        <Select
            items={countrySelectItems}
            isMulti={true}
            placeholder="Filter countries..."
            on:select={handleSelect}
        />
    </div>

    <div class="content">
        <Tabs style="is-boxed">
            <Tab label="Maritime Polygons">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <RowHead />
                        </tr>
                    </thead>
                    <tbody>
                        {#each countries as country}
                            {#if selectedCountries.length > 0}
                                {#if selectedCountries.includes(country["alpha-2"])}
                                    <RowBody {country} {adminLevel} />
                                {/if}
                            {:else}
                                <RowBody {country} {adminLevel} />
                            {/if}
                        {/each}
                    </tbody>
                </table>
            </Tab>

            <Tab label="Land Polygons">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <RowHead />
                        </tr>
                    </thead>
                    <tbody>
                        {#each countries as country}
                            {#if selectedCountries.length > 0}
                                {#if selectedCountries.includes(country["alpha-2"])}
                                    <RowBody
                                        {country}
                                        {adminLevel}
                                        landOnly={true}
                                    />
                                {/if}
                            {:else}
                                <RowBody
                                    {country}
                                    {adminLevel}
                                    landOnly={true}
                                />
                            {/if}
                        {/each}
                    </tbody>
                </table>
            </Tab>
        </Tabs>
    </div>
</main>
