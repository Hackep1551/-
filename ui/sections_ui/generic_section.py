import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class GenericSection(BaseSection):
    """Универсальный класс для отображения разделов без специальной обработки"""
    
    def setup_ui(self):
        """Создает стандартные поля для обычных секций"""
        row = 0
        
        for key, value in self.config_data.items():
            # Метка для поля
            label = tk.Label(self.parent, text=key, fg=LIGHT_TEXT, bg=DARK_SECONDARY,
                           font=FONT_NORMAL, anchor="w")
            label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            
            # Создаем соответствующий виджет ввода в зависимости от типа значения
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                field = ttk.Checkbutton(self.parent, variable=var)
                field.configure(command=lambda k=key, v=var: self.on_field_change(k, v))
                self.fields[key] = var
            elif isinstance(value, int):
                var = tk.StringVar(value=str(value))
                field = ttk.Entry(self.parent, textvariable=var, width=20)
                var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                self.fields[key] = var
            elif isinstance(value, float):
                var = tk.StringVar(value=str(value))
                field = ttk.Entry(self.parent, textvariable=var, width=20)
                var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                self.fields[key] = var
            elif isinstance(value, dict):
                # Для словарей создаем кнопку редактирования вложенного словаря
                var = tk.StringVar(value="<Редактировать вложенные поля>")
                field = ttk.Button(self.parent, text="Редактировать...", 
                                 command=lambda k=key, v=value: self.edit_nested_dict(k, v))
                self.fields[key] = value  # Сохраняем сам словарь
            elif isinstance(value, list):
                var = tk.StringVar(value=", ".join(map(str, value)))
                field = ttk.Entry(self.parent, textvariable=var, width=40)
                var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                self.fields[key] = var
            else:  # строка и другие типы
                var = tk.StringVar(value=str(value))
                field = ttk.Entry(self.parent, textvariable=var, width=40)
                var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
                self.fields[key] = var
            
            field.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            row += 1
            
        # Настройка весов для правильного растяжения
        self.parent.grid_columnconfigure(1, weight=1)
    
    def edit_nested_dict(self, key, value):
        """Открывает диалог для редактирования вложенного словаря"""
        messagebox.showinfo("Редактирование вложенных полей", 
                          f"Редактирование вложенных полей для {key} пока не реализовано.")
