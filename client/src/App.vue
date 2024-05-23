<script setup>
    import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <h1 class="title">
        <router-link class="title" to="/">Emotion Detection</router-link>
    </h1>
    <RouterView />
</template>

<style scoped>
    .title {
        font-size: 3rem;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2.5rem;
        padding-top: 1rem;
        text-decoration: none;
        color: #0c1203;
    }
</style>
