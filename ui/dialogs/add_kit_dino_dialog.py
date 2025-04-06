import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from ui.constants import *

class AddKitDinoDialog:
    """Класс диалогового окна для добавления динозавра в набор"""
    
    def __init__(self, parent, dinos_data=None, on_save=None, dino_data=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            dinos_data: словарь с данными о динозаврах для автозаполнения
            on_save: функция обратного вызова при сохранении
            dino_data: данные о редактируемом динозавре (если редактирование)
        """
        self.parent = parent
        self.dinos_data = dinos_data or {}
        self.on_save = on_save
        self.dino_data = dino_data or {}
        self.result = None
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить динозавра в набор")
        self.dialog.geometry("900x700")  # Увеличил размер диалога
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if hasattr(parent, "winfo_x") and hasattr(parent, "winfo_width"):
            x = parent.winfo_x() + (parent.winfo_width() - 900) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 700) // 2
            self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.dino_data:
            self.blueprint_var.set(self.dino_data.get("Blueprint", ""))
            self.level_var.set(str(self.dino_data.get("Level", 150)))
            self.neutered_var.set(self.dino_data.get("Neutered", False))
            self.name_var.set(self.dino_data.get("Name", ""))
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Создаем раздел для выбора между поиском и ручным вводом
        input_method_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        input_method_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.input_method_var = tk.StringVar(value="search")
        search_radio = ttk.Radiobutton(input_method_frame, text="Поиск динозавра", variable=self.input_method_var, 
                                      value="search", command=self.toggle_input_method)
        search_radio.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        manual_radio = ttk.Radiobutton(input_method_frame, text="Ручной ввод Blueprint", variable=self.input_method_var, 
                                     value="manual", command=self.toggle_input_method)
        manual_radio.pack(side=tk.LEFT)
        
        # Создаем фрейм для поиска динозавров
        self.search_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        self.search_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Поле поиска
        search_label = tk.Label(self.search_frame, text="Поиск:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        search_label.pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0), fill=tk.X, expand=True)
        
        # Создаем listbox для отображения результатов поиска
        list_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        self.dinos_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.dinos_listbox.yview)
        self.dinos_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.dinos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Заполняем listbox при загрузке
        self.populate_dinos_list()
        
        # Привязываем события
        self.search_var.trace_add("write", self.filter_dinos)
        self.dinos_listbox.bind("<Double-1>", self.select_dino)
        
        # Создаем фрейм для ручного ввода Blueprint
        self.manual_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        # Изначально не показываем фрейм для ручного ввода
        
        # Поле для ввода Blueprint
        blueprint_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        blueprint_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        blueprint_label = tk.Label(blueprint_frame, text="Blueprint:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        blueprint_label.pack(side=tk.LEFT)
        
        self.blueprint_var = tk.StringVar()
        blueprint_entry = ttk.Entry(blueprint_frame, textvariable=self.blueprint_var, width=70)  # Увеличил ширину
        blueprint_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0), fill=tk.X, expand=True)
        
        # Инструкция для Blueprint
        blueprint_hint = tk.Label(main_frame, text="Формат: Blueprint'/Game/Path/To/Dino.Dino'", 
                                bg=DARK_SECONDARY, fg=GRAY_TEXT)
        blueprint_hint.pack(anchor="w", pady=(0, PADDING_SMALL))
        
        # Поле для ввода уровня
        level_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        level_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        level_label = tk.Label(level_frame, text="Уровень:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        level_label.pack(side=tk.LEFT)
        
        self.level_var = tk.StringVar(value="150")
        level_entry = ttk.Entry(level_frame, textvariable=self.level_var, width=10)
        level_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Поле для ввода имени
        name_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        name_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        name_label = tk.Label(name_frame, text="Имя:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        name_label.pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Флажок "Стерилизован"
        self.neutered_var = tk.BooleanVar(value=False)
        neutered_cb = ttk.Checkbutton(
            main_frame, 
            text="Стерилизован", 
            variable=self.neutered_var
        )
        neutered_cb.pack(anchor="w", pady=PADDING_SMALL)
        
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
            command=self.save_dino
        )
        save_button.pack(side=tk.RIGHT)
        
        # Вызываем метод переключения для установки начального состояния интерфейса
        self.toggle_input_method()
    
    def populate_dinos_list(self):
        """Заполняет listbox списком динозавров"""
        self.dinos_listbox.delete(0, tk.END)
        
        # Сортируем динозавров по имени для удобства поиска
        sorted_dinos = sorted(self.dinos_data.keys())
        
        for dino_name in sorted_dinos:
            self.dinos_listbox.insert(tk.END, dino_name)

    def filter_dinos(self, *args):
        """Фильтрует список динозавров по поисковому запросу"""
        search_term = self.search_var.get().lower()
        self.dinos_listbox.delete(0, tk.END)
        
        # Если поисковый запрос пустой, показываем всех динозавров
        if not search_term:
            sorted_dinos = sorted(self.dinos_data.keys())
            for dino_name in sorted_dinos:
                self.dinos_listbox.insert(tk.END, dino_name)
            return
        
        # Иначе фильтруем динозавров по поисковому запросу
        for dino_name in sorted(self.dinos_data.keys()):
            if search_term in dino_name.lower():
                self.dinos_listbox.insert(tk.END, dino_name)
    
    def select_dino(self, event=None):
        """Обработчик выбора динозавра из списка"""
        selected_indices = self.dinos_listbox.curselection()
        if not selected_indices:
            return
        
        selected_dino = self.dinos_listbox.get(selected_indices[0])
        if selected_dino in self.dinos_data:
            blueprint = self.dinos_data[selected_dino].get("blueprint", "")
            self.blueprint_var.set(blueprint)

    def toggle_input_method(self):
        """Переключение между поиском и ручным вводом Blueprint"""
        if self.input_method_var.get() == "search":
            self.search_frame.pack(fill=tk.X, pady=PADDING_SMALL)
            if hasattr(self, "manual_frame") and self.manual_frame.winfo_exists():
                self.manual_frame.pack_forget()
        else:
            if hasattr(self, "search_frame") and self.search_frame.winfo_exists():
                self.search_frame.pack_forget()
            self.manual_frame.pack(fill=tk.X, pady=PADDING_SMALL)

    def save_dino(self):
        """Сохраняет данные о динозавре"""
        blueprint = self.blueprint_var.get()
        
        if not blueprint:
            messagebox.showerror("Ошибка", "Blueprint не может быть пустым")
            return
        
        try:
            level = int(self.level_var.get())
            if level <= 0:
                messagebox.showerror("Ошибка", "Уровень должен быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Уровень должен быть целым числом")
            return
        
        # Формируем результат
        result = {
            "Blueprint": blueprint,
            "Level": level,
            "Neutered": self.neutered_var.get(),
            "Name": self.name_var.get()
        }
        
        self.result = result
        
        # Закрываем диалог и вызываем callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(result)
