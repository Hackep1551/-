import tkinter as tk
import json

from ui.constants import *
from utils.json_handler import load_config, get_full_config

class JsonPreviewFrame(tk.Frame):
    def __init__(self, parent, section_name):
        super().__init__(parent, bg=DARK_SECONDARY)
        self.section_name = section_name
        self.setup_ui()
    
    def setup_ui(self):
        # Настройка растяжения фрейма
        self.pack_propagate(False)  # Отключаем автоматическое изменение размера
        
        # Верхняя часть с элементами управления
        top_frame = tk.Frame(self, bg=DARK_SECONDARY)
        top_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Заголовок с названием раздела
        self.header = tk.Label(top_frame, text="JSON Preview", 
                             font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        self.header.pack(side=tk.LEFT)
        
        # Переключатель между полным JSON и текущей секцией
        self.view_mode_var = tk.StringVar(value="full")
        
        full_view_radio = tk.Radiobutton(top_frame, text="Полный конфиг", 
                                       variable=self.view_mode_var, value="full",
                                       command=self.update_view,
                                       bg=DARK_SECONDARY, fg=LIGHT_TEXT, 
                                       selectcolor=DARK_BG)
        full_view_radio.pack(side=tk.RIGHT, padx=(0, PADDING_MEDIUM))
        
        section_view_radio = tk.Radiobutton(top_frame, text="Текущий раздел", 
                                          variable=self.view_mode_var, value="section",
                                          command=self.update_view,
                                          bg=DARK_SECONDARY, fg=LIGHT_TEXT,
                                          selectcolor=DARK_BG)
        section_view_radio.pack(side=tk.RIGHT, padx=(0, PADDING_MEDIUM))
        
        # Текстовое поле для отображения JSON
        self.text_frame = tk.Frame(self, bg=DARK_SECONDARY)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Настройка растяжения текстового фрейма
        self.text_frame.pack_propagate(False)  # Отключаем автоматическое изменение размера
        
        # Добавляем скроллбары
        y_scrollbar = tk.Scrollbar(self.text_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = tk.Scrollbar(self.text_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Текстовое поле с моноширинным шрифтом для JSON
        self.text_area = tk.Text(self.text_frame, bg=DARK_BG, fg=LIGHT_TEXT,
                              font=("Consolas", 11), wrap=tk.NONE,  # NONE для горизонтальной прокрутки
                              yscrollcommand=y_scrollbar.set,
                              xscrollcommand=x_scrollbar.set)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        y_scrollbar.config(command=self.text_area.yview)
        x_scrollbar.config(command=self.text_area.xview)
        
        # Запрещаем редактирование
        self.text_area.config(state=tk.DISABLED)
        
        # Загружаем данные
        self.update_section(self.section_name)
    
    def update_section(self, section_name):
        """Обновляет текущий раздел и обновляет просмотр"""
        self.section_name = section_name
        self.update_view()
    
    def update_view(self):
        """Обновляет содержимое JSON предпросмотра в зависимости от выбранного режима"""
        view_mode = self.view_mode_var.get()
        
        # Определяем, какие данные показывать
        if view_mode == "full":
            # Загружаем полную конфигурацию из памяти
            config_data = get_full_config()
            self.header.config(text="JSON Preview: Полный конфиг")
        else:
            # Загружаем только текущий раздел из памяти
            config_data = load_config(self.section_name)
            self.header.config(text=f"JSON Preview: {self.section_name}")
        
        # Форматируем JSON с отступами для читаемости
        formatted_json = json.dumps(config_data, indent=4, ensure_ascii=False)
        
        # Разрешаем редактирование для обновления содержимого
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, formatted_json)
        self.text_area.config(state=tk.DISABLED)  # Снова запрещаем редактирование
        
        # Прокручиваем в начало
        self.text_area.yview_moveto(0)
        self.text_area.xview_moveto(0)
