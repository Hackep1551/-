import tkinter as tk
from tkinter import ttk, colorchooser
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class LotterySection(BaseSection):
    def setup_ui(self):
        """Настройка интерфейса для раздела Lottery"""
        # Создаем фрейм с вкладками для основных настроек и сообщений
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Вкладка основных настроек
        settings_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(settings_frame, text="Основные настройки")
        
        # Вкладка сообщений
        messages_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(messages_frame, text="Сообщения")
        
        # Настраиваем основные поля
        row = 0
        self.lottery_fields = {}
        
        # Описания для основных полей
        descriptions = {
            "Enable_Lottery": "Включить/выключить систему лотереи",
            "Buy_Ticket_Command": "Команда для покупки билета",
            "Announce_Interval_Seconds": "Интервал объявления в секундах",
            "Timespan_In_Minutes": "Продолжительность лотереи в минутах",
            "Minimum_Participants": "Минимальное количество участников",
            "Win_Percentage": "Процент выигрыша (от общего пула)",
            "Entry_Price": "Цена входного билета",
            "Interval_Minimum_Minutes": "Минимальный интервал между лотереями (минуты)",
            "Interval_Maximum_Minutes": "Максимальный интервал между лотереями (минуты)",
            "Lottery_Ingame_Name": "Название лотереи в игре"
        }
        
        # Основные настройки
        for key, value in self.config_data.items():
            if key != "Messages":  # Messages обрабатываем отдельно
                # Метка для поля
                label = tk.Label(settings_frame, text=key, fg=LIGHT_TEXT, bg=DARK_SECONDARY,
                               font=FONT_NORMAL, anchor="w")
                label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
                
                # Создаем соответствующий виджет ввода
                if isinstance(value, bool):
                    var = tk.BooleanVar(value=value)
                    field = ttk.Checkbutton(settings_frame, variable=var)
                    field.configure(command=lambda k=key, v=var: self.on_field_change(k, v))
                    self.lottery_fields[key] = var
                elif isinstance(value, int):
                    var = tk.StringVar(value=str(value))
                    field = ttk.Entry(settings_frame, textvariable=var, width=20)
                    var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                    self.lottery_fields[key] = var
                elif isinstance(value, float):
                    var = tk.StringVar(value=str(value))
                    field = ttk.Entry(settings_frame, textvariable=var, width=20)
                    var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                    self.lottery_fields[key] = var
                elif isinstance(value, str):
                    var = tk.StringVar(value=value)
                    field = ttk.Entry(settings_frame, textvariable=var, width=40)
                    var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                    self.lottery_fields[key] = var
                
                field.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
                
                # Добавляем описание, если есть
                if key in descriptions:
                    desc_label = tk.Label(settings_frame, text=descriptions[key], 
                                        fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL, anchor="w")
                    desc_label.grid(row=row+1, column=0, columnspan=2, sticky="w", 
                                  padx=(PADDING_LARGE*2, PADDING_MEDIUM))
                    row += 2
                else:
                    row += 1
        
        # Настройка весов для правильного растяжения
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Настраиваем раздел сообщений
        self.setup_lottery_messages(messages_frame)
        
        # Добавляем все поля в основной словарь fields
        self.fields.update(self.lottery_fields)
    
    def setup_lottery_messages(self, parent_frame):
        """Настройка интерфейса для сообщений лотереи"""
        # Заголовок
        header_label = tk.Label(parent_frame, text="Настройка сообщений лотереи", 
                              fg=ORANGE_PRIMARY, bg=DARK_SECONDARY,
                              font=FONT_SUBHEADER)
        header_label.pack(anchor="w", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Фрейм для списка сообщений (с прокруткой)
        canvas_frame = tk.Frame(parent_frame, bg=DARK_SECONDARY)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM)
        
        # Добавляем вертикальную прокрутку
        v_scrollbar = tk.Scrollbar(canvas_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаём канвас
        canvas = tk.Canvas(canvas_frame, bg=DARK_SECONDARY, 
                         bd=0, highlightthickness=0,
                         yscrollcommand=v_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=canvas.yview)
        
        # Фрейм внутри канваса для сообщений
        messages_container = tk.Frame(canvas, bg=DARK_SECONDARY)
        canvas_window = canvas.create_window((0, 0), window=messages_container, anchor="nw", tags="messages_container")
        
        # Настраиваем изменение размера канваса при изменении размера фрейма
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        messages_container.bind("<Configure>", on_frame_configure)
        
        # Настраиваем изменение ширины фрейма при изменении ширины канваса
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Получаем словарь сообщений
        messages = self.config_data.get("Messages", {})
        self.lottery_messages = {}
        
        # Создаем элементы управления для каждого сообщения
        for message_key, message_data in messages.items():
            message_frame = tk.Frame(messages_container, bg=DARK_SECONDARY, 
                                   bd=1, relief=tk.GROOVE)
            message_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            
            # Заголовок сообщения
            message_header = tk.Label(message_frame, text=message_key, 
                                    fg=LIGHT_TEXT, bg=DARK_SECONDARY,
                                    font=FONT_SUBHEADER)
            message_header.pack(anchor="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Редактирование текста
            text_frame = tk.Frame(message_frame, bg=DARK_SECONDARY)
            text_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            text_label = tk.Label(text_frame, text="Текст:", fg=LIGHT_TEXT, 
                                bg=DARK_SECONDARY, font=FONT_NORMAL)
            text_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
            
            message_text = message_data.get("Text", "")
            text_var = tk.StringVar(value=message_text)
            text_entry = ttk.Entry(text_frame, textvariable=text_var, width=60)
            text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Получаем цвет
            color_data = message_data.get("Color", {"Red": 255, "Green": 255, "Blue": 255})
            red = color_data.get("Red", 255)
            green = color_data.get("Green", 255)
            blue = color_data.get("Blue", 255)
            
            # Рамка для цвета
            color_frame = tk.Frame(message_frame, bg=DARK_SECONDARY)
            color_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            color_label = tk.Label(color_frame, text="Цвет:", fg=LIGHT_TEXT, 
                                 bg=DARK_SECONDARY, font=FONT_NORMAL)
            color_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
            
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
                                          command=lambda p=color_preview, rv=r_var, gv=g_var, bv=b_var: 
                                                 self.choose_color(p, rv, gv, bv))
            choose_color_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            
            # Сохраняем ссылки на переменные
            self.lottery_messages[message_key] = {
                "Text": text_var,
                "Color": {
                    "Red": r_var,
                    "Green": g_var,
                    "Blue": b_var
                },
                "preview": color_preview
            }
            
            # Добавляем обновление при изменении текста
            text_var.trace_add("write", lambda *args, k=message_key: 
                              self.update_lottery_message(k))
            
            # Добавляем обновление при изменении цвета
            r_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                           rv=r_var, gv=g_var, bv=b_var: 
                           self.update_color_preview(p, rv, gv, bv, k))
            g_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                           rv=r_var, gv=g_var, bv=b_var: 
                           self.update_color_preview(p, rv, gv, bv, k))
            b_var.trace_add("write", lambda *args, k=message_key, p=color_preview, 
                           rv=r_var, gv=g_var, bv=b_var: 
                           self.update_color_preview(p, rv, gv, bv, k))
    
    def choose_color(self, preview_widget, r_var, g_var, b_var):
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
    
    def update_color_preview(self, preview_widget, r_var, g_var, b_var, message_key=None):
        """Обновляет предпросмотр цвета и конфигурацию лотереи"""
        # Проверяем, что значения RGB корректны
        try:
            r = int(r_var.get())
            g = int(g_var.get())
            b = int(b_var.get())
            
            # Ограничиваем значения от 0 до 255
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Обновляем предпросмотр
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            preview_widget.config(bg=color_hex)
            
            # Если указан ключ сообщения, обновляем конфигурацию
            if message_key:
                self.update_lottery_message(message_key)
        except ValueError:
            pass  # Игнорируем некорректные значения
    
    def update_lottery_message(self, message_key):
        """Обновляет конфигурацию сообщения лотереи"""
        message_data = self.lottery_messages.get(message_key)
        if not message_data:
            return
        
        # Получаем текст и цвет из интерфейса
        text = message_data["Text"].get()
        try:
            red = int(message_data["Color"]["Red"].get())
            green = int(message_data["Color"]["Green"].get())
            blue = int(message_data["Color"]["Blue"].get())
            
            # Ограничиваем значения от 0 до 255
            red = max(0, min(255, red))
            green = max(0, min(255, green))
            blue = max(0, min(255, blue))
        except ValueError:
            # По умолчанию белый, если некорректные значения
            red, green, blue = 255, 255, 255
        
        # Обновляем конфигурацию в памяти
        if "Messages" not in self.config_data:
            self.config_data["Messages"] = {}
            
        if message_key not in self.config_data["Messages"]:
            self.config_data["Messages"][message_key] = {}
            
        self.config_data["Messages"][message_key]["Text"] = text
        self.config_data["Messages"][message_key]["Color"] = {
            "Red": red,
            "Green": green,
            "Blue": blue
        }
        
        # Обновляем данные в памяти
        self.on_field_change("Messages", self.config_data["Messages"])
    
    def collect_field_data(self):
        """Собирает данные из полей ввода с учетом специальной обработки для лотереи"""
        updated_data = {}
        
        # Копируем основную структуру конфига
        for key in self.config_data:
            updated_data[key] = self.config_data[key]
        
        # Обновляем основные настройки из полей
        for key, var in self.lottery_fields.items():
            value = var.get()
            original_value = self.config_data[key]
            
            if isinstance(original_value, bool):
                updated_data[key] = bool(value)
            elif isinstance(original_value, int):
                try:
                    updated_data[key] = int(value)
                except ValueError:
                    updated_data[key] = 0
            elif isinstance(original_value, float):
                try:
                    updated_data[key] = float(value)
                except ValueError:
                    updated_data[key] = 0.0
            else:
                updated_data[key] = value
        
        # Сообщения уже обновлены через update_lottery_message
        return updated_data
