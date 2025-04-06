import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *
import json
import os

class AddShopItemDialog:
    """Диалоговое окно для добавления или редактирования товара магазина"""
    
    def __init__(self, parent, ark_data, item_id=None, item_data=None):
        """
        Инициализирует диалоговое окно
        
        Args:
            parent: Родительское окно
            ark_data: Данные из ArkData.json
            item_id: ID товара (если редактирование)
            item_data: Данные товара (если редактирование)
        """
        self.parent = parent
        self.ark_data = ark_data
        self.result = None
        
        # Создаем модальное окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавление товара" if item_id is None else "Редактирование товара")
        self.dialog.geometry("700x500")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.grab_set()  # Делаем окно модальным
        
        # Создаем фрейм с прокруткой для вмещения всех элементов
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Создаем контейнер для элементов формы
        form_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # ID товара
        row = 0
        id_label = tk.Label(form_frame, text="ID товара:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        id_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        self.id_var = tk.StringVar(value=item_id or "")
        id_entry = ttk.Entry(form_frame, textvariable=self.id_var, width=30)
        id_entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Подсказка для ID
        id_hint = tk.Label(
            form_frame,
            text="Уникальный идентификатор товара (например, '0001_Tool_Cryopod')",
            fg=GRAY_TEXT,
            bg=DARK_SECONDARY,
            font=FONT_SMALL
        )
        id_hint.grid(row=row, column=0, columnspan=2, sticky="w", padx=(PADDING_LARGE, PADDING_MEDIUM))
        row += 1
        
        # Название товара
        title_label = tk.Label(form_frame, text="Название:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        title_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        self.title_var = tk.StringVar(value=item_data.get("Title", "") if item_data else "")
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var, width=30)
        title_entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Описание
        desc_label = tk.Label(form_frame, text="Описание:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        desc_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        self.desc_var = tk.StringVar(value=item_data.get("Description", "") if item_data else "")
        desc_entry = ttk.Entry(form_frame, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Цена
        price_label = tk.Label(form_frame, text="Цена:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        price_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        self.price_var = tk.StringVar(value=str(item_data.get("Price", 1)) if item_data else "1")
        price_entry = ttk.Entry(form_frame, textvariable=self.price_var, width=10)
        price_entry.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Исключить из скидок
        self.exclude_discount_var = tk.BooleanVar(value=bool(item_data.get("Exclude_From_Discount", False)) if item_data else False)
        exclude_checkbox = ttk.Checkbutton(
            form_frame,
            text="Исключить из скидок",
            variable=self.exclude_discount_var
        )
        exclude_checkbox.grid(row=row, column=0, columnspan=2, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Категории
        categories_label = tk.Label(form_frame, text="Категории:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        categories_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        default_categories = []
        if item_data and "Categories" in item_data:
            default_categories = item_data["Categories"]
        
        self.categories_var = tk.StringVar(value=", ".join(default_categories))
        categories_entry = ttk.Entry(form_frame, textvariable=self.categories_var, width=30)
        categories_entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Подсказка для категорий
        categories_hint = tk.Label(
            form_frame,
            text="Список категорий через запятую (например, 'Tools, Consumables')",
            fg=GRAY_TEXT,
            bg=DARK_SECONDARY,
            font=FONT_SMALL
        )
        categories_hint.grid(row=row, column=0, columnspan=2, sticky="w", padx=(PADDING_LARGE, PADDING_MEDIUM))
        row += 1
        
        # Разделитель
        separator = ttk.Separator(form_frame, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=2, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Добавление предметов
        items_label = tk.Label(
            form_frame, 
            text="Blueprint предмета:", 
            fg=ORANGE_PRIMARY,
            bg=DARK_SECONDARY,
            font=FONT_SUBHEADER
        )
        items_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Blueprint
        self.blueprint_var = tk.StringVar(value="" if not item_data or not item_data.get("Items") else item_data["Items"][0].get("Blueprint", ""))
        blueprint_entry = ttk.Entry(form_frame, textvariable=self.blueprint_var, width=60)
        blueprint_entry.grid(row=row, column=0, columnspan=2, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Кнопка выбора из ArkData
        select_button = tk.Button(
            form_frame,
            text="Выбрать из базы данных",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.open_blueprint_selector
        )
        select_button.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        row += 1
        
        # Количество
        quantity_frame = tk.Frame(form_frame, bg=DARK_SECONDARY)
        quantity_frame.grid(row=row, column=0, columnspan=2, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        amount_label = tk.Label(quantity_frame, text="Количество:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        amount_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Значение по умолчанию для количества
        default_amount = 1
        if item_data and item_data.get("Items") and len(item_data["Items"]) > 0:
            default_amount = item_data["Items"][0].get("Amount", 1)
            
        self.amount_var = tk.StringVar(value=str(default_amount))
        amount_entry = ttk.Entry(quantity_frame, textvariable=self.amount_var, width=5)
        amount_entry.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        # Качество
        quality_label = tk.Label(quantity_frame, text="Качество:", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        quality_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Значение по умолчанию для качества
        default_quality = 0
        if item_data and item_data.get("Items") and len(item_data["Items"]) > 0:
            default_quality = item_data["Items"][0].get("Quality", 0)
            
        self.quality_var = tk.StringVar(value=str(default_quality))
        quality_entry = ttk.Entry(quantity_frame, textvariable=self.quality_var, width=5)
        quality_entry.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        # Чертеж
        default_force_bp = False
        if item_data and item_data.get("Items") and len(item_data["Items"]) > 0:
            default_force_bp = item_data["Items"][0].get("ForceBlueprint", False)
            
        self.force_bp_var = tk.BooleanVar(value=default_force_bp)
        force_bp_check = ttk.Checkbutton(quantity_frame, text="Чертёж", variable=self.force_bp_var)
        force_bp_check.pack(side=tk.LEFT)
        row += 1
        
        # Настройка весов для правильного растяжения
        form_frame.grid_columnconfigure(1, weight=1)
        
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
        
        # Кнопка сохранения
        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.save_item
        )
        save_button.pack(side=tk.RIGHT)
        
        # Ждем закрытия диалога
        self.dialog.wait_window()
    
    def open_blueprint_selector(self):
        """Открывает диалог выбора Blueprint из ArkData"""
        BlueprintSelectorDialog(self.dialog, self.ark_data, self.blueprint_var)
    
    def save_item(self):
        """Сохраняет данные о товаре и закрывает окно"""
        try:
            # Проверяем заполнение обязательных полей
            if not self.id_var.get().strip():
                messagebox.showerror("Ошибка", "ID товара не может быть пустым")
                return
            
            if not self.title_var.get().strip():
                messagebox.showerror("Ошибка", "Название товара не может быть пустым")
                return
            
            if not self.blueprint_var.get().strip():
                messagebox.showerror("Ошибка", "Blueprint не может быть пустым")
                return
            
            # Проверяем числовые поля
            try:
                price = int(self.price_var.get())
                amount = int(self.amount_var.get())
                quality = int(self.quality_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Цена, количество и качество должны быть целыми числами")
                return
            
            # Формируем список категорий из строки
            categories = [cat.strip() for cat in self.categories_var.get().split(",") if cat.strip()]
            
            # Формируем предмет
            item = {
                "Blueprint": self.blueprint_var.get(),
                "Amount": amount,
                "Quality": quality,
                "ForceBlueprint": self.force_bp_var.get()
            }
            
            # Формируем данные товара
            item_data = {
                "Title": self.title_var.get(),
                "Categories": categories,
                "Description": self.desc_var.get(),
                "Price": price,
                "Exclude_From_Discount": self.exclude_discount_var.get(),
                "Items": [item],
                "Dinos": [],
                "ConsoleCommands": [],
                "PermissionGroupRequired": [],
                "Only_On_These_Maps": [],
                "NOT_On_These_Maps": []
            }
            
            # Сохраняем результат
            self.result = {
                "id": self.id_var.get(),
                "data": item_data
            }
            
            # Закрываем окно
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении товара: {str(e)}")


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
