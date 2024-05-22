<script setup>
    import EmotionDetection from '../components/EmotionDetection.vue'
</script>

<template>
    <main class="emotion-detection-container">
        <EmotionDetection />
        <div class="btn">
            <router-link to="/howitworks" class="howitworks">
                How it works?
            </router-link>
        </div>
    </main>
</template>

<style scoped>
    .emotion-detection-container {
        display: flex;
        flex-direction: column;
    }

    .btn {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    .howitworks {
        text-align: center;
        font-size: 1.5rem;
        text-decoration: none;
        color: #fff;
        background-color: #42a5f5;
        border: 3px solid #42a5f5;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        width: 200px;
        transition: all 0.3s ease;
        animation: pulse 1.5s infinite;
    }

    .howitworks:hover {
        background-color: #ff4081;
        border-color: #ff4081;
        color: #fff;
        transform: scale(1.1);
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(66, 165, 245, 0.7);
        }
        70% {
            box-shadow: 0 0 10px 20px rgba(66, 165, 245, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(66, 165, 245, 0);
        }
    }
</style>
