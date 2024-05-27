<script setup>
    import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <main>
        <h1 class="title">
            <router-link class="title" to="/">Emotion Detection</router-link>
        </h1>
        <RouterView />
    </main>
</template>

<style scoped>
    .title {
        font-size: 3rem;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2.5rem;
        padding-top: 2rem;
        text-decoration: none;
        color: #0c1203;
    }

    @media (max-width: 1536px) {
        .title {
            font-size: 2rem;
            margin-bottom: 0rem;
        }
    }
</style>
