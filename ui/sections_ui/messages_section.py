import tkinter as tk
from tkinter import ttk, colorchooser
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class MessagesSection(BaseSection):
    """Класс для отображения настроек раздела Messages"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела Messages"""
        # Создаем главный фрейм, занимающий все доступное пространство
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок в верхней части окна
        header_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        header_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        header = tk.Label(header_frame, text="Настройка игровых сообщений", 
                        font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(side=tk.LEFT)
        
        description = tk.Label(header_frame, text="Настройте текст и цвет системных сообщений", 
                             fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        description.pack(side=tk.LEFT, padx=(PADDING_MEDIUM, 0))
        
        # Создаем фрейм с прокруткой для всех сообщений
        canvas_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Добавляем вертикальную прокрутку
        scrollbar = tk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаем канвас для прокручиваемого содержимого
        canvas = tk.Canvas(canvas_frame, bg=DARK_SECONDARY, bd=0, 
                         highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Настраиваем прокрутку
        scrollbar.config(command=canvas.yview)
        
        # Фрейм внутри канваса для сообщений (сетка сообщений)
        messages_frame = tk.Frame(canvas, bg=DARK_SECONDARY)
        canvas_window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")
        
        # Настраиваем изменение размера канваса и его содержимого
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        messages_frame.bind("<Configure>", on_frame_configure)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Разделяем фрейм на 2 колонки для более эффективного использования пространства
        messages_frame.columnconfigure(0, weight=1)
        messages_frame.columnconfigure(1, weight=1)
        
        # Создаем элементы управления для каждого сообщения в сетке
        self.message_fields = {}
        
        # Разделяем сообщения по колонкам
        messages = list(self.config_data.items())
        left_messages = messages[:len(messages)//2 + len(messages) % 2]
        right_messages = messages[len(messages)//2 + len(messages) % 2:]
        
        # Создаем левую колонку сообщений
        for i, (message_key, message_data) in enumerate(left_messages):
            self.create_message_editor(messages_frame, message_key, message_data, 0, i)
        
        # Создаем правую колонку сообщений
        for i, (message_key, message_data) in enumerate(right_messages):
            self.create_message_editor(messages_frame, message_key, message_data, 1, i)
    
    def create_message_editor(self, parent, message_key, message_data, col, row):
        """Создает редактор для одного сообщения"""
        # Создаем фрейм для сообщения
        message_frame = tk.Frame(parent, bg=DARK_SECONDARY, bd=1, relief=tk.GROOVE)
        message_frame.grid(row=row, column=col, sticky="nsew", padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Заголовок сообщения
        header = tk.Label(message_frame, text=message_key.replace("_", " "), 
                       font=FONT_SUBHEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(anchor="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Фрейм для текста сообщения
        text_frame = tk.Frame(message_frame, bg=DARK_SECONDARY)
        text_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Метка для текста
        text_label = tk.Label(text_frame, text="Текст:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        text_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Поле для ввода текста сообщения
        text_var = tk.StringVar(value=message_data.get("Text", ""))
        text_entry = ttk.Entry(text_frame, textvariable=text_var, width=60)
        text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Сохраняем переменную текста
        if message_key not in self.message_fields:
            self.message_fields[message_key] = {}
        self.message_fields[message_key]["Text"] = text_var
        
        # Обработчик изменения текста
        text_var.trace_add("write", lambda *args, k=message_key: self.update_message(k))
        
        # Фрейм для цвета
        color_frame = tk.Frame(message_frame, bg=DARK_SECONDARY)
        color_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Цвет сообщения
        color_label = tk.Label(color_frame, text="Цвет:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        color_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Получаем данные о цвете
        color_data = message_data.get("Color", {"Red": 255, "Green": 255, "Blue": 255})
        red = color_data.get("Red", 255)
        green = color_data.get("Green", 255)
        blue = color_data.get("Blue", 255)
        
        # Превью цвета
        color_hex = f'#{red:02x}{green:02x}{blue:02x}'
        color_preview = tk.Frame(color_frame, bg=color_hex, width=30, height=20, bd=1, relief=tk.SUNKEN)
        color_preview.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Поля для RGB
        rgb_frame = tk.Frame(color_frame, bg=DARK_SECONDARY)
        rgb_frame.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # R
        r_label = tk.Label(rgb_frame, text="R:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        r_label.grid(row=0, column=0, padx=(0, 2))
        r_var = tk.StringVar(value=str(red))
        r_entry = ttk.Entry(rgb_frame, textvariable=r_var, width=4)
        r_entry.grid(row=0, column=1, padx=(0, PADDING_SMALL))
        
        # G
        g_label = tk.Label(rgb_frame, text="G:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        g_label.grid(row=0, column=2, padx=(0, 2))
        g_var = tk.StringVar(value=str(green))
        g_entry = ttk.Entry(rgb_frame, textvariable=g_var, width=4)
        g_entry.grid(row=0, column=3, padx=(0, PADDING_SMALL))
        
        # B
        b_label = tk.Label(rgb_frame, text="B:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        b_label.grid(row=0, column=4, padx=(0, 2))
        b_var = tk.StringVar(value=str(blue))
        b_entry = ttk.Entry(rgb_frame, textvariable=b_var, width=4)
        b_entry.grid(row=0, column=5)
        
        # Кнопка выбора цвета
        choose_color_button = tk.Button(color_frame, text="Выбрать цвет", 
                                      bg=DARK_BG, fg=LIGHT_TEXT,
                                      command=lambda p=color_preview, rv=r_var, gv=g_var, bv=b_var, k=message_key: 
                                             self.choose_color(p, rv, gv, bv, k))
        choose_color_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Сохраняем переменные цвета
        self.message_fields[message_key]["Color"] = {
            "Red": r_var,
            "Green": g_var,
            "Blue": b_var
        }
        self.message_fields[message_key]["preview"] = color_preview
        
        # Обработчики изменения цвета
        r_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
        g_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
        b_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
    
    def choose_color(self, preview_widget, r_var, g_var, b_var, message_key):
        """Открывает диалог выбора цвета и обновляет RGB поля"""
        # Текущий цвет
        current_r = int(r_var.get()) if r_var.get().isdigit() else 0
        current_g = int(g_var.get()) if g_var.get().isdigit() else 0
        current_b = int(b_var.get()) if b_var.get().isdigit() else 0
        
        current_color = f'#{current_r:02x}{current_g:02x}{current_b:02x}'
        
        # Открываем диалог выбора цвета
        color = colorchooser.askcolor(color=current_color, title="Выберите цвет")
        
        # Если цвет выбран, обновляем переменные
        if color and color[0]:
            r, g, b = [int(c) for c in color[0]]
            r_var.set(str(r))
            g_var.set(str(g))
            b_var.set(str(b))
            
            # Обновляем предпросмотр цвета
            preview_widget.config(bg=color[1])
            
            # Обновляем конфигурацию
            self.update_message(message_key)
    
    def update_color_preview(self, preview_widget, r_var, g_var, b_var, message_key):
        """Обновляет предпросмотр цвета"""
        try:
            r = int(r_var.get())
            g = int(g_var.get())
            b = int(b_var.get())
            
            # Ограничиваем значения
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Обновляем предпросмотр
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            preview_widget.config(bg=color_hex)
            
            # Обновляем конфигурацию
            self.update_message(message_key)
        except ValueError:
            pass
    
    def update_message(self, message_key):
        """Обновляет данные сообщения в конфигурации"""
        if message_key not in self.message_fields:
            return
        
        message_fields = self.message_fields[message_key]
        
        # Текст сообщения
        text = message_fields["Text"].get()
        
        # Цвет сообщения
        try:
            red = int(message_fields["Color"]["Red"].get())
            green = int(message_fields["Color"]["Green"].get())
            blue = int(message_fields["Color"]["Blue"].get())
            
            # Ограничиваем значения
            red = max(0, min(255, red))
            green = max(0, min(255, green))
            blue = max(0, min(255, blue))
        except ValueError:
            red, green, blue = 255, 255, 255
        
        # Обновляем конфигурацию
        if message_key not in self.config_data:
            self.config_data[message_key] = {}
        
        self.config_data[message_key]["Text"] = text
        self.config_data[message_key]["Color"] = {
            "Red": red,
            "Green": green,
            "Blue": blue
        }

