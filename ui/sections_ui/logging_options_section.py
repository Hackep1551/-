import tkinter as tk
from tkinter import ttk
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class LoggingOptionsSection(BaseSection):
    """Класс для отображения настроек Logging Options"""
    
    def setup_ui(self):
        """Настройка интерфейса для LoggingOptionsSection"""
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        header = tk.Label(main_frame, text="Настройки журналирования", 
                       font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Разделяем экран на две части: левую с чекбоксами и правую с форматами
        split_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        split_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая часть с чекбоксами
        left_frame = tk.Frame(split_frame, bg=DARK_SECONDARY)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING_MEDIUM))
        
        # Правая часть с форматами
        right_frame = tk.Frame(split_frame, bg=DARK_SECONDARY)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Настраиваем левую часть - опции журналирования
        self.setup_logging_checkboxes(left_frame)
        
        # Настраиваем правую часть - форматы сообщений
        self.setup_logging_formats(right_frame)
    
    def setup_logging_checkboxes(self, parent_frame):
        """Настраивает чекбоксы для опций журналирования"""
        # Заголовок
        header = tk.Label(parent_frame, text="Опции журналирования", 
                       font=FONT_SUBHEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Основные опции журналирования
        checkboxes_frame = tk.Frame(parent_frame, bg=DARK_SECONDARY)
        checkboxes_frame.pack(fill=tk.X)
        
        # Список чекбоксов для создания
        logging_options = [
            {"key": "Enable_Log_File", "text": "Включить журналирование в файл"},
            {"key": "Enable_Discord_Log", "text": "Включить журналирование в Discord"},
            {"key": "Log_Buy", "text": "Журналировать покупки"},
            {"key": "Log_Buy_Kits", "text": "Журналировать покупки наборов"},
            {"key": "Log_Use_Kits", "text": "Журналировать использование наборов"},
            {"key": "Log_Points_Trading", "text": "Журналировать обмен очками"}
        ]
        
        # Создаем чекбоксы
        for i, option in enumerate(logging_options):
            key = option["key"]
            text = option["text"]
            
            var = tk.BooleanVar(value=self.config_data.get(key, False))
            checkbox = ttk.Checkbutton(
                checkboxes_frame, 
                text=text, 
                variable=var
            )
            checkbox.grid(row=i, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
            
            # Сохраняем переменную и привязываем функцию обновления
            self.fields[key] = var
            var.trace_add("write", lambda name, index, mode, key=key, var=var: 
                        self.on_field_change(key, var.get()))
        
        # Поле для Discord webhook URL
        webhook_frame = tk.Frame(parent_frame, bg=DARK_SECONDARY)
        webhook_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        webhook_label = tk.Label(webhook_frame, text="Discord webhook URL:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        webhook_label.pack(anchor="w")
        
        webhook_var = tk.StringVar(value=self.config_data.get("Discord_Log_Webhook", ""))
        webhook_entry = ttk.Entry(webhook_frame, textvariable=webhook_var, width=40)
        webhook_entry.pack(fill=tk.X, pady=(PADDING_SMALL, 0))
        
        # Сохраняем переменную и привязываем функцию обновления
        self.fields["Discord_Log_Webhook"] = webhook_var
        webhook_var.trace_add("write", lambda name, index, mode: 
                            self.on_field_change("Discord_Log_Webhook", webhook_var.get()))
    
    def setup_logging_formats(self, parent_frame):
        """Настраивает форматы сообщений журналирования"""
        # Заголовок
        header = tk.Label(parent_frame, text="Форматы сообщений", 
                       font=FONT_SUBHEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Создаем фрейм для полей ввода форматов
        formats_frame = tk.Frame(parent_frame, bg=DARK_SECONDARY)
        formats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Список форматов для создания
        format_fields = [
            {"key": "AddPointsFormat", "label": "Формат добавления очков:"},
            {"key": "BuyLogFormat", "label": "Формат покупки:"},
            {"key": "SellLogFormat", "label": "Формат продажи:"},
            {"key": "BuyKitsFormat", "label": "Формат покупки набора:"},
            {"key": "UseKitLogFormat", "label": "Формат использования набора:"},
            {"key": "TradeLogFormat", "label": "Формат обмена очками:"}
        ]
        
        # Создаем поля ввода для форматов
        for i, field in enumerate(format_fields):
            key = field["key"]
            label_text = field["label"]
            
            # Создаем метку
            label = tk.Label(formats_frame, text=label_text, fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=i*2, column=0, sticky="w", padx=PADDING_SMALL, pady=(PADDING_SMALL, 0))
            
            # Получаем значение из конфигурации
            value = self.config_data.get(key, "")
            
            # Создаем переменную для поля
            var = tk.StringVar(value=value)
            
            # Создаем поле ввода
            entry = ttk.Entry(formats_frame, textvariable=var, width=50)
            entry.grid(row=i*2+1, column=0, sticky="ew", padx=PADDING_SMALL, pady=(0, PADDING_SMALL))
            
            # Сохраняем переменную и привязываем функцию обновления
            self.fields[key] = var
            var.trace_add("write", lambda name, index, mode, key=key, var=var: 
                        self.on_field_change(key, var.get()))
