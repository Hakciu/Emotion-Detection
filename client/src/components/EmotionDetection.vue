<script setup>
    import { ref, onMounted, watch } from 'vue'
    import EmotionBar from './EmotionBar.vue'
    import { NButton, NModal, NSelect } from 'naive-ui'

    const video = ref(null)
    const canvas = ref(null)
    const emotion = ref('')
    const probabilities = ref({})
    const showModal = ref(false)
    const selectOption = ref(300000)
    let memeInterval = null

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
        setTimeout(() => {
            setInterval(getEmotion, 1000)
        }, 100) // Opóźnienie żeby nie wywalalo błędu
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

    const fetchMeme = async () => {
        try {
            console.log('Fetching meme for emotion:', emotion.value)
            const response = await fetch(
                `http://localhost:8000/random_meme/${emotion.value}`
            )
            if (!response.ok) {
                throw new Error('Network response was not ok')
            }
            const data = await response.json()
            const memeUrl = data.url
            console.log('Meme URL fetched:', memeUrl)
            if (memeUrl) {
                focusTabAndOpenUrl(memeUrl)
            } else {
                console.log('No meme URL received')
            }
        } catch (error) {
            console.error('Error fetching meme:', error)
        }
    }

    // Funkcja do skupienia karty i otwarcia nowego adresu URL
    const focusTabAndOpenUrl = (url) => {
        window.focus()
        setTimeout(() => {
            window.open(url, '_blank')
        }, 100) // Opóźnienie, aby upewnić się, że karta jest skupiona
    }

    const setMemeInterval = () => {
        if (memeInterval) {
            clearInterval(memeInterval)
        }
        memeInterval = setInterval(fetchMeme, selectOption.value)
    }

    watch(selectOption, (newVal, oldVal) => {
        console.log(`Changed meme interval from ${oldVal} to ${newVal}`)
        setMemeInterval()
    })

    onMounted(() => {
        setMemeInterval()
    })

    const selectOptions = [
        {
            label: "Don't show memes",
            value: 36000000000,
        },
        { label: '1 min', value: 60000 },
        { label: '3 min ', value: 180000 },
        { label: '5 min', value: 300000 },
        { label: '10 min', value: 600000 },
    ]

    const submitCallback = () => {
        console.log('Submit clicked')
        console.log(selectOption)
        showModal.value = false
    }

    const cancelCallback = () => {
        console.log('Cancel clicked')
        showModal.value = false
    }
</script>

<template>
    <main>
        <div class="emotion-detection">
            <div class="camera-container">
                <div class="camera">
                    <video
                        ref="video"
                        width="700"
                        height="525"
                        autoplay
                    ></video>
                    <canvas ref="canvas" style="display: none"></canvas>
                </div>
                <n-button @click="showModal = true">Show meme</n-button>
                <n-modal
                    v-model:show="showModal"
                    preset="dialog"
                    title="Show memes based on your emotion"
                    positive-text="Submit"
                    negative-text="Cancel"
                    @positive-click="submitCallback"
                    @negative-click="cancelCallback"
                >
                    <template #default>
                        <p>How long do you want to see memes?</p>
                        <n-select
                            v-model:value="selectOption"
                            :options="selectOptions"
                            placeholder="Choose time"
                            style="width: 100%; margin-top: 20px"
                        />
                    </template>
                </n-modal>
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
    .camera-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 3rem;
    }
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

    /* @media (max-width: 1200px) {
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
    } */

    @media (max-width: 1536px) {
        .emotion-detection {
            flex-direction: row;
            align-items: flex-start;
            margin-top: 3rem;
        }

        .camera,
        .results {
            width: 500px;
        }

        .results {
            min-height: auto;
        }

        .results .detected-emotion {
            font-size: 1.5rem;
        }

        .emotion-bar-container {
            margin-top: 10px;
        }
    }
</style>
