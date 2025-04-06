import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from utils.memory_storage import memory_config

class ShopItemsSection(BaseSection):
    """Класс для отображения и редактирования предметов магазина"""
    
    def setup_ui(self):
        """Настройка интерфейса для ShopItemsSection"""
        # Загружаем данные о предметах из файла ArkData.json
        self.items_data = {}
        self.load_ark_data()
        
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Верхняя панель с заголовком и кнопками
        header_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        header_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        # Заголовок
        header = tk.Label(header_frame, text="Предметы магазина", font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(side=tk.LEFT)
        
        # Кнопка добавления нового предмета
        add_button = tk.Button(
            header_frame, 
            text="Добавить предмет", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.add_shop_item
        )
        add_button.pack(side=tk.RIGHT)
        
        # Создаем рамку с таблицей предметов и кнопками
        list_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем таблицу предметов
        columns = ("id", "name", "price", "category", "description")
        self.items_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # Настраиваем заголовки колонок
        self.items_tree.heading("id", text="ID")
        self.items_tree.heading("name", text="Название")
        self.items_tree.heading("price", text="Цена")
        self.items_tree.heading("category", text="Категория")
        self.items_tree.heading("description", text="Описание")
        
        # Настройка ширины колонок
        self.items_tree.column("id", width=50)
        self.items_tree.column("name", width=200)
        self.items_tree.column("price", width=80)
        self.items_tree.column("category", width=150)
        self.items_tree.column("description", width=300)
        
        # Добавление вертикальной прокрутки
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=vsb.set)
        
        # Добавление горизонтальной прокрутки
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.items_tree.xview)
        self.items_tree.configure(xscrollcommand=hsb.set)
        
        # Размещаем таблицу и полосы прокрутки
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Привязываем двойной клик для редактирования
        self.items_tree.bind("<Double-1>", lambda e: self.edit_shop_item())
        
        # Кнопки для действий с выбранным предметом
        button_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        button_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        edit_button = tk.Button(
            button_frame, 
            text="Редактировать", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.edit_shop_item
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        duplicate_button = tk.Button(
            button_frame, 
            text="Дублировать", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.duplicate_shop_item
        )
        duplicate_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            button_frame, 
            text="Удалить", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_shop_item
        )
        delete_button.pack(side=tk.LEFT)
        
        # Заполняем таблицу предметами из конфигурации
        self.populate_items_tree()
    
    def load_ark_data(self):
        """Загружает данные о предметах из ArkData.json"""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ArkData.json")
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf-8') as file:
                    ark_data = json.load(file)
                    self.items_data = ark_data.get("items", {})
        except Exception as e:
            print(f"Ошибка при загрузке данных из ArkData.json: {e}")
    
    def populate_items_tree(self):
        """Заполняет таблицу предметами из конфигурации"""
        # Очищаем таблицу
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Получаем предметы из конфигурации
        shop_items = self.config_data or {}
        
        # Заполняем таблицу данными
        for item_id, item_data in shop_items.items():
            self.items_tree.insert("", "end", values=(
                item_id,
                item_data.get("Name", ""),
                item_data.get("Price", 0),
                item_data.get("Category", ""),
                item_data.get("Description", "")
            ))
    
    def add_shop_item(self):
        """Добавляет новый предмет в магазин"""
        # Здесь будет реализована функция добавления предмета
        messagebox.showinfo("Информация", "Функция добавления предмета будет реализована позже")
    
    def edit_shop_item(self):
        """Редактирует выбранный предмет магазина"""
        # Получаем выбранную строку
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите предмет для редактирования")
            return
        
        # Здесь будет реализована функция редактирования предмета
        messagebox.showinfo("Информация", "Функция редактирования предмета будет реализована позже")
    
    def duplicate_shop_item(self):
        """Дублирует выбранный предмет магазина"""
        # Получаем выбранную строку
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите предмет для дублирования")
            return
        
        # Получаем ID выбранного предмета
        item_id = self.items_tree.item(selected[0])["values"][0]
        
        # Проверяем, существует ли такой предмет в конфигурации
        if item_id not in self.config_data:
            messagebox.showerror("Ошибка", f"Предмет с ID '{item_id}' не найден в конфигурации")
            return
        
        # Запрашиваем новый ID
        new_id = simpledialog.askstring(
            "Дублирование предмета", 
            "Введите ID для нового предмета:", 
            initialvalue=f"{item_id}_copy"
        )
        
        if not new_id:
            return
        
        if new_id in self.config_data:
            messagebox.showerror("Ошибка", f"Предмет с ID '{new_id}' уже существует")
            return
        
        # Копируем предмет
        self.config_data[new_id] = self.config_data[item_id].copy()
        
        # Обновляем данные в памяти
        memory_config[self.section_name] = self.config_data
        
        # Обновляем таблицу
        self.populate_items_tree()
    
    def delete_shop_item(self):
        """Удаляет выбранный предмет магазина"""
        # Получаем выбранную строку
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите предмет для удаления")
            return
        
        # Получаем ID выбранного предмета
        item_id = self.items_tree.item(selected[0])["values"][0]
        
        # Запрашиваем подтверждение
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить предмет с ID '{item_id}'?"):
            return
        
        # Удаляем предмет
        if item_id in self.config_data:
            del self.config_data[item_id]
            
            # Обновляем данные в памяти
            memory_config[self.section_name] = self.config_data
            
            # Обновляем таблицу
            self.populate_items_tree()
