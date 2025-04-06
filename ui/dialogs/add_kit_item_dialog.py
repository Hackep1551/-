import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from ui.constants import *

class AddKitItemDialog:
    """Класс диалогового окна для добавления предмета в набор"""
    
    def __init__(self, parent, items_data=None, on_save=None, item_data=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            items_data: словарь с данными о предметах для автозаполнения
            on_save: функция обратного вызова при сохранении
            item_data: данные о редактируемом предмете (если редактирование)
        """
        self.parent = parent
        self.items_data = items_data or {}
        self.on_save = on_save
        self.item_data = item_data or {}
        self.result = None
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить предмет в набор")
        self.dialog.geometry("700x460")  # Увеличим размер диалога
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if hasattr(parent, "winfo_x") and hasattr(parent, "winfo_width"):
            x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 460) // 2
            self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.item_data:
            self.blueprint_var.set(self.item_data.get("Blueprint", ""))
            self.amount_var.set(str(self.item_data.get("Amount", 1)))
            self.quality_var.set(str(self.item_data.get("Quality", 0)))
            self.force_blueprint_var.set(self.item_data.get("ForceBlueprint", False))
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Создаем раздел для выбора между поиском и ручным вводом
        input_method_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        input_method_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.input_method_var = tk.StringVar(value="search")
        search_radio = ttk.Radiobutton(input_method_frame, text="Поиск предмета", variable=self.input_method_var, 
                                      value="search", command=self.toggle_input_method)
        search_radio.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        manual_radio = ttk.Radiobutton(input_method_frame, text="Ручной ввод Blueprint", variable=self.input_method_var, 
                                     value="manual", command=self.toggle_input_method)
        manual_radio.pack(side=tk.LEFT)
        
        # Создаем фрейм для поиска предметов
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
        
        self.items_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.items_listbox.yview)
        self.items_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Заполняем listbox при загрузке
        self.populate_items_list()
        
        # Привязываем события
        self.search_var.trace_add("write", self.filter_items)
        self.items_listbox.bind("<Double-1>", self.select_item)
        
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
        blueprint_hint = tk.Label(main_frame, text="Формат: Blueprint'/Game/Path/To/Item.Item'", 
                                bg=DARK_SECONDARY, fg=GRAY_TEXT)
        blueprint_hint.pack(anchor="w", pady=(0, PADDING_SMALL))
        
        # Поле для ввода количества
        amount_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        amount_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        amount_label = tk.Label(amount_frame, text="Количество:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        amount_label.pack(side=tk.LEFT)
        
        self.amount_var = tk.StringVar(value="1")
        amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var, width=10)
        amount_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Поле для ввода качества
        quality_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        quality_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        quality_label = tk.Label(quality_frame, text="Качество (0-5):", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        quality_label.pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar(value="0")
        quality_entry = ttk.Entry(quality_frame, textvariable=self.quality_var, width=10)
        quality_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Флажок "Принудительно чертеж"
        self.force_blueprint_var = tk.BooleanVar(value=False)
        force_blueprint_cb = ttk.Checkbutton(
            main_frame, 
            text="Принудительно чертеж", 
            variable=self.force_blueprint_var
        )
        force_blueprint_cb.pack(anchor="w", pady=PADDING_SMALL)
        
        # Информационный текст
        info_text = """
        Качество предмета:
        0 - обычное, 1 - необычное (зеленое), 2 - редкое (синее), 
        3 - эпическое (фиолетовое), 4 - легендарное (желтое), 5 - мифическое (красное)
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
            command=self.save_item
        )
        save_button.pack(side=tk.RIGHT)
        
        # Вызываем метод переключения для установки начального состояния интерфейса
        self.toggle_input_method()
    
    def populate_items_list(self):
        """Заполняет listbox списком предметов"""
        self.items_listbox.delete(0, tk.END)
        
        # Сортируем предметы по имени для удобства поиска
        sorted_items = sorted(self.items_data.keys())
        
        for item_name in sorted_items:
            self.items_listbox.insert(tk.END, item_name)
            
    def filter_items(self, *args):
        """Фильтрует список предметов по поисковому запросу"""
        search_term = self.search_var.get().lower()
        self.items_listbox.delete(0, tk.END)
        
        # Если поисковый запрос пустой, показываем все предметы
        if not search_term:
            sorted_items = sorted(self.items_data.keys())
            for item_name in sorted_items:
                self.items_listbox.insert(tk.END, item_name)
            return
        
        # Иначе фильтруем предметы по поисковому запросу
        for item_name in sorted(self.items_data.keys()):
            if search_term in item_name.lower():
                self.items_listbox.insert(tk.END, item_name)
    
    def select_item(self, event=None):
        """Обработчик выбора предмета из списка"""
        selected_indices = self.items_listbox.curselection()
        if not selected_indices:
            return
        
        selected_item = self.items_listbox.get(selected_indices[0])
        if selected_item in self.items_data:
            blueprint = self.items_data[selected_item].get("blueprint", "")
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
            
    def save_item(self):
        """Сохраняет данные о предмете"""
        blueprint = self.blueprint_var.get()
        
        if not blueprint:
            messagebox.showerror("Ошибка", "Blueprint не может быть пустым")
            return
        
        try:
            amount = int(self.amount_var.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Количество должно быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом")
            return
        
        try:
            quality = int(self.quality_var.get())
            if quality < 0 or quality > 5:
                messagebox.showerror("Ошибка", "Качество должно быть в диапазоне от 0 до 5")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Качество должно быть целым числом")
            return
        
        # Формируем результат
        result = {
            "Blueprint": blueprint,
            "Amount": amount,
            "Quality": quality,
            "ForceBlueprint": self.force_blueprint_var.get()
        }
        
        self.result = result
        
        # Закрываем диалог и вызываем callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(result)
