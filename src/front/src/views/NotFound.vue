<template>
    <div id="content">
        <h2 class="errtext">E404: Page not found</h2>
        <p>Go <router-link :to="'/'">home</router-link></p>
    </div>
</template>

<style scoped>
#content {
    padding-top: 60px;
    padding-bottom: 50px;
}

p {
    font-size: 16pt;
    text-align: center;
}

.errtext {
    color: crimson;
    text-align: center;
    text-shadow: 2px 2px 2px pink;
}

</style>