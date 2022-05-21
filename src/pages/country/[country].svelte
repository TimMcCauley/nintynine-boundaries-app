<script>
    import { metatags } from "@roxi/routify";
    import { params } from "@roxi/routify";
    import countries from "../../active-countries.json";

    let country = $params.country;

    let countryName;
    for (let cntry of countries) {
        if (cntry["alpha-2"] == country) {
            countryName = cntry["name"];
            break;
        }
    }

    metatags.title = "Additional downloads for " + country;
    metatags.description = "Country Boundary packages for " + country;
</script>

<main>
    <div class="content is-normal">
        <h2>{countryName}</h2>
        <p>
            Additional boundary extracts of {countryName} to follow.
        </p>
    </div>
</main>
