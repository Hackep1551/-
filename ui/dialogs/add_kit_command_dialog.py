import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *

# Define FONT_BOLD if not already defined in ui.constants
FONT_BOLD = ("Arial", 10, "bold")

class AddKitCommandDialog:
    """Класс диалогового окна для добавления консольной команды в набор"""
    
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
        self.result = None
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить консольную команду")
        self.dialog.geometry("700x250")  # Увеличил размер диалога
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if hasattr(parent, "winfo_x") and hasattr(parent, "winfo_width"):
            x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 250) // 2
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
        
        # Поле для ввода команды
        command_label = tk.Label(main_frame, text="Консольная команда:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        command_label.pack(anchor="w")
        
        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(main_frame, textvariable=self.command_var, width=80)  # Увеличил ширину
        command_entry.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Примеры команд
        examples_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        examples_frame.pack(fill=tk.X, pady=PADDING_SMALL, anchor="w")
        
        examples_label = tk.Label(examples_frame, text="Примеры команд:", bg=DARK_SECONDARY, fg=LIGHT_TEXT, font=FONT_BOLD)
        examples_label.pack(anchor="w")
        
        example1 = "woolyitem {steamid} Blueprint'/Game/Path/To/Item.Item' 1 5 0 200 200 0"
        example2 = "admincheat GiveItemToPlayer {steamid} 0 1 0 0 Blueprint'/Game/Path/To/Item.Item'"
        example3 = "admincheat SpawnDino Blueprint'/Game/Path/To/Dino.Dino' 150 0 0 1"
        
        example1_label = tk.Label(examples_frame, text=example1, bg=DARK_SECONDARY, fg=GRAY_TEXT, wraplength=650)
        example1_label.pack(anchor="w")
        
        example2_label = tk.Label(examples_frame, text=example2, bg=DARK_SECONDARY, fg=GRAY_TEXT, wraplength=650)
        example2_label.pack(anchor="w")
        
        example3_label = tk.Label(examples_frame, text=example3, bg=DARK_SECONDARY, fg=GRAY_TEXT, wraplength=650)
        example3_label.pack(anchor="w")
        
        # Информационный текст
        info_text = """
        Подсказка: используйте {steamid} или {eosid} в команде для подстановки ID игрока.
        Формат Blueprint: Blueprint'/Game/Path/To/Item.Item' или Blueprint'/Game/Path/To/Dino.Dino'
        """
        info_label = tk.Label(main_frame, text=info_text, bg=DARK_SECONDARY, fg=GRAY_TEXT, justify=tk.LEFT, wraplength=650)
        info_label.pack(pady=PADDING_MEDIUM)
        
        # Кнопки
        buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
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
        """Сохраняет данные о команде"""
        command = self.command_var.get()
        
        if not command:
            messagebox.showerror("Ошибка", "Команда не может быть пустой")
            return
        
        self.result = command
        
        # Закрываем диалог и вызываем callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(command)
