import tkinter as tk
from tkinter import ttk
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class PointsStealingSection(BaseSection):
    """Класс для отображения настроек Points Stealing"""
    
    def setup_ui(self):
        """Настройка интерфейса для PointsStealingSection"""
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        header = tk.Label(main_frame, text="Настройки кражи очков при убийствах", 
                       font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Описание
        description = tk.Label(main_frame, 
                             text="Настройте параметры кражи очков при убийстве игроков", 
                             fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        description.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Создаем настройки
        settings_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        settings_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Включить/выключить кражу очков
        enable_var = tk.BooleanVar(value=self.config_data.get("Enable", False))
        enable_checkbox = ttk.Checkbutton(
            settings_frame, 
            text="Включить кражу очков при убийстве", 
            variable=enable_var
        )
        enable_checkbox.grid(row=0, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL, columnspan=2)
        self.fields["Enable"] = enable_var
        enable_var.trace_add("write", lambda *args: self.on_field_change("Enable", enable_var.get()))
        
        # Процент крадущихся очков
        steal_label = tk.Label(settings_frame, text="Процент кражи очков (0.01 = 1%):", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        steal_label.grid(row=1, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        steal_var = tk.StringVar(value=str(self.config_data.get("Points_Stolen_On_Kill", 0.03)))
        steal_entry = ttk.Entry(settings_frame, textvariable=steal_var, width=10)
        steal_entry.grid(row=1, column=1, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.fields["Points_Stolen_On_Kill"] = steal_var
        steal_var.trace_add("write", lambda *args: self.update_steal_percentage())
        
        # Множитель награды
        multiplier_label = tk.Label(settings_frame, text="Множитель итоговой награды:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        multiplier_label.grid(row=2, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        multiplier_var = tk.StringVar(value=str(self.config_data.get("Final_Reward_Multiplier", 1)))
        multiplier_entry = ttk.Entry(settings_frame, textvariable=multiplier_var, width=10)
        multiplier_entry.grid(row=2, column=1, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.fields["Final_Reward_Multiplier"] = multiplier_var
        multiplier_var.trace_add("write", lambda *args: self.update_multiplier())
    
    def update_steal_percentage(self):
        """Обновляет значение процента кражи в конфигурации"""
        try:
            percentage = float(self.fields["Points_Stolen_On_Kill"].get())
            self.on_field_change("Points_Stolen_On_Kill", percentage)
        except ValueError:
            pass
    
    def update_multiplier(self):
        """Обновляет значение множителя в конфигурации"""
        try:
            multiplier = float(self.fields["Final_Reward_Multiplier"].get())
            self.on_field_change("Final_Reward_Multiplier", multiplier)
        except ValueError:
            pass
