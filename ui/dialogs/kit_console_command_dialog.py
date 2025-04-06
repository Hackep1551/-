import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *  # Ensure FONT_REGULAR is defined in this module or imported here

# Define FONT_REGULAR if not imported
FONT_REGULAR = ("Arial", 12)  # Example font definition, adjust as needed

class KitConsoleCommandDialog:
    """Диалоговое окно для добавления/редактирования консольных команд в китах"""
    
    def __init__(self, parent, on_save=None, command_data=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            on_save: функция обратного вызова при сохранении
            command_data: данные о редактируемой команде (если редактирование)
        """
        self.parent = parent
        self.on_save = on_save
        self.command_data = command_data or ""
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить консольную команду" if not command_data else "Редактировать консольную команду")
        self.dialog.geometry("600x200")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(True, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
            self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поле
        if self.command_data:
            self.command_var.set(self.command_data)
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="Введите консольную команду:",
            font=FONT_REGULAR,
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        title_label.pack(anchor="w", pady=(0, PADDING_SMALL))
        
        # Поле для ввода команды
        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(main_frame, textvariable=self.command_var, width=60)
        command_entry.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Подсказка
        hint_label = tk.Label(
            main_frame,
            text="Подсказка: используйте {steamid} или {eosid} для подстановки ID игрока",
            font=FONT_SMALL,
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        hint_label.pack(anchor="w", pady=(0, PADDING_MEDIUM))
        
        # Кнопки
        buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(PADDING_MEDIUM, 0))
        
        cancel_button = tk.Button(
            buttons_frame,
            text="Отмена",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(PADDING_SMALL, 0))
        
        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            bg=ORANGE_PRIMARY,
            fg=DARK_BG,
            command=self.save_command
        )
        save_button.pack(side=tk.RIGHT)
    
    def save_command(self):
        """Сохраняет введенную консольную команду"""
        command = self.command_var.get().strip()
        
        # Проверяем, не пустая ли строка
        if not command:
            messagebox.showwarning("Предупреждение", "Команда не может быть пустой")
            return
        
        # Закрываем диалог и вызываем callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(command)
