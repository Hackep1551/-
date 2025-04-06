import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from ui.constants import *
from utils.json_handler import load_config, update_memory_config
from ui.sections_ui.section_factory import SectionFactory

class SectionFrame(tk.Frame):
    def __init__(self, parent, section_name):
        super().__init__(parent, bg=DARK_SECONDARY)
        self.section_name = section_name
        self.config_data = {}
        self.section_instance = None
        self.setup_ui()
        
    def setup_ui(self):
        # Отключаем автоматическое изменение размера
        self.pack_propagate(False)
        
        # Главный вертикальный фрейм
        main_frame = tk.Frame(self, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок раздела
        header = tk.Label(main_frame, text=self.section_name, font=FONT_HEADER, 
                         fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(anchor="w", padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        # Создаем канвас с прокруткой для полей настроек
        canvas_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Добавляем вертикальную прокрутку
        v_scrollbar = tk.Scrollbar(canvas_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаём канвас
        canvas = tk.Canvas(canvas_frame, bg=DARK_SECONDARY, 
                         bd=0, highlightthickness=0,
                         yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=canvas.yview)
        
        # Фрейм внутри канваса для полей
        self.fields_frame = tk.Frame(canvas, bg=DARK_SECONDARY)
        canvas_window = canvas.create_window((0, 0), window=self.fields_frame, anchor="nw", tags="fields_frame")
        
        # Настраиваем изменение размера канваса при изменении размера фрейма
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.fields_frame.bind("<Configure>", on_frame_configure)
        
        # Настраиваем изменение ширины фрейма при изменении ширины канваса
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Загрузка данных раздела
        self.load_section()
    
    def load_section(self):
        # Очистка текущих полей
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        
        # Загрузка данных из конфигурации
        self.config_data = load_config(self.section_name)
        
        if not self.config_data:
            empty_label = tk.Label(self.fields_frame, text="Нет доступных настроек для этого раздела",
                                  fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_NORMAL)
            empty_label.pack(pady=PADDING_LARGE)
            return
        
        # Создаем соответствующий раздел с помощью фабрики
        self.section_instance = SectionFactory.create_section(
            self.section_name, 
            self.fields_frame, 
            self.config_data
        )
