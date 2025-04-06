import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from ui.dialogs.shop_item_dialog import ShopItemDialog
from utils.memory_storage import memory_config

class ShopItemsSection(BaseSection):
    """Класс для отображения и редактирования раздела ShopItems"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела ShopItems"""
        # Основной контейнер с прокруткой
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Создаем верхнюю панель с кнопками
        control_panel = tk.Frame(main_frame, bg=DARK_SECONDARY)
        control_panel.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        # Заголовок секции
        title_label = tk.Label(
            control_panel,
            text="Управление товарами магазина",
            font=FONT_HEADER,
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        title_label.pack(side=tk.LEFT, pady=PADDING_SMALL)
        
        # Кнопка добавления товара
        add_button = tk.Button(
            control_panel,
            text="Добавить товар",
            bg=ORANGE_PRIMARY,
            fg=DARK_BG,
            command=self.add_shop_item
        )
        add_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
        
        # Кнопка удаления товара
        remove_button = tk.Button(
            control_panel,
            text="Удалить товар",
            bg=RED_BTN,
            fg=LIGHT_TEXT,
            command=self.remove_shop_item
        )
        remove_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
        
        # Создаем панель поиска
        search_panel = tk.Frame(main_frame, bg=DARK_SECONDARY)
        search_panel.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        search_label = tk.Label(
            search_panel,
            text="Поиск товара:",
            bg=DARK_SECONDARY,
            fg=LIGHT_TEXT
        )
        search_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_items)
        search_entry = ttk.Entry(search_panel, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Создаем таблицу для отображения товаров
        table_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Настраиваем столбцы таблицы
        columns = ("id", "title", "price", "categories")
        self.item_table = ttk.Treeview(
            table_frame, 
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Заголовки столбцов
        self.item_table.heading("id", text="ID")
        self.item_table.heading("title", text="Название")
        self.item_table.heading("price", text="Цена")
        self.item_table.heading("categories", text="Категории")
        
        # Настройка ширины столбцов
        self.item_table.column("id", width=150, anchor="w")
        self.item_table.column("title", width=200, anchor="w")
        self.item_table.column("price", width=100, anchor="center")
        self.item_table.column("categories", width=250, anchor="w")
        
        # Добавляем прокрутку для таблицы
        table_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.item_table.yview)
        self.item_table.configure(yscrollcommand=table_scroll.set)
        self.item_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Добавляем обработчик двойного клика для редактирования
        self.item_table.bind("<Double-1>", self.edit_shop_item)
        
        # Загружаем список товаров
        self.load_shop_items()
    
    def add_shop_item(self):
        """Открывает диалог для добавления нового товара"""
        # Загружаем данные из ARK Data для автозаполнения
        ark_data = self.load_ark_data()
        
        # Создаем диалоговое окно
        dialog = ShopItemDialog(
            self.parent,
            ark_data=ark_data,
            on_save=self.save_new_item
        )
    
    def edit_shop_item(self, event=None):
        """Открывает диалог для редактирования выбранного товара"""
        # Получаем выбранный элемент
        selected_items = self.item_table.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите товар для редактирования")
            return
        
        selected_id = self.item_table.item(selected_items[0])['values'][0]
        shop_items = memory_config.get("ShopItems", {})
        
        if selected_id not in shop_items:
            messagebox.showerror("Ошибка", f"Товар с ID {selected_id} не найден")
            return
        
        # Загружаем данные из ARK Data для автозаполнения
        ark_data = self.load_ark_data()
        
        # Создаем диалоговое окно
        dialog = ShopItemDialog(
            self.parent,
            ark_data=ark_data,
            on_save=lambda item_id, data: self.save_edited_item(selected_id, item_id, data),
            item_data=shop_items[selected_id],
            item_id=selected_id
        )
    
    def remove_shop_item(self):
        """Удаляет выбранный товар"""
        # Получаем выбранный элемент
        selected_items = self.item_table.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите товар для удаления")
            return
        
        selected_id = self.item_table.item(selected_items[0])['values'][0]
        shop_items = memory_config.get("ShopItems", {})
        
        if selected_id not in shop_items:
            messagebox.showerror("Ошибка", f"Товар с ID {selected_id} не найден")
            return
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить товар '{selected_id}'?"):
            # Удаляем товар
            del shop_items[selected_id]
            memory_config["ShopItems"] = shop_items
            
            # Обновляем таблицу
            self.load_shop_items()
    
    def save_new_item(self, item_id, item_data):
        """Сохраняет новый товар в конфигурацию"""
        shop_items = memory_config.get("ShopItems", {})
        
        # Проверяем существование товара с таким ID
        if item_id in shop_items:
            response = messagebox.askyesno(
                "Подтверждение", 
                f"Товар с ID '{item_id}' уже существует. Хотите перезаписать его?"
            )
            if not response:
                return
        
        # Сохраняем товар
        shop_items[item_id] = item_data
        memory_config["ShopItems"] = shop_items
        
        # Обновляем таблицу
        self.load_shop_items()
        
        # Выводим сообщение об успехе
        messagebox.showinfo("Успех", f"Товар '{item_id}' успешно сохранен")
    
    def save_edited_item(self, old_id, new_id, item_data):
        """Сохраняет отредактированный товар в конфигурацию"""
        shop_items = memory_config.get("ShopItems", {})
        
        # Если ID изменился и новый ID уже существует
        if old_id != new_id and new_id in shop_items:
            response = messagebox.askyesno(
                "Подтверждение", 
                f"Товар с ID '{new_id}' уже существует. Хотите перезаписать его?"
            )
            if not response:
                return
        
        # Удаляем старый товар
        if old_id in shop_items:
            del shop_items[old_id]
        
        # Сохраняем товар с новым ID
        shop_items[new_id] = item_data
        memory_config["ShopItems"] = shop_items
        
        # Обновляем таблицу
        self.load_shop_items()
        
        # Выводим сообщение об успехе
        messagebox.showinfo("Успех", f"Товар '{new_id}' успешно обновлен")
    
    def load_shop_items(self):
        """Загружает и отображает список товаров"""
        # Очищаем таблицу
        for item in self.item_table.get_children():
            self.item_table.delete(item)
        
        # Получаем данные товаров
        shop_items = memory_config.get("ShopItems", {})
        
        # Добавляем товары в таблицу
        for item_id, item_data in shop_items.items():
            title = item_data.get("Title", "Без названия")
            price = item_data.get("Price", 0)
            categories = ", ".join(item_data.get("Categories", []))
            
            self.item_table.insert("", "end", values=(item_id, title, price, categories))
    
    def filter_items(self, *args):
        """Фильтрует товары по поисковому запросу"""
        search_text = self.search_var.get().lower()
        
        # Очищаем таблицу
        for item in self.item_table.get_children():
            self.item_table.delete(item)
        
        # Получаем данные товаров
        shop_items = memory_config.get("ShopItems", {})
        
        # Фильтруем и добавляем товары в таблицу
        for item_id, item_data in shop_items.items():
            title = item_data.get("Title", "Без названия")
            price = item_data.get("Price", 0)
            categories = ", ".join(item_data.get("Categories", []))
            
            # Проверяем соответствие поисковому запросу
            if (search_text in item_id.lower() or 
                search_text in title.lower() or 
                search_text in categories.lower()):
                self.item_table.insert("", "end", values=(item_id, title, price, categories))
    
    def load_ark_data(self):
        """Загружает данные из файла ArkData.json"""
        try:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "ArkData.json"
            )
            
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Ошибка при загрузке ArkData: {e}")
            return {"items": {}, "creatures": {}}
    
    def refresh(self):
        """Обновляет содержимое секции"""
        self.load_shop_items()
