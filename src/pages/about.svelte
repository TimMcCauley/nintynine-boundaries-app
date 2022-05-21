<script>
    import Fa from "svelte-fa";
    import { faGithub } from "@fortawesome/free-brands-svg-icons";

    import { metatags } from "@roxi/routify";

    metatags.title = "About 99Bounadires";
    metatags.description = "The About Section";
</script>

<main>
    <div class="content is-normal">
        <h1>99Boundaries</h1>
        <p>
            This website provides <strong>OpenStreetMap</strong> boundaries for
            all countries for free. The data is generated via the
            <strong>Overpass API</strong>
            and exported to different file formats.
        </p>
        <h2>Data Generation</h2>
        <p>
            Data is re-generated once a month. Currently <span
                class="tag is-success is-light"
            >
                admin level 2
            </span> is provided, however the plans are to introduce higher levels,
            too.
        </p>
        <h2>Feedback</h2>
        <p>
            Do you have ideas how to make this website more user friendly or
            even how to pimp the overpass queries? Please feel free to raise an
            issue or start an discussion in the
            <a href={"https://github.com/TimMcCauley/nintynine_boundaries/"}
                ><strong><Fa icon={faGithub} /> GitHub repository</strong></a
            >.
        </p>
    </div>
</main>
