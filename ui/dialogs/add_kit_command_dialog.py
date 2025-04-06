import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *  # Ensure FONT_REGULAR is defined in this module or add it below

# Define FONT_REGULAR if not imported
FONT_REGULAR = ("Arial", 12)  # Example font definition
from ui.dialogs.kit_console_command_dialog import KitConsoleCommandDialog

class AddKitCommandDialog:
    """Диалоговое окно для добавления/редактирования консольных команд в киты"""
    
    def __init__(self, parent, on_save=None, commands=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            on_save: функция обратного вызова при сохранении
            commands: список существующих команд (если редактирование)
        """
        self.parent = parent
        self.on_save = on_save
        self.commands_list = commands or []
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Управление консольными командами")
        self.dialog.geometry("700x500")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 500) // 2
            self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Заполняем список команд, если они были переданы
        if self.commands_list:
            self.refresh_commands_list()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="Консольные команды кита",
            font=FONT_HEADER,
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        title_label.pack(anchor="w", pady=(0, PADDING_MEDIUM))
        
        # Список команд
        list_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        self.commands_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, font=FONT_REGULAR)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.commands_listbox.yview)
        self.commands_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.commands_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Двойной клик для редактирования
        self.commands_listbox.bind("<Double-1>", self.edit_command)
        
        # Подсказка
        hint_label = tk.Label(
            main_frame,
            text="Подсказка: используйте {steamid} или {eosid} для подстановки ID игрока",
            font=FONT_SMALL,
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        hint_label.pack(anchor="w", pady=(PADDING_SMALL, PADDING_MEDIUM))
        
        # Кнопки управления
        buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        add_button = tk.Button(
            buttons_frame,
            text="Добавить команду",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.add_command
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        edit_button = tk.Button(
            buttons_frame,
            text="Редактировать",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.edit_command
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        remove_button = tk.Button(
            buttons_frame,
            text="Удалить",
            bg=RED_BTN,
            fg=LIGHT_TEXT,
            command=self.remove_command
        )
        remove_button.pack(side=tk.LEFT)
        
        # Кнопки диалога
        dialog_buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        dialog_buttons_frame.pack(fill=tk.X, pady=(PADDING_MEDIUM, 0))
        
        cancel_button = tk.Button(
            dialog_buttons_frame,
            text="Отмена",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(PADDING_SMALL, 0))
        
        save_button = tk.Button(
            dialog_buttons_frame,
            text="Сохранить",
            bg=ORANGE_PRIMARY,
            fg=DARK_BG,
            command=self.save_all_commands
        )
        save_button.pack(side=tk.RIGHT)
    
    def add_command(self):
        """Добавляет новую консольную команду"""
        KitConsoleCommandDialog(self.dialog, self.add_command_to_list)
    
    def edit_command(self, event=None):
        """Редактирует выбранную консольную команду"""
        selected = self.commands_listbox.curselection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите команду для редактирования")
            return
        
        index = selected[0]
        command = self.commands_list[index]
        
        KitConsoleCommandDialog(self.dialog, lambda cmd: self.update_command_in_list(index, cmd), command)
    
    def remove_command(self):
        """Удаляет выбранную консольную команду"""
        selected = self.commands_listbox.curselection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите команду для удаления")
            return
        
        index = selected[0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту команду?"):
            del self.commands_list[index]
            self.refresh_commands_list()
    
    def add_command_to_list(self, command):
        """Добавляет команду в список"""
        self.commands_list.append(command)
        self.refresh_commands_list()
    
    def update_command_in_list(self, index, command):
        """Обновляет команду в списке"""
        if 0 <= index < len(self.commands_list):
            self.commands_list[index] = command
            self.refresh_commands_list()
    
    def refresh_commands_list(self):
        """Обновляет отображаемый список команд"""
        self.commands_listbox.delete(0, tk.END)
        for command in self.commands_list:
            self.commands_listbox.insert(tk.END, command)
    
    def save_all_commands(self):
        """Сохраняет все команды и закрывает диалог"""
        self.dialog.destroy()
        if self.on_save:
            self.on_save(self.commands_list)
