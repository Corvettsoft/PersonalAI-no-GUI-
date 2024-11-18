import os
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Размер изображений
IMAGE_SIZE = 1024

# Количество эпох обучения
EPOCHS = 20000

# Функция для загрузки изображений из папки
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        image = Image.open(img_path).convert('L')  # Преобразуем в черно-белое изображение
        image = image.resize((IMAGE_SIZE, IMAGE_SIZE))  # Изменяем размер до 1024x1024
        data = np.array(image.getdata()) / 255  # Нормализуем данные от 0 до 1
        images.append(data)
    return images

# Загрузка данных
images_1 = load_images_from_folder("1")
labels_1 = [1] * len(images_1)

images_0 = load_images_from_folder("0")
labels_0 = [0] * len(images_0)

# Объединение всех данных
X_train = np.concatenate([images_1, images_0])
y_train = labels_1 + labels_0

# Проверка существования файла с весами
if os.path.exists("FaceWeights.txt"):
    with open("FaceWeights.txt", "r") as f:
        lines = f.readlines()
        weights_str = lines[-2].strip().split(",")
        weights = np.array(list(map(float, weights_str)))
        bias = float(lines[-1].strip())
else:
    # Инициализация весов и смещения
    weights = np.zeros(X_train.shape[1])  # Веса для каждого пикселя
    bias = 0  # Смещение

# Основной цикл работы программы
while True:
    command = input("Enter command (Training/Start/Exit): ").lower()

    if command == 'training':
        # Обучение перцептрона
        for epoch in range(EPOCHS):
            for x, y in zip(X_train, y_train):
                prediction = np.dot(x, weights) + bias > 0
                error = y - int(prediction)
                
                if error != 0:
                    weights += error * x
                    bias += error

        # Добавление новых весов и смещения в конец файла
        with open("FaceWeights.txt", "a+") as f:
            f.write(f"\n{','.join(map(str, weights))}\n{bias}")

        print("AI training completed.")

    elif command == 'start':
        root = tk.Tk()
        root.withdraw()  # Скрываем главное окно

        file_path = filedialog.askopenfilename(title="Choose picture")

        if file_path:
            try:
                image = Image.open(file_path).convert('L')
                image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
                data = np.array(image.getdata()) / 255
                
                prediction = np.dot(data, weights) + bias > 0
                iprediction = int(prediction)
                print("Trained_Object_detection:", int(prediction))
            except Exception as e:
                print("Log: error: loading distrupted", e)

    elif command == 'exit':
        break

    else:
        print("Log: error: Unknown command. Try again.")