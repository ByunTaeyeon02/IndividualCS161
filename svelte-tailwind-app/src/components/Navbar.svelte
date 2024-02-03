<script lang="ts">
	//import meep from "../images/MyMeepies.png";
    import { navigate } from 'svelte-routing';

	function handleHome() {
		navigate("/");
	}

    function handleProjects() {
		navigate("/Projects");
	}

	function handleContact() {
		navigate("/Contact");
	}
</script>

<style>
	.navbar {
		box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Adjust the values as needed */
	}
</style>

<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
<div class="navbar px-4">
    <div class="flex-1">
        <a class="btn btn-ghost normal-case text-xs" href="/home">
            <!-- svelte-ignore a11y-missing-attribute -->
            <img src={"https://i.ytimg.com/vi/Grrz_gtb5Vg/maxresdefault.jpg"} class="w-1">
        </a>
    </div>
    <!-- svelte-ignore missing-declaration -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleHome}>
        <div class="indicator">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-2 -2 30 30"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
        </div>
    </label>
    <!-- svelte-ignore missing-declaration -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleProjects}>
        <div class="indicator">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-2 -2 30 30"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
        </div>
    </label>
    <!-- svelte-ignore missing-declaration -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleContact}>
        <div class="indicator">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-2 -2 30 30"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
        </div>
    </label>
</div>