import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from ui.constants import *

class AddShopItemDialog:
    """Класс диалогового окна для добавления товара в магазин"""
    
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
        self.result = None
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить предмет в магазин" if not item_id else f"Редактировать предмет: {item_id}")
        self.dialog.geometry("800x600")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно экрана
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.item_data:
            self.fill_form_with_item_data()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер с прокруткой
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # ID предмета (только если добавляем новый)
        if not self.item_id:
            id_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
            id_frame.pack(fill=tk.X, pady=PADDING_SMALL)
            
            id_label = tk.Label(id_frame, text="ID предмета:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
            id_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
            
            self.id_var = tk.StringVar()
            id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
            id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        else:
            # Если редактируем существующий предмет, создаем поле для нового ID
            id_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
            id_frame.pack(fill=tk.X, pady=PADDING_SMALL)
            
            id_label = tk.Label(id_frame, text="ID предмета:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
            id_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
            
            self.id_var = tk.StringVar(value=self.item_id)
            id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
            id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Выбор между поиском предмета и вводом blueprint
        method_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        method_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.method_var = tk.StringVar(value="search")
        search_radio = ttk.Radiobutton(method_frame, text="Поиск предмета", variable=self.method_var, value="search", command=self.toggle_method)
        search_radio.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        manual_radio = ttk.Radiobutton(method_frame, text="Ввод blueprint", variable=self.method_var, value="manual", command=self.toggle_method)
        manual_radio.pack(side=tk.LEFT)
        
        # Фрейм для поиска предмета
        self.search_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        self.search_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        search_label = tk.Label(self.search_frame, text="Поиск:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        search_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Создаем listbox для отображения результатов
        list_frame = tk.Frame(self.search_frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        self.items_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=8)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.items_listbox.yview)
        self.items_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязываем поиск к вводу текста
        self.search_var.trace("w", self.filter_items)
        
        # Привязываем двойной клик к выбору предмета
        self.items_listbox.bind("<Double-1>", self.select_item)
        
        # Заполняем список всеми предметами изначально
        self.populate_items_list()
        
        # Фрейм для ручного ввода blueprint
        self.manual_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        
        blueprint_label = tk.Label(self.manual_frame, text="Blueprint:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        blueprint_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.blueprint_var = tk.StringVar()
        blueprint_entry = ttk.Entry(self.manual_frame, textvariable=self.blueprint_var, width=50)
        blueprint_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Название предмета
        name_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        name_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        name_label = tk.Label(name_frame, text="Название:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        name_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=50)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Цена предмета
        price_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        price_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        price_label = tk.Label(price_frame, text="Цена:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        price_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.price_var = tk.StringVar(value="0")
        price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=10)
        price_entry.pack(side=tk.LEFT)
        
        # Количество предмета
        amount_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        amount_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        amount_label = tk.Label(amount_frame, text="Количество:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        amount_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.amount_var = tk.StringVar(value="1")
        amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var, width=10)
        amount_entry.pack(side=tk.LEFT)
        
        # Качество предмета
        quality_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        quality_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        quality_label = tk.Label(quality_frame, text="Качество (0-5):", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        quality_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.quality_var = tk.StringVar(value="0")
        quality_entry = ttk.Entry(quality_frame, textvariable=self.quality_var, width=10)
        quality_entry.pack(side=tk.LEFT)
        
        # Категория предмета
        category_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        category_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        category_label = tk.Label(category_frame, text="Категория:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        category_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        categories = [
            "Weapons", "Dye", "Dinosaurs", "Armor", 
            "Structures", "Consumables", "Chibis", "Maps"
        ]
        
        self.category_var = tk.StringVar(value=categories[0])
        category_combobox = ttk.Combobox(category_frame, textvariable=self.category_var, values=categories)
        category_combobox.pack(side=tk.LEFT)
        
        # Дополнительные настройки в чекбоксах
        options_frame = tk.LabelFrame(main_frame, text="Дополнительные настройки", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        options_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.force_blueprint_var = tk.BooleanVar(value=False)
        force_blueprint_cb = ttk.Checkbutton(
            options_frame, 
            text="Принудительно чертеж", 
            variable=self.force_blueprint_var
        )
        force_blueprint_cb.pack(anchor="w")
        
        self.hide_until_unlocked_var = tk.BooleanVar(value=False)
        hide_until_unlocked_cb = ttk.Checkbutton(
            options_frame, 
            text="Скрыть до разблокировки", 
            variable=self.hide_until_unlocked_var
        )
        hide_until_unlocked_cb.pack(anchor="w")
        
        self.block_in_buildings_var = tk.BooleanVar(value=False)
        block_in_buildings_cb = ttk.Checkbutton(
            options_frame, 
            text="Блокировать в постройках", 
            variable=self.block_in_buildings_var
        )
        block_in_buildings_cb.pack(anchor="w")
        
        self.block_in_enemy_territory_var = tk.BooleanVar(value=False)
        block_in_enemy_territory_cb = ttk.Checkbutton(
            options_frame, 
            text="Блокировать на территории врага", 
            variable=self.block_in_enemy_territory_var
        )
        block_in_enemy_territory_cb.pack(anchor="w")
        
        # Кнопки внизу
        buttons_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=PADDING_SMALL, side=tk.BOTTOM)
        
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
        
        # Изначально показываем фрейм поиска
        self.toggle_method()

    def populate_items_list(self):
        """Заполнение списка всеми доступными предметами"""
        self.items_listbox.delete(0, tk.END)
        
        if not self.ark_data or "items" not in self.ark_data:
            return
            
        sorted_items = sorted(self.ark_data.get("items", {}).keys())
        for item_name in sorted_items:
            self.items_listbox.insert(tk.END, item_name)
    
    def filter_items(self, *args):
        """Фильтрация предметов по поисковому запросу"""
        search_term = self.search_var.get().lower()
        self.items_listbox.delete(0, tk.END)
        
        # Если поисковый запрос пуст, показываем все предметы
        if not search_term:
            self.populate_items_list()
            return
            
        if not self.ark_data or "items" not in self.ark_data:
            return
            
        items = self.ark_data.get("items", {})
        
        # Ищем совпадения
        matching_items = [name for name in items.keys() if search_term in name.lower()]
                
        # Сортируем и добавляем в список
        for item_name in sorted(matching_items):
            self.items_listbox.insert(tk.END, item_name)
            
    def select_item(self, event=None):
        """Выбор предмета из списка"""
        selected_indices = self.items_listbox.curselection()
        if not selected_indices:
            return
            
        item_name = self.items_listbox.get(selected_indices[0])
        if "items" not in self.ark_data or item_name not in self.ark_data.get("items", {}):
            return
            
        item_info = self.ark_data["items"][item_name]
        
        # Заполняем поля данными предмета
        self.blueprint_var.set(item_info.get("blueprint", ""))
        if not self.name_var.get():  # Если имя не задано, используем имя из ArkData
            self.name_var.set(item_name)

    def toggle_method(self):
        """Переключение между поиском и ручным вводом"""
        method = self.method_var.get()
        
        if method == "search":
            self.search_frame.pack(fill=tk.X, pady=PADDING_SMALL)
            if hasattr(self, "manual_frame") and self.manual_frame.winfo_exists():
                self.manual_frame.pack_forget()
        else:
            if hasattr(self, "search_frame") and self.search_frame.winfo_exists():
                self.search_frame.pack_forget()
            self.manual_frame.pack(fill=tk.X, pady=PADDING_SMALL)
    
    def fill_form_with_item_data(self):
        """Заполнение формы данными существующего предмета"""
        self.blueprint_var.set(self.item_data.get("Blueprint", ""))
        self.name_var.set(self.item_data.get("Name", ""))
        self.price_var.set(str(self.item_data.get("Price", 0)))
        self.amount_var.set(str(self.item_data.get("Amount", 1)))
        self.quality_var.set(str(self.item_data.get("Quality", 0)))
        self.category_var.set(self.item_data.get("Category", "Weapons"))
        
        # Дополнительные настройки
        self.force_blueprint_var.set(self.item_data.get("ForceBlueprint", False))
        self.hide_until_unlocked_var.set(self.item_data.get("HideUntilUnlocked", False))
        self.block_in_buildings_var.set(self.item_data.get("BlockInBuildings", False))
        self.block_in_enemy_territory_var.set(self.item_data.get("BlockInEnemyTerritory", False))
    
    def save_item(self):
        """Сохранение данных предмета"""
        # Проверка ID
        item_id = self.id_var.get().strip()
        if not item_id:
            messagebox.showerror("Ошибка", "ID предмета не может быть пустым")
            return
            
        # Проверка Blueprint
        blueprint = self.blueprint_var.get().strip()
        if not blueprint:
            messagebox.showerror("Ошибка", "Blueprint не может быть пустым")
            return
            
        # Проверка названия
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Название не может быть пустым")
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
            
        # Проверка количества
        try:
            amount = int(self.amount_var.get())
            if amount < 1:
                messagebox.showerror("Ошибка", "Количество должно быть не меньше 1")
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
            
        # Формируем данные предмета
        item_data = {
            "Blueprint": blueprint,
            "Name": name,
            "Price": price,
            "Amount": amount,
            "Quality": quality,
            "Category": self.category_var.get(),
            "ForceBlueprint": self.force_blueprint_var.get(),
            "HideUntilUnlocked": self.hide_until_unlocked_var.get(),
            "BlockInBuildings": self.block_in_buildings_var.get(),
            "BlockInEnemyTerritory": self.block_in_enemy_territory_var.get()
        }
        
        # Сохраняем данные
        self.result = (item_id, item_data)
        self.dialog.destroy()
        if self.on_save:
            self.on_save(item_id, item_data)


class BlueprintSelectorDialog:
    """Диалоговое окно для выбора Blueprint из ArkData"""
    
    def __init__(self, parent, ark_data, blueprint_var):
        """
        Инициализирует диалоговое окно выбора Blueprint
        
        Args:
            parent: Родительское окно
            ark_data: Данные из ArkData.json
            blueprint_var: Переменная для сохранения выбранного Blueprint
        """
        self.parent = parent
        self.ark_data = ark_data
        self.blueprint_var = blueprint_var
        
        # Создаем модальное окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Выбор Blueprint")
        self.dialog.geometry("800x500")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.grab_set()  # Делаем окно модальным
        
        # Создаем фрейм для поиска
        search_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        search_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Переключатель между предметами и существами
        self.item_type_var = tk.StringVar(value="items")
        
        items_radio = ttk.Radiobutton(
            search_frame, 
            text="Предметы", 
            variable=self.item_type_var, 
            value="items",
            command=self.update_list
        )
        items_radio.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        creatures_radio = ttk.Radiobutton(
            search_frame, 
            text="Существа", 
            variable=self.item_type_var, 
            value="creatures",
            command=self.update_list
        )
        creatures_radio.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        # Поле для поиска
        search_label = tk.Label(search_frame, text="Поиск:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        search_label.pack(side=tk.LEFT, padx=(PADDING_MEDIUM, PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # При изменении текста в поле поиска вызываем функцию фильтрации
        self.search_var.trace_add("write", lambda *args: self.update_list())
        
        # Фрейм для списка Blueprint
        list_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
        
        # Добавляем прокрутку
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаем список с колонками
        self.blueprint_tree = ttk.Treeview(
            list_frame,
            columns=("name", "blueprint"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Настраиваем заголовки колонок
        self.blueprint_tree.heading("name", text="Название")
        self.blueprint_tree.heading("blueprint", text="Blueprint")
        
        # Настраиваем ширину колонок
        self.blueprint_tree.column("name", width=300)
        self.blueprint_tree.column("blueprint", width=500)
        
        self.blueprint_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.blueprint_tree.yview)
        
        # Связываем двойной клик по элементу с выбором Blueprint
        self.blueprint_tree.bind("<Double-1>", self.select_blueprint)
        
        # Фрейм с кнопками
        buttons_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Кнопка отмены
        cancel_button = tk.Button(
            buttons_frame,
            text="Отмена",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(PADDING_SMALL, 0))
        
        # Кнопка выбора
        select_button = tk.Button(
            buttons_frame,
            text="Выбрать",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.select_blueprint_button
        )
        select_button.pack(side=tk.RIGHT)
        
        # Заполняем список Blueprint
        self.update_list()
        
        # Ждем закрытия диалога
        self.dialog.wait_window()
    
    def update_list(self):
        """Обновляет список Blueprint в соответствии с поиском"""
        # Очищаем текущий список
        for item in self.blueprint_tree.get_children():
            self.blueprint_tree.delete(item)
        
        # Получаем тип данных (предметы или существа)
        item_type = self.item_type_var.get()
        
        # Получаем поисковый запрос
        search_text = self.search_var.get().lower()
        
        # Получаем данные из ArkData
        data = self.ark_data.get(item_type, {})
        
        # Фильтруем данные по поисковому запросу
        filtered_data = {}
        for name, item_data in data.items():
            if search_text in name.lower():
                filtered_data[name] = item_data
        
        # Добавляем отфильтрованные данные в список
        for name, item_data in filtered_data.items():
            blueprint = item_data.get("blueprint", "")
            self.blueprint_tree.insert("", "end", values=(name, blueprint))
    
    def select_blueprint(self, event):
        """Выбирает Blueprint при двойном клике и закрывает окно"""
        # Получаем выбранный элемент
        selected_item = self.blueprint_tree.selection()
        if not selected_item:
            return
        
        # Получаем Blueprint выбранного элемента
        blueprint = self.blueprint_tree.item(selected_item[0])['values'][1]
        
        # Устанавливаем Blueprint в переменную
        self.blueprint_var.set(blueprint)
        
        # Закрываем окно
        self.dialog.destroy()
    
    def select_blueprint_button(self):
        """Выбирает Blueprint при нажатии на кнопку и закрывает окно"""
        # Получаем выбранный элемент
        selected_item = self.blueprint_tree.selection()
        if not selected_item:
            messagebox.showinfo("Информация", "Выберите Blueprint из списка")
            return
        
        # Получаем Blueprint выбранного элемента
        blueprint = self.blueprint_tree.item(selected_item[0])['values'][1]
        
        # Устанавливаем Blueprint в переменную
        self.blueprint_var.set(blueprint)
        
        # Закрываем окно
        self.dialog.destroy()
