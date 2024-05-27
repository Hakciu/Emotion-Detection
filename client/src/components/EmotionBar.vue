<template>
    <div class="emotion-bar">
        <span class="icon">{{ icon }}</span>
        <div class="bar-container">
            <div class="bar" :style="{ width: probability + '%' }"></div>
            <span class="percentage">{{ probability }}%</span>
        </div>
        <span class="emotion-name">{{ emotionName }}</span>
    </div>
</template>

<script setup>
    import { defineProps } from 'vue'

    const props = defineProps({
        icon: {
            type: String,
            required: true,
        },
        probability: {
            type: Number,
            required: true,
        },
        emotionName: {
            type: String,
            required: true,
        },
    })
</script>

<style scoped>
    .emotion-bar {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }

    .icon {
        font-size: 2rem; /* Wielkość emoji */
        margin-right: 10px;
    }

    .bar-container {
        position: relative;
        flex-grow: 1;
        height: 40px;
        border: 2px solid #000;
        border-radius: 20px;
        overflow: hidden;
        min-width: 200px; /* Dodanie minimalnej szerokości */
        margin-right: 10px; /* Odstęp dla nazw emocji */
    }

    .bar {
        height: 100%;
        background-color: #42a5f5;
        border-radius: 10px;
        transition: width 0.5s;
    }

    .percentage {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-weight: bold;
        color: #000;
    }

    .emotion-name {
        min-width: 60px; /* Dodanie minimalnej szerokości dla wyrównania */
        text-align: left; /* Wyrównanie tekstu do lewej */
        font-weight: bold;
    }

    @media (max-width: 1536px) {
        .icon {
            font-size: 1.5rem;
        }

        .bar-container {
            height: 30px;
            min-width: 150px;
        }

        .percentage {
            font-size: 0.8rem;
        }

        .emotion-name {
            min-width: 50px;
        }
    }
</style>
