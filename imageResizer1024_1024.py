from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

def select_input_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Выберите папку с исходными изображениями")
    return folder_selected

def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Выберите папку для сохраненных изображений")
    return folder_selected

# Запрашиваем у пользователя выбор папок
input_folder = select_input_folder()
output_folder = select_output_folder()

# Создаем папку для вывода, если она еще не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Проходимся по всем файлам в input_folder
for filename in os.listdir(input_folder):
    # Проверяем, является ли файл изображением
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(input_folder, filename)
        
        try:
            # Открываем изображение
            img = Image.open(file_path)
            
            # Изменяем размер изображения до 1024x1024
            resized_img = img.resize((1024, 1024), resample=Image.LANCZOS)
            
            # Сохраняем обработанное изображение в output_folder
            output_file_path = os.path.join(output_folder, filename)
            resized_img.save(output_file_path)
            
            print(f'Обработано изображение: {filename}')
        except Exception as e:
            print(f'Ошибка при обработке файла {filename}: {e}')