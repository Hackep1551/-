import tkinter as tk
from tkinter import ttk
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class MySQLSection(BaseSection):
    """Класс для отображения настроек MySQL"""
    
    def setup_ui(self):
        """Настройка интерфейса для MySQLSection"""
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        header = tk.Label(main_frame, text="Настройки MySQL подключения", 
                       font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Создаем поля для настройки подключения к MySQL
        fields_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        fields_frame.pack(fill=tk.BOTH, pady=PADDING_SMALL)
        
        # Список полей для создания
        mysql_fields = [
            {"key": "HostAdress", "label": "Хост:", "default": ""},
            {"key": "Username", "label": "Имя пользователя:", "default": ""},
            {"key": "Password", "label": "Пароль:", "default": "", "show": "*"},
            {"key": "DataBaseName", "label": "Название базы данных:", "default": ""},
            {"key": "Port", "label": "Порт:", "default": 3306},
        ]
        
        # Создаем поля для каждого параметра
        row = 0
        for field in mysql_fields:
            key = field["key"]
            label_text = field["label"]
            default = field["default"]
            show = field.get("show", None)
            
            # Создаем метку
            label = tk.Label(fields_frame, text=label_text, fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=row, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
            
            # Получаем значение из конфигурации или используем значение по умолчанию
            value = self.config_data.get(key, default)
            
            # Создаем переменную для поля
            var = tk.StringVar(value=str(value))
            
            # Создаем поле ввода
            if show:
                entry = ttk.Entry(fields_frame, textvariable=var, width=30, show=show)
            else:
                entry = ttk.Entry(fields_frame, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
            
            # Сохраняем переменную и привязываем функцию обновления
            self.fields[key] = var
            var.trace_add("write", lambda name, index, mode, key=key, var=var: self.update_field(key, var))
            
            row += 1
    
    def update_field(self, key, var):
        """Обновляет поле в конфигурации при изменении значения в интерфейсе"""
        value = var.get()
        
        # Преобразуем значение к нужному типу
        if key == "Port":
            try:
                value = int(value)
            except ValueError:
                value = 3306
        
        # Обновляем конфигурацию
        self.on_field_change(key, value)
