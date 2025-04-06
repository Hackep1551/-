import tkinter as tk
from ui.app_window import AppWindow
from utils.json_handler import initialize_config

if __name__ == "__main__":
    # Инициализируем конфигурацию из шаблона при запуске
    initialize_config()
    
    # Создаем и запускаем приложение
    root = tk.Tk()
    
    # Устанавливаем размер окна (ширина x высота)
    window_width = 1200
    window_height = 800
    
    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Находим координаты для центрирования окна
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    
    # Устанавливаем размер и позицию окна
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    app = AppWindow(root)
    root.mainloop()
