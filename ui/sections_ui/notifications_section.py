import tkinter as tk
from tkinter import ttk, colorchooser
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from utils.memory_storage import memory_config

class NotificationsSection(BaseSection):
    """Класс для отображения настроек раздела Notifications"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела Notifications"""
        # Создаем главный фрейм, занимающий все доступное пространство
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок в верхней части окна
        header_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        header_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        header = tk.Label(header_frame, text="Настройка игровых уведомлений", 
                        font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(side=tk.LEFT)
        
        description = tk.Label(header_frame, text="Настройте текст, цвет и параметры отображения уведомлений", 
                             fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        description.pack(side=tk.LEFT, padx=(PADDING_MEDIUM, 0))
        
        # Создаем фрейм с прокруткой для всех уведомлений
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
        
        # Фрейм внутри канваса для уведомлений (сетка уведомлений)
        notifications_frame = tk.Frame(canvas, bg=DARK_SECONDARY)
        canvas_window = canvas.create_window((0, 0), window=notifications_frame, anchor="nw")
        
        # Настраиваем изменение размера канваса и его содержимого
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        notifications_frame.bind("<Configure>", on_frame_configure)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Создаем элементы управления для каждого уведомления
        # Разделяем на две колонки для более эффективного использования пространства
        notifications_frame.columnconfigure(0, weight=1)
        notifications_frame.columnconfigure(1, weight=1)
        
        # Создаем элементы управления для каждого уведомления в сетке
        self.notification_fields = {}
        
        # Распределяем уведомления по колонкам
        notifications = list(self.config_data.items())
        left_notifications = notifications[:len(notifications)//2 + len(notifications) % 2]
        right_notifications = notifications[len(notifications)//2 + len(notifications) % 2:]
        
        # Создаем левую колонку уведомлений
        for i, (notification_key, notification_data) in enumerate(left_notifications):
            self.create_notification_editor(notifications_frame, notification_key, notification_data, 0, i)
        
        # Создаем правую колонку уведомлений
        for i, (notification_key, notification_data) in enumerate(right_notifications):
            self.create_notification_editor(notifications_frame, notification_key, notification_data, 1, i)
    
    def create_notification_editor(self, parent, notification_key, notification_data, col, row):
        """Создает редактор для одного уведомления"""
        # Создаем фрейм для уведомления
        notification_frame = tk.Frame(parent, bg=DARK_SECONDARY, bd=1, relief=tk.GROOVE)
        notification_frame.grid(row=row, column=col, sticky="nsew", padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Настраиваем, чтобы фрейм растягивался при изменении размеров
        parent.rowconfigure(row, weight=1)
        
        # Заголовок уведомления
        header = tk.Label(notification_frame, text=notification_key.replace("_", " "), 
                       font=FONT_SUBHEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(anchor="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Фрейм для текста уведомления
        text_frame = tk.Frame(notification_frame, bg=DARK_SECONDARY)
        text_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Метка для текста
        text_label = tk.Label(text_frame, text="Текст:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        text_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Поле для ввода текста уведомления
        text_var = tk.StringVar(value=notification_data.get("Text", ""))
        text_entry = ttk.Entry(text_frame, textvariable=text_var, width=60)
        text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Сохраняем переменную текста
        if notification_key not in self.notification_fields:
            self.notification_fields[notification_key] = {}
        self.notification_fields[notification_key]["Text"] = text_var
        
        # Обработчик изменения текста
        text_var.trace_add("write", lambda *args, k=notification_key: self.update_notification(k))
        
        # Фрейм для параметров отображения
        params_frame = tk.Frame(notification_frame, bg=DARK_SECONDARY)
        params_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Размер текста
        size_label = tk.Label(params_frame, text="Размер:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        size_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        size_var = tk.StringVar(value=str(notification_data.get("Size", 3)))
        size_entry = ttk.Entry(params_frame, textvariable=size_var, width=5)
        size_entry.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        # Время отображения
        time_label = tk.Label(params_frame, text="Время отображения (сек):", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        time_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        time_var = tk.StringVar(value=str(notification_data.get("Display_Time", 6)))
        time_entry = ttk.Entry(params_frame, textvariable=time_var, width=5)
        time_entry.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        # Сохраняем переменные параметров
        self.notification_fields[notification_key]["Size"] = size_var
        self.notification_fields[notification_key]["Display_Time"] = time_var
        
        # Обработчики изменения параметров
        size_var.trace_add("write", lambda *args, k=notification_key: self.update_notification(k))
        time_var.trace_add("write", lambda *args, k=notification_key: self.update_notification(k))
        
        # Опция отправки как сообщения (если есть в данных)
        if "Send_As_Message" in notification_data:
            send_as_message_var = tk.BooleanVar(value=notification_data.get("Send_As_Message", False))
            send_as_message_check = ttk.Checkbutton(
                notification_frame, 
                text="Отправлять как сообщение в чат", 
                variable=send_as_message_var
            )
            send_as_message_check.pack(anchor="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.notification_fields[notification_key]["Send_As_Message"] = send_as_message_var
            
            # Обработчик изменения
            send_as_message_var.trace_add("write", lambda *args, k=notification_key: self.update_notification(k))
        
        # Фрейм для цвета
        color_frame = tk.Frame(notification_frame, bg=DARK_SECONDARY)
        color_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Цвет уведомления
        color_label = tk.Label(color_frame, text="Цвет:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        color_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Получаем данные о цвете
        color_data = notification_data.get("Color", {"Red": 255, "Green": 255, "Blue": 255})
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
                                      command=lambda p=color_preview, rv=r_var, gv=g_var, bv=b_var, k=notification_key: 
                                             self.choose_color(p, rv, gv, bv, k))
        choose_color_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Сохраняем переменные цвета
        self.notification_fields[notification_key]["Color"] = {
            "Red": r_var,
            "Green": g_var,
            "Blue": b_var
        }
        self.notification_fields[notification_key]["preview"] = color_preview
        
        # Обработчики изменения цвета
        r_var.trace_add("write", lambda *args, k=notification_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
        g_var.trace_add("write", lambda *args, k=notification_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
        b_var.trace_add("write", lambda *args, k=notification_key, p=color_preview, 
                       rv=r_var, gv=g_var, bv=b_var: 
                       self.update_color_preview(p, rv, gv, bv, k))
    
    def choose_color(self, preview_widget, r_var, g_var, b_var, notification_key):
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
            self.update_notification(notification_key)
    
    def update_color_preview(self, preview_widget, r_var, g_var, b_var, notification_key):
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
            self.update_notification(notification_key)
        except ValueError:
            pass
    
    def update_notification(self, notification_key):
        """Обновляет данные уведомления в конфигурации"""
        if notification_key not in self.notification_fields:
            return
        
        fields = self.notification_fields[notification_key]
        
        # Текст уведомления
        text = fields["Text"].get()
        
        # Размер текста
        try:
            size = int(fields["Size"].get())
        except ValueError:
            size = 3  # По умолчанию
        
        # Время отображения
        try:
            display_time = int(fields["Display_Time"].get())
        except ValueError:
            display_time = 6  # По умолчанию
        
        # Цвет уведомления
        try:
            red = int(fields["Color"]["Red"].get())
            green = int(fields["Color"]["Green"].get())
            blue = int(fields["Color"]["Blue"].get())
            
            # Ограничиваем значения
            red = max(0, min(255, red))
            green = max(0, min(255, green))
            blue = max(0, min(255, blue))
        except ValueError:
            red, green, blue = 255, 255, 255
        
        # Проверяем, существует ли секция Notifications в memory_config
        if "Notifications" not in memory_config:
            memory_config["Notifications"] = {}
        
        # Обновляем конфигурацию в памяти
        if notification_key not in memory_config["Notifications"]:
            memory_config["Notifications"][notification_key] = {}
        
        memory_config["Notifications"][notification_key]["Text"] = text
        memory_config["Notifications"][notification_key]["Size"] = size
        memory_config["Notifications"][notification_key]["Display_Time"] = display_time
        memory_config["Notifications"][notification_key]["Color"] = {
            "Red": red,
            "Green": green,
            "Blue": blue
        }
        
        # Проверяем наличие опции Send_As_Message
        if "Send_As_Message" in fields:
            memory_config["Notifications"][notification_key]["Send_As_Message"] = fields["Send_As_Message"].get()
        
        # Обновляем локальные данные для отображения в UI
        self.config_data = memory_config["Notifications"]
