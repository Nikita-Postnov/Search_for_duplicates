import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


def find_duplicates(folder):
    file_hash = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Пропустить папки и символьные ссылки
            if not os.path.isfile(filepath):
                continue

            with open(filepath, "rb") as f:
                filehash = hashlib.md5(f.read()).hexdigest()

            if filehash not in file_hash:
                file_hash[filehash] = [filepath]
            else:
                file_hash[filehash].append(filepath)

    for filehash, files in file_hash.items():
        if len(files) > 1:
            duplicates.append(files)

    return duplicates


def delete_duplicates(duplicates):
    for files in duplicates:
        message = "Дубликаты файлов:\n" + "\n".join(files)
        choice = messagebox.askyesno("Удаление дубликатов", message + "\n\nУдалить дубликаты?")
        if choice:
            for file in files[1:]:
                os.remove(file)
                print(f"{file} удален.")


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        duplicates = find_duplicates(folder_path)
        if duplicates:
            delete_duplicates(duplicates)
        else:
            messagebox.showinfo("Поиск дубликатов", "Дубликатов не найдено.")
    else:
        messagebox.showwarning("Ошибка", "Не выбрана папка.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Поиск дубликатов файлов")
    root.geometry("300x100")

    browse_button = tk.Button(root, text="Выбрать папку", command=browse_folder)
    browse_button.pack(pady=20)

    root.mainloop()
