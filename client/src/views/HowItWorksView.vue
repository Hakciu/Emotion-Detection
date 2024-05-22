<template>
    <div class="howItWorks">
        <h1>How it works</h1>
        <p>
            This project showcases an emotion detection application built using
            Artificial Intelligence (AI) with PyTorch. The core of this
            application is a Convolutional Neural Network (CNN) model, trained
            on the FER-2013 Dataset. This dataset includes a wide range of
            facial expressions categorized into different emotions such as
            happiness, sadness, anger, and more.
        </p>
        <p>
            The CNN model consists of several layers designed to extract and
            process features from the input images. It includes three
            convolutional blocks, each featuring ReLU activation functions and
            batch normalization layers to stabilize and speed up the learning
            process. Each block ends with a max-pooling layer to reduce the
            spatial dimensions of the data.
        </p>
        <p>
            After these convolutional layers, the data is flattened and passed
            through two fully connected (dense) layers. The first dense layer
            contains 512 neurons and is followed by a ReLU activation function
            and a dropout layer to prevent overfitting. The final layer is a
            softmax layer with 7 neurons, corresponding to the 7 emotion
            categories.
        </p>
        <p>
            For the backend, FastAPI is used to create a server that handles
            communication between the web interface and the AI model. When the
            application is used, the video feed from the camera is captured and
            processed frame by frame. Each frame is converted into an image and
            sent to the FastAPI server as a POST request.
        </p>
        <p>
            The server processes each image using the pre-trained CNN model to
            predict the emotion displayed. It then sends back the predictions,
            including probabilities for each emotion category, to the frontend.
            The application dynamically updates to display the detected emotion
            and the corresponding probabilities in real-time.
        </p>
        <p>
            This project was developed as part of the coursework for the
            Artificial Neural Network (ANN) subject. It demonstrates the
            practical application of neural networks and deep learning
            techniques in solving real-world problems.
        </p>
        <div class="btn">
            <router-link to="/" class="howitworks">Try it out</router-link>
        </div>
    </div>
</template>

<style scoped>
    .howItWorks {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        font-family: Roboto, sans-serif;
    }

    h1 {
        text-align: center;
        margin-bottom: 20px;
    }

    p {
        margin-bottom: 15px;
        line-height: 1.6;
    }

    .btn {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
        font-family: 'Poetsen One', sans-serif;
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
