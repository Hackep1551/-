import tkinter as tk
from tkinter import ttk
from ui.constants import *
from utils.config_manager import update_memory_config
from utils.memory_storage import memory_config

class BaseSection:
    """Базовый класс для всех разделов конфигурации"""
    
    def __init__(self, parent, section_name, config_data):
        """
        Инициализирует базовый класс раздела
        
        Args:
            parent: Родительский виджет для размещения элементов раздела
            section_name: Имя раздела в конфигурации
            config_data: Данные конфигурации для этого раздела
        """
        self.parent = parent
        self.section_name = section_name
        self.config_data = config_data if config_data is not None else {}
        self.fields = {}  # Инициализация словаря для хранения полей ввода
        
    def setup_ui(self):
        """Метод для настройки пользовательского интерфейса раздела"""
        # Базовая реализация показывает сообщение об отсутствии доступных настроек
        message = tk.Label(
            self.parent,
            text=f"Нет доступных настроек для раздела '{self.section_name}'",
            padx=20,
            pady=20
        )
        message.pack(expand=True)
        
    def on_field_change(self, key, value, delete=False):
        """
        Обрабатывает изменение поля в конфигурации
        
        Args:
            key: Ключ изменяемого поля
            value: Новое значение поля (None для удаления)
            delete: Если True, поле будет удалено из конфигурации
        """
        # Убедимся, что раздел существует в памяти
        if self.section_name not in memory_config:
            memory_config[self.section_name] = {}
        
        if delete:
            if key in memory_config[self.section_name]:
                del memory_config[self.section_name][key]
        else:
            memory_config[self.section_name][key] = value
        
        # Обновляем локальные данные для отображения в UI
        self.config_data = memory_config[self.section_name]
    
    def collect_field_data(self):
        """Собирает данные из полей ввода и преобразует их в соответствующие типы"""
        updated_data = {}
        
        for key, var in self.fields.items():
            if isinstance(var, tk.Variable):
                value = var.get()
                
                # Преобразуем значения обратно в соответствующие типы
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
                elif isinstance(original_value, list):
                    # Разделяем строку по запятым
                    items = [item.strip() for item in value.split(",")]
                    if all(item.isdigit() for item in items if item):
                        updated_data[key] = [int(item) for item in items if item]
                    else:
                        updated_data[key] = items
                else:
                    updated_data[key] = value
            else:
                # Для сложных типов, которые не являются переменными tk
                updated_data[key] = var
                
        return updated_data
