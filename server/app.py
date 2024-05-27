from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import json
import random
from fastapi.responses import JSONResponse
import uvicorn

from AI.model import EmotionCNN


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicjalizacja modelu
device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = 'AI/models/emotion_cnn.pth'
model = EmotionCNN(input_shape=1, hidden_units=128, output_shape=7).to(device)

# Wczytywanie modelu
if torch.cuda.is_available():
    model.load_state_dict(torch.load(MODEL_PATH))
else:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# Przekształcenia obrazu
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# Mapowanie numerów klas na nazwy emocji
class_names = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Emotion Detection API"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)
        image = Image.open(io.BytesIO(await file.read())).convert('L')
        image = transform(image).unsqueeze(0).to(device)
        print("Image transformed successfully")

        with torch.no_grad():
            output = model(image)
            probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]
            predicted = torch.argmax(output, 1).cpu().numpy()[0]
            predicted_emotion = class_names[predicted]

        response = {
            "emotion": predicted_emotion,
            "probabilities": {class_names[i]: float(probabilities[i]) for i in range(len(class_names))}
        }

        return response
    except Exception as e:
        print("Error processing the image:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    


# Load memes from JSON file
with open("memes.json", "r") as file:
    memes = json.load(file)

@app.get("/random_meme/{emotion}")
async def random_meme(emotion: str):
    print(f"Received request for emotion: {emotion}")
    if emotion in memes:
        meme_url = random.choice(memes[emotion])
        print(f"Selected meme URL: {meme_url}")
        return {"url": meme_url}
    else:
        print("No memes found for emotion:", emotion)
        return {"url": None}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
