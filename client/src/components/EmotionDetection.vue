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

    /**
     * Starts the video stream from the user's camera and sets it as the source for the video element.
     * @function startVideo
     * @returns {void}
     */
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

    /**
     * Function to get the emotion from the video frame.
     * It captures the current frame from the video element, converts it to a data URL,
     * creates a blob from the data URL, and sends it to the server for emotion prediction.
     * The predicted emotion and probabilities are then updated in the component's reactive variables.
     */
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

    /**
     * Converts a data URI to a Blob object.
     *
     * @param {string} dataURI - The data URI to convert.
     * @returns {Blob} - The converted Blob object.
     */
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

    /**
     * Returns an emoji icon based on the given emotion.
     *
     * @param {string} emotion - The emotion to get the icon for.
     * @returns {string} The emoji icon corresponding to the emotion.
     */
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

    /**
     * Requests permission for browser notifications.
     *
     * @returns {void}
     */
    const askNotificationPermission = () => {
        Notification.requestPermission().then((permission) => {
            if (permission === 'granted') {
                console.log('Notification permission granted.')
            } else {
                console.log('Notification permission denied.')
            }
        })
    }

    /**
     * Shows a notification with a meme.
     *
     * @param {string} memeUrl - The URL of the meme to be displayed as the notification icon.
     */
    const showNotification = (memeUrl) => {
        const notification = new Notification('New Meme Available!', {
            body: 'Click to see the meme.',
            icon: memeUrl,
        })
        notification.onclick = () => {
            window.open(memeUrl, '_blank')
        }
    }

    /**
     * Fetches a meme based on the selected emotion.
     * @async
     * @function fetchMeme
     * @throws {Error} If the network response is not ok.
     */
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
                showNotification(memeUrl)
            } else {
                console.log('No meme URL received')
            }
        } catch (error) {
            console.error('Error fetching meme:', error)
        }
    }

    /**
     * Sets the interval for fetching memes.
     * If there is an existing interval, it is cleared before setting the new interval.
     * @function setMemeInterval
     */
    const setMemeInterval = () => {
        if (memeInterval) {
            clearInterval(memeInterval)
        }
        memeInterval = setInterval(fetchMeme, selectOption.value)
    }

    /**
     * Watches the `selectOption` property for changes and performs actions accordingly.
     *
     * @param {any} newVal - The new value of the `selectOption` property.
     * @param {any} oldVal - The old value of the `selectOption` property.
     */
    watch(selectOption, (newVal, oldVal) => {
        console.log(`Changed meme interval from ${oldVal} to ${newVal}`)
        setMemeInterval()
    })

    /**
     * Initializes the EmotionDetection component.
     * - Requests permission for notifications.
     * - Starts the video stream.
     * - Sets up a recurring interval to get emotion data.
     * - Sets up a recurring interval to display memes.
     */
    onMounted(() => {
        askNotificationPermission()
        startVideo()
        setTimeout(() => {
            setInterval(getEmotion, 1000)
        }, 100)
        setMemeInterval()
    })

    /**
     * Array of options for the selection.
     *
     * Each option object has a `label` property representing the display label
     * and a `value` property representing the corresponding value in milliseconds.
     *
     * @type {Array<{ label: string, value: number }>}
     */
    const selectOptions = [
        { label: "Don't show memes", value: 36000000000 },
        { label: '1 min', value: 60000 },
        { label: '3 min ', value: 180000 },
        { label: '5 min', value: 300000 },
        { label: '10 min', value: 600000 },
    ]

    /**
     * Callback function triggered when the submit button is clicked.
     * It logs a message to the console and updates the value of showModal.
     */
    const submitCallback = () => {
        console.log('Submit clicked')
        console.log(selectOption)
        showModal.value = false
    }

    /**
     * Callback function for cancel action.
     * Logs 'Cancel clicked' to the console and hides the modal.
     */
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
