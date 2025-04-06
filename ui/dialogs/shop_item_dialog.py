import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from ui.constants import *

class ShopItemDialog:
    """Класс диалогового окна для добавления/редактирования товара в магазине"""
    
    def __init__(self, parent, ark_data=None, on_save=None, item_data=None, item_id=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            ark_data: данные ARK для автозаполнения
            on_save: функция обратного вызова при сохранении
            item_data: данные о редактируемом предмете (если редактирование)
            item_id: ID редактируемого предмета (если редактирование)
        """
        self.parent = parent
        self.ark_data = ark_data or {}
        self.on_save = on_save
        self.item_data = item_data or {}
        self.item_id = item_id
        self.items_list = []
        self.dinos_list = []
        self.console_commands_list = []
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить товар в магазин" if not item_id else f"Редактировать товар: {item_id}")
        self.dialog.geometry("900x700")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно экрана
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 700) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.item_data:
            self.fill_form_with_item_data()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создаем основной фрейм с прокруткой
        main_canvas = tk.Canvas(self.dialog, bg=DARK_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=main_canvas.yview)
        main_frame = tk.Frame(main_canvas, bg=DARK_SECONDARY)
        
        main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(
                scrollregion=main_canvas.bbox("all")
            )
        )
        
        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязываем колесо мыши для прокрутки
        main_canvas.bind_all("<MouseWheel>", lambda event: main_canvas.yview_scroll(-1*(event.delta//120), "units"))
        
        # ID товара
        id_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        id_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        id_label = tk.Label(id_frame, text="ID товара:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        id_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.id_var = tk.StringVar(value=self.item_id or "")
        id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
        id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Заголовок товара
        title_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        title_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        title_label = tk.Label(title_frame, text="Название товара:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        title_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(title_frame, textvariable=self.title_var, width=50)
        title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Описание товара
        desc_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        desc_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        desc_label = tk.Label(desc_frame, text="Описание:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        desc_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.desc_var, width=50)
        desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Цена товара
        price_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        price_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        price_label = tk.Label(price_frame, text="Цена:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        price_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.price_var = tk.StringVar(value="1")
        price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=10)
        price_entry.pack(side=tk.LEFT)
        
        # Флаг исключения из скидок
        self.exclude_discount_var = tk.BooleanVar(value=False)
        exclude_discount_cb = ttk.Checkbutton(
            price_frame, 
            text="Исключить из скидок", 
            variable=self.exclude_discount_var
        )
        exclude_discount_cb.pack(side=tk.LEFT, padx=(PADDING_MEDIUM, 0))
        
        # Категории
        categories_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        categories_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        categories_label = tk.Label(categories_frame, text="Категории:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        categories_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.categories_var = tk.StringVar()
        categories_entry = ttk.Entry(categories_frame, textvariable=self.categories_var, width=30)
        categories_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Список доступных категорий для быстрого выбора
        categories_list = ["Weapons", "Dye", "Dinosaurs", "Armor", "Structures", "Consumables", "Chibis", "Maps", "Tools"]
        
        self.category_buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        self.category_buttons_frame.pack(fill=tk.X, pady=(0, PADDING_SMALL), padx=PADDING_MEDIUM)
        
        for category in categories_list:
            btn = tk.Button(
                self.category_buttons_frame,
                text=category,
                bg=BUTTON_BG,
                fg=LIGHT_TEXT,
                command=lambda cat=category: self.add_category(cat)
            )
            btn.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Вкладки для предметов, динозавров и консольных команд
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        # Вкладка для предметов
        items_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(items_frame, text="Предметы")
        
        # Фрейм для списка предметов
        items_list_frame = tk.Frame(items_frame, bg=DARK_SECONDARY)
        items_list_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        # Колонки для таблицы предметов
        items_columns = ("blueprint", "amount", "quality", "force_bp")
        self.items_table = ttk.Treeview(
            items_list_frame, 
            columns=items_columns,
            show="headings",
            selectmode="browse"
        )
        
        # Заголовки колонок
        self.items_table.heading("blueprint", text="Blueprint")
        self.items_table.heading("amount", text="Количество")
        self.items_table.heading("quality", text="Качество")
        self.items_table.heading("force_bp", text="Принуд. чертеж")
        
        # Настройка ширины колонок
        self.items_table.column("blueprint", width=300, anchor="w")
        self.items_table.column("amount", width=80, anchor="center")
        self.items_table.column("quality", width=80, anchor="center")
        self.items_table.column("force_bp", width=100, anchor="center")
        
        # Добавляем прокрутку для таблицы
        items_scroll = ttk.Scrollbar(items_list_frame, orient="vertical", command=self.items_table.yview)
        self.items_table.configure(yscrollcommand=items_scroll.set)
        self.items_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления предметами
        items_btn_frame = tk.Frame(items_frame, bg=DARK_SECONDARY)
        items_btn_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        add_item_btn = tk.Button(
            items_btn_frame,
            text="Добавить предмет",
            bg=ORANGE_PRIMARY,
            fg=DARK_BG,
            command=self.add_item
        )
        add_item_btn.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        edit_item_btn = tk.Button(
            items_btn_frame,
            text="Редактировать",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.edit_item
        )
        edit_item_btn.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        remove_item_btn = tk.Button(
            items_btn_frame,
            text="Удалить",
            bg=RED_BTN,
            fg=LIGHT_TEXT,
            command=self.remove_item
        )
        remove_item_btn.pack(side=tk.LEFT)
        
        # Вкладка для динозавров
        dinos_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(dinos_frame, text="Динозавры")
        
        # Вкладка для консольных команд
        commands_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(commands_frame, text="Консольные команды")
        
        # Разделы для разрешений и ограничений карт
        options_frame = tk.LabelFrame(main_frame, text="Дополнительные настройки", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        options_frame.pack(fill=tk.X, pady=PADDING_SMALL, padx=PADDING_MEDIUM)
        
        # Группы разрешений
        permission_frame = tk.Frame(options_frame, bg=DARK_SECONDARY)
        permission_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        permission_label = tk.Label(permission_frame, text="Группы разрешений:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        permission_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.permission_var = tk.StringVar()
        permission_entry = ttk.Entry(permission_frame, textvariable=self.permission_var, width=30)
        permission_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Карты, на которых доступно
        maps_frame = tk.Frame(options_frame, bg=DARK_SECONDARY)
        maps_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        maps_label = tk.Label(maps_frame, text="Только на картах:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        maps_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.maps_var = tk.StringVar()
        maps_entry = ttk.Entry(maps_frame, textvariable=self.maps_var, width=30)
        maps_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Карты, на которых недоступно
        not_maps_frame = tk.Frame(options_frame, bg=DARK_SECONDARY)
        not_maps_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        not_maps_label = tk.Label(not_maps_frame, text="НЕ на картах:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        not_maps_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.not_maps_var = tk.StringVar()
        not_maps_entry = ttk.Entry(not_maps_frame, textvariable=self.not_maps_var, width=30)
        not_maps_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Кнопки внизу
        buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=PADDING_MEDIUM, padx=PADDING_MEDIUM)
        
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
            command=self.save_shop_item
        )
        save_button.pack(side=tk.RIGHT)
        
        # Добавляем обработчик двойного клика для редактирования предметов
        self.items_table.bind("<Double-1>", self.edit_item)
        
        # Заполняем таблицу предметами если они есть
        self.refresh_items_table()
    
    def add_category(self, category):
        """Добавляет категорию в поле категорий"""
        current = self.categories_var.get().strip()
        if not current:
            self.categories_var.set(category)
        else:
            categories = [cat.strip() for cat in current.split(",")]
            if category not in categories:
                categories.append(category)
                self.categories_var.set(", ".join(categories))
    
    def add_item(self):
        """Открывает диалог для добавления предмета"""
        dialog = ItemDialog(self.dialog, self.ark_data, lambda item: self.add_item_to_list(item))
        
    def edit_item(self, event=None):
        """Открывает диалог для редактирования предмета"""
        # Получаем выбранный элемент
        selected_items = self.items_table.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите предмет для редактирования")
            return
        
        selected_index = self.items_table.index(selected_items[0])
        if selected_index < 0 or selected_index >= len(self.items_list):
            return
        
        dialog = ItemDialog(
            self.dialog, 
            self.ark_data, 
            lambda item: self.update_item_in_list(selected_index, item),
            self.items_list[selected_index]
        )
        
    def remove_item(self):
        """Удаляет выбранный предмет из списка"""
        # Получаем выбранный элемент
        selected_items = self.items_table.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите предмет для удаления")
            return
        
        selected_index = self.items_table.index(selected_items[0])
        if selected_index < 0 or selected_index >= len(self.items_list):
            return
        
        # Удаляем предмет из списка
        del self.items_list[selected_index]
        
        # Обновляем таблицу
        self.refresh_items_table()
    
    def add_item_to_list(self, item):
        """Добавляет предмет в список"""
        if item:
            self.items_list.append(item)
            self.refresh_items_table()
    
    def update_item_in_list(self, index, item):
        """Обновляет предмет в списке"""
        if item and 0 <= index < len(self.items_list):
            self.items_list[index] = item
            self.refresh_items_table()
    
    def refresh_items_table(self):
        """Обновляет таблицу предметов"""
        # Очищаем таблицу
        for item in self.items_table.get_children():
            self.items_table.delete(item)
        
        # Добавляем предметы в таблицу
        for item in self.items_list:
            blueprint = item.get("Blueprint", "")
            amount = item.get("Amount", 1)
            quality = item.get("Quality", 0)
            force_bp = "Да" if item.get("ForceBlueprint", False) else "Нет"
            
            self.items_table.insert("", "end", values=(blueprint, amount, quality, force_bp))
    
    def fill_form_with_item_data(self):
        """Заполняет форму данными существующего товара"""
        # Заполняем основные поля
        self.title_var.set(self.item_data.get("Title", ""))
        self.desc_var.set(self.item_data.get("Description", ""))
        self.price_var.set(str(self.item_data.get("Price", 1)))
        self.exclude_discount_var.set(self.item_data.get("Exclude_From_Discount", False))
        
        # Заполняем категории
        categories = self.item_data.get("Categories", [])
        if categories:
            self.categories_var.set(", ".join(categories))
        
        # Заполняем предметы
        self.items_list = self.item_data.get("Items", [])
        
        # Заполняем динозавров
        self.dinos_list = self.item_data.get("Dinos", [])
        
        # Заполняем консольные команды
        self.console_commands_list = self.item_data.get("ConsoleCommands", [])
        
        # Заполняем дополнительные настройки
        permissions = self.item_data.get("PermissionGroupRequired", [])
        if permissions:
            self.permission_var.set(", ".join(permissions))
        
        only_maps = self.item_data.get("Only_On_These_Maps", [])
        if only_maps:
            self.maps_var.set(", ".join(only_maps))
        
        not_maps = self.item_data.get("NOT_On_These_Maps", [])
        if not_maps:
            self.not_maps_var.set(", ".join(not_maps))
            
        # Обновляем таблицы
        self.refresh_items_table()
    
    def save_shop_item(self):
        """Сохраняет данные товара"""
        # Проверка основных полей
        item_id = self.id_var.get().strip()
        if not item_id:
            messagebox.showerror("Ошибка", "ID товара не может быть пустым")
            return
        
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Ошибка", "Название товара не может быть пустым")
            return
        
        # Проверка цены
        try:
            price = int(self.price_var.get())
            if price < 0:
                messagebox.showerror("Ошибка", "Цена не может быть отрицательной")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть целым числом")
            return
        
        # Парсим категории
        categories = []
        if self.categories_var.get().strip():
            categories = [cat.strip() for cat in self.categories_var.get().split(",") if cat.strip()]
        
        # Парсим группы разрешений
        permissions = []
        if self.permission_var.get().strip():
            permissions = [perm.strip() for perm in self.permission_var.get().split(",") if perm.strip()]
        
        # Парсим ограничения карт
        only_maps = []
        if self.maps_var.get().strip():
            only_maps = [map_name.strip() for map_name in self.maps_var.get().split(",") if map_name.strip()]
        
        not_maps = []
        if self.not_maps_var.get().strip():
            not_maps = [map_name.strip() for map_name in self.not_maps_var.get().split(",") if map_name.strip()]
        
        # Формируем данные товара
        item_data = {
            "Title": title,
            "Categories": categories,
            "Description": self.desc_var.get().strip(),
            "Price": price,
            "Exclude_From_Discount": self.exclude_discount_var.get(),
            "Items": self.items_list,
            "Dinos": self.dinos_list,
            "ConsoleCommands": self.console_commands_list,
            "PermissionGroupRequired": permissions,
            "Only_On_These_Maps": only_maps,
            "NOT_On_These_Maps": not_maps
        }
        
        # Сохраняем данные
        self.dialog.destroy()
        if self.on_save:
            self.on_save(item_id, item_data)


class ItemDialog:
    """Диалог для добавления/редактирования предмета"""
    
    def __init__(self, parent, ark_data, on_save, item_data=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            ark_data: данные ARK для автозаполнения
            on_save: функция обратного вызова при сохранении
            item_data: данные о редактируемом предмете (если редактирование)
        """
        self.parent = parent
        self.ark_data = ark_data
        self.on_save = on_save
        self.item_data = item_data or {}
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить предмет" if not item_data else "Редактировать предмет")
        self.dialog.geometry("700x400")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно родителя
        if parent:
            x = parent.winfo_x() + (parent.winfo_width() - 700) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
            self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.item_data:
            self.fill_form_with_item_data()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создаем фрейм с вкладками
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Вкладка поиска предмета
        search_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(search_frame, text="Поиск предмета")
        
        # Поле поиска
        search_input_frame = tk.Frame(search_frame, bg=DARK_SECONDARY)
        search_input_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        search_label = tk.Label(search_input_frame, text="Поиск:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        search_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_input_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Таблица результатов поиска
        results_frame = tk.Frame(search_frame, bg=DARK_SECONDARY)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        # Колонки для таблицы результатов
        results_columns = ("name", "blueprint")
        self.results_table = ttk.Treeview(
            results_frame, 
            columns=results_columns,
            show="headings",
            selectmode="browse"
        )
        
        # Заголовки колонок
        self.results_table.heading("name", text="Название")
        self.results_table.heading("blueprint", text="Blueprint")
        
        # Настройка ширины колонок
        self.results_table.column("name", width=200, anchor="w")
        self.results_table.column("blueprint", width=400, anchor="w")
        
        # Добавляем прокрутку для таблицы
        results_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=results_scroll.set)
        self.results_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Вкладка ручного ввода
        manual_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(manual_frame, text="Ручной ввод")
        
        # Поле для ввода Blueprint
        bp_frame = tk.Frame(manual_frame, bg=DARK_SECONDARY)
        bp_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        bp_label = tk.Label(bp_frame, text="Blueprint:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        bp_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.blueprint_var = tk.StringVar()
        bp_entry = ttk.Entry(bp_frame, textvariable=self.blueprint_var, width=50)
        bp_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Общие параметры (отображаются внизу обеих вкладок)
        params_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        params_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
        
        # Количество
        amount_frame = tk.Frame(params_frame, bg=DARK_SECONDARY)
        amount_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        amount_label = tk.Label(amount_frame, text="Количество:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        amount_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.amount_var = tk.StringVar(value="1")
        amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var, width=10)
        amount_entry.pack(side=tk.LEFT)
        
        # Качество
        quality_frame = tk.Frame(params_frame, bg=DARK_SECONDARY)
        quality_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        quality_label = tk.Label(quality_frame, text="Качество (0-5):", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        quality_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.quality_var = tk.StringVar(value="0")
        quality_entry = ttk.Entry(quality_frame, textvariable=self.quality_var, width=10)
        quality_entry.pack(side=tk.LEFT)
        
        # Принудительно чертеж
        options_frame = tk.Frame(params_frame, bg=DARK_SECONDARY)
        options_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.force_blueprint_var = tk.BooleanVar(value=False)
        force_blueprint_cb = ttk.Checkbutton(
            options_frame, 
            text="Принудительно чертеж", 
            variable=self.force_blueprint_var
        )
        force_blueprint_cb.pack(anchor="w")
        
        # Кнопки
        buttons_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
        
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
        
        # Привязываем события
        self.search_var.trace_add("write", self.search_items)
        self.results_table.bind("<Double-1>", self.select_item)
        
        # Заполняем таблицу результатов поиска
        self.populate_items_table()
    
    def populate_items_table(self):
        """Заполняет таблицу результатов поиска"""
        # Очищаем таблицу
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        
        # Получаем предметы из ArkData
        items = self.ark_data.get("items", {})
        
        # Добавляем предметы в таблицу (макс. 100 для производительности)
        count = 0
        for name, item_data in sorted(items.items()):
            blueprint = item_data.get("blueprint", "")
            
            self.results_table.insert("", "end", values=(name, blueprint))
            
            count += 1
            if count >= 100:
                break
    
    def search_items(self, *args):
        """Поиск предметов по введенному тексту"""
        search_text = self.search_var.get().lower()
        
        # Очищаем таблицу
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        
        # Если поисковая строка пустая, показываем первые 100 предметов
        if not search_text:
            self.populate_items_table()
            return
        
        # Получаем предметы из ArkData
        items = self.ark_data.get("items", {})
        
        # Фильтруем предметы по поисковому запросу
        filtered_items = {}
        for name, item_data in items.items():
            if search_text in name.lower():
                filtered_items[name] = item_data
        
        # Добавляем отфильтрованные предметы в таблицу
        for name, item_data in sorted(filtered_items.items()):
            blueprint = item_data.get("blueprint", "")
            
            self.results_table.insert("", "end", values=(name, blueprint))
    
    def select_item(self, event=None):
        """Обработчик выбора предмета из таблицы результатов"""
        # Получаем выбранный элемент
        selected_items = self.results_table.selection()
        if not selected_items:
            return
        
        # Получаем данные выбранного элемента
        selected_item = self.results_table.item(selected_items[0])
        
        # Устанавливаем Blueprint в соответствующее поле
        self.blueprint_var.set(selected_item["values"][1])
    
    def fill_form_with_item_data(self):
        """Заполняет форму данными существующего предмета"""
        self.blueprint_var.set(self.item_data.get("Blueprint", ""))
        self.amount_var.set(str(self.item_data.get("Amount", 1)))
        self.quality_var.set(str(self.item_data.get("Quality", 0)))
        self.force_blueprint_var.set(self.item_data.get("ForceBlueprint", False))
    
    def save_item(self):
        """Сохраняет данные предмета"""
        # Проверка Blueprint
        blueprint = self.blueprint_var.get().strip()
        if not blueprint:
            messagebox.showerror("Ошибка", "Blueprint не может быть пустым")
            return
        
        # Проверка количества
        try:
            amount = int(self.amount_var.get())
            if amount < 1:
                messagebox.showerror("Ошибка", "Количество должно быть больше нуля")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом")
            return
        
        # Проверка качества
        try:
            quality = int(self.quality_var.get())
            if quality < 0 or quality > 5:
                messagebox.showerror("Ошибка", "Качество должно быть в диапазоне от 0 до 5")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Качество должно быть целым числом")
            return
        
        # Формируем результат
        item_data = {
            "Blueprint": blueprint,
            "Amount": amount,
            "Quality": quality,
            "ForceBlueprint": self.force_blueprint_var.get()
        }
        
        # Закрываем диалог и вызываем callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(item_data)
