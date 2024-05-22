import os
import torch
import torch.nn as nn

import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder


from model import EmotionCNN
from helper_functions import accuracy_fn

from tqdm.auto import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Ustawienie hiperparametrów
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 50
MODEL_PATH = 'models/emotion_cnn2.pth'

# Przygotowanie danych
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

train_dataset = ImageFolder(root='server/AI/data/train', transform=transform)
test_dataset = ImageFolder(root='server/AI/data/test', transform=transform)

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

model = EmotionCNN(input_shape=1, hidden_units=128, output_shape=7).to(device)

# Sprawdzanie, czy model istnieje i wczytywanie go
if os.path.exists(MODEL_PATH):
    print("Wczytywanie istniejącego modelu...")
    model.load_state_dict(torch.load(MODEL_PATH))
    print("Model wczytany pomyślnie.\n")
else:
    print("Nie znaleziono modelu. Tworzenie nowego modelu\n")

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)

best_test_acc = 0

for epoch in tqdm(range(EPOCHS)):
    print(f'\nEpoch: {epoch + 1}/{EPOCHS}\n-----------')
    train_loss, train_acc = 0, 0

    for batch, (X, y) in enumerate(train_dataloader):
        X, y = X.to(device), y.to(device)
        model.train()

        y_pred = model(X)
        loss = loss_fn(y_pred, y)
        train_loss += loss.item()
        train_acc += accuracy_fn(y_true=y, y_pred=y_pred.argmax(dim=1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss /= len(train_dataloader)
    train_acc /= len(train_dataloader)
    print(f'Train loss: {train_loss:.4f} | Train accuracy: {train_acc:.2f}%')

    test_loss, test_acc = 0, 0
    model.eval()
    with torch.inference_mode():
        for X, y in test_dataloader:
            X, y = X.to(device), y.to(device)
            test_pred = model(X)
            test_loss += loss_fn(test_pred, y).item()
            test_acc += accuracy_fn(y_true=y, y_pred=test_pred.argmax(dim=1))
        
        test_loss /= len(test_dataloader)
        test_acc /= len(test_dataloader)
        print(f'Test loss: {test_loss:.4f} | Test accuracy: {test_acc:.2f}%')


torch.save(model.state_dict(), MODEL_PATH)


"""
Wynik:
Epoch: 50/50
-----------
Train loss: 0.7633 | Train accuracy: 71.53%
Test loss: 1.1637 | Test accuracy: 63.69%
"""