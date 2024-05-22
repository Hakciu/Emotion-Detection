<script setup>
    import { ref, onMounted } from 'vue'
    import EmotionBar from './EmotionBar.vue'

    const video = ref(null)
    const canvas = ref(null)
    const emotion = ref('')
    const probabilities = ref({})

    const getEmotion = async () => {
        const context = canvas.value.getContext('2d')
        context.drawImage(
            video.value,
            0,
            0,
            canvas.value.width,
            canvas.value.height
        )
        const imageData = canvas.value.toDataURL('image/jpeg')

        const blob = dataURItoBlob(imageData)
        const formData = new FormData()
        formData.append('file', blob, 'image.jpg')

        const response = await fetch('http://localhost:8000/predict/', {
            method: 'POST',
            body: formData,
        })

        const result = await response.json()
        emotion.value = result.emotion
        probabilities.value = result.probabilities
    }

    const startVideo = () => {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                video.value.srcObject = stream
            })
            .catch((err) => {
                console.error('Error accessing camera: ', err)
            })
    }

    onMounted(() => {
        startVideo()
        setInterval(getEmotion, 1000) // Co 1 sekundę
    })

    const dataURItoBlob = (dataURI) => {
        const byteString = atob(dataURI.split(',')[1])
        const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
        const ab = new ArrayBuffer(byteString.length)
        const ia = new Uint8Array(ab)
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i)
        }
        return new Blob([ab], { type: mimeString })
    }

    const getIcon = (emotion) => {
        switch (emotion) {
            case 'Happy':
                return '😊'
            case 'Sad':
                return '😢'
            case 'Angry':
                return '😡'
            case 'Surprise':
                return '😲'
            case 'Fear':
                return '😨'
            case 'Disgust':
                return '🤢'
            case 'Neutral':
                return '😐'
            default:
                return '❓'
        }
    }
</script>

<template>
    <main>
        <div class="emotion-detection">
            <div class="camera-container">
                <div class="camera">
                    <video
                        ref="video"
                        width="800"
                        height="600"
                        autoplay
                    ></video>
                    <canvas ref="canvas" style="display: none"></canvas>
                </div>
            </div>
            <div class="results">
                <p class="detected-emotion">
                    Detected Emotion: {{ emotion ? emotion : '' }}
                    {{ getIcon(emotion) }}
                </p>
                <div
                    class="emotion-bar-container"
                    v-for="(probability, emotion) in probabilities"
                    :key="emotion"
                >
                    <EmotionBar
                        :icon="getIcon(emotion)"
                        :probability="Number((probability * 100).toFixed(2))"
                        :emotionName="emotion"
                    />
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
    .title {
        text-align: center;
        font-size: 3rem;
    }

    .emotion-detection {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        flex-direction: row;
        margin: 0 10rem;
        flex-wrap: wrap;
        min-height: 650px; /* Ustawienie minimalnej wysokości */
    }

    video,
    canvas {
        display: block;
        max-width: 100%;
        height: auto;
    }

    p {
        text-align: center;
    }

    .emotion-bar-container {
        margin-top: 20px;
        width: 85%;
    }

    .detected-emotion {
        font-size: 2rem;
        margin-bottom: 20px;
        font-weight: bold;
    }

    .camera-container {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 800px; /* Ensure fixed size */
        height: 600px; /* Ensure fixed size */
    }

    .camera {
        position: relative;
        padding: 10px;
        background-color: white;
    }

    .camera::before,
    .camera::after {
        content: '';
        position: absolute;
        top: -15px; /* Adjust as needed */
        left: -15px; /* Adjust as needed */
        width: calc(100% + 30px); /* Adjust as needed */
        height: calc(100% + 30px); /* Adjust as needed */
        border: 3px dashed #42a5f5;
        border-radius: 10px;
        box-sizing: border-box;
        animation: dash 2s linear infinite;
    }

    .camera::after {
        border-color: #ff4081;
        animation-delay: 1s;
    }

    @keyframes dash {
        0% {
            stroke-dashoffset: 100%;
        }
        100% {
            stroke-dashoffset: 0%;
        }
    }

    .results {
        flex-basis: 45%;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 600px; /* Ensure fixed size */
    }

    @media (max-width: 1200px) {
        .emotion-detection {
            margin: 0 5rem;
        }
    }

    @media (max-width: 768px) {
        .emotion-detection {
            flex-direction: column;
            margin: 0 2rem;
        }

        .camera,
        .results {
            flex-basis: 100%;
        }

        .detected-emotion {
            font-size: 1.5rem;
        }
    }
</style>
