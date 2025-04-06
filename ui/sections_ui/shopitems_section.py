import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from ui.dialogs.add_shop_item_dialog import AddShopItemDialog
from utils.memory_storage import memory_config

class ShopItemsSection(BaseSection):
    """Класс для отображения настроек раздела ShopItems"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела ShopItems"""
        # Основной контейнер с прокруткой
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Создаем Canvas с прокруткой
        canvas = tk.Canvas(main_frame, bg=DARK_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=DARK_SECONDARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заголовок секции
        header = tk.Label(
            scrollable_frame, 
            text="Товары магазина (ShopItems)", 
            font=FONT_HEADER, 
            bg=DARK_SECONDARY, 
            fg=LIGHT_TEXT
        )
        header.pack(anchor="w", pady=(0, PADDING_MEDIUM))
        
        # Панель поиска
        search_frame = tk.Frame(scrollable_frame, bg=DARK_SECONDARY)
        search_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        search_label = tk.Label(search_frame, text="Поиск:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        search_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT)
        
        self.search_var.trace("w", self.filter_items)
        
        # Кнопка для добавления нового предмета
        add_button = tk.Button(
            search_frame,
            text="Добавить предмет",
            bg=ORANGE_PRIMARY,
            fg=DARK_BG,
            command=self.add_shop_item
        )
        add_button.pack(side=tk.RIGHT)
        
        # Кнопки для редактирования и удаления предмета
        edit_button = tk.Button(
            search_frame,
            text="Редактировать",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.edit_shop_item
        )
        edit_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
        
        delete_button = tk.Button(
            search_frame,
            text="Удалить",
            bg=BUTTON_BG,
            fg=LIGHT_TEXT,
            command=self.delete_shop_item
        )
        delete_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
        
        # Создаем список предметов
        self.items_listbox = tk.Listbox(scrollable_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=25, width=80)
        self.items_listbox.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        self.items_listbox.bind("<Double-1>", lambda e: self.edit_shop_item())
        
        # Загружаем предметы из конфигурации
        self.load_shop_items()
    
    def load_shop_items(self):
        """Загрузка предметов из конфигурации"""
        self.items_listbox.delete(0, tk.END)
        
        shop_items = memory_config.get("ShopItems", {})
        
        # Создаем словарь для хранения полной информации о предметах
        self.shop_items_data = {}
        
        for item_id, item_data in shop_items.items():
            display_name = item_data.get("Name", "Без имени")
            price = item_data.get("Price", 0)
            display_text = f"{item_id} - {display_name} (Цена: {price})"
            
            self.items_listbox.insert(tk.END, display_text)
            self.shop_items_data[display_text] = (item_id, item_data)
            
    def filter_items(self, *args):
        """Фильтрация предметов по поисковому запросу"""
        search_term = self.search_var.get().lower()
        self.items_listbox.delete(0, tk.END)
        
        shop_items = memory_config.get("ShopItems", {})
        
        # Очищаем данные
        self.shop_items_data = {}
        
        for item_id, item_data in shop_items.items():
            display_name = item_data.get("Name", "Без имени")
            price = item_data.get("Price", 0)
            display_text = f"{item_id} - {display_name} (Цена: {price})"
            
            # Фильтрация по ID или имени
            if search_term in item_id.lower() or search_term in display_name.lower():
                self.items_listbox.insert(tk.END, display_text)
                self.shop_items_data[display_text] = (item_id, item_data)
    
    def add_shop_item(self):
        """Открывает диалог для добавления нового предмета в магазин"""
        # Загружаем данные элементов ARK для автозаполнения
        ark_data = self.load_ark_data()
        
        dialog = AddShopItemDialog(self.parent, ark_data, self.save_new_item)
    
    def edit_shop_item(self):
        """Открывает диалог для редактирования выбранного предмета"""
        selected_index = self.items_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Информация", "Выберите предмет для редактирования")
            return
        
        selected_text = self.items_listbox.get(selected_index)
        item_id, item_data = self.shop_items_data.get(selected_text, (None, None))
        
        if not item_id:
            messagebox.showerror("Ошибка", "Не удалось найти данные предмета")
            return
        
        # Загружаем данные элементов ARK для автозаполнения
        ark_data = self.load_ark_data()
        
        # Открываем диалог редактирования
        dialog = AddShopItemDialog(
            self.parent, 
            ark_data, 
            lambda new_id, data: self.save_edited_item(item_id, new_id, data),
            item_data,
            item_id
        )
    
    def delete_shop_item(self):
        """Удаляет выбранный предмет из магазина"""
        selected_index = self.items_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Информация", "Выберите предмет для удаления")
            return
            
        selected_text = self.items_listbox.get(selected_index)
        item_id, _ = self.shop_items_data.get(selected_text, (None, None))
        
        if not item_id:
            messagebox.showerror("Ошибка", "Не удалось найти данные предмета")
            return
            
        # Запрашиваем подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить предмет '{item_id}'?"):
            shop_items = memory_config.get("ShopItems", {})
            if item_id in shop_items:
                del shop_items[item_id]
                memory_config["ShopItems"] = shop_items
                self.load_shop_items()
    
    def save_new_item(self, item_id, item_data):
        """Сохраняет новый предмет в конфигурацию"""
        shop_items = memory_config.get("ShopItems", {})
        
        # Проверяем, существует ли предмет с таким ID
        if item_id in shop_items:
            messagebox.showwarning(
                "Предупреждение", 
                f"Предмет с ID '{item_id}' уже существует и будет перезаписан"
            )
        
        # Сохраняем предмет
        shop_items[item_id] = item_data
        memory_config["ShopItems"] = shop_items
        
        # Обновляем список предметов
        self.load_shop_items()
    
    def save_edited_item(self, old_id, new_id, item_data):
        """Сохраняет отредактированный предмет в конфигурацию"""
        shop_items = memory_config.get("ShopItems", {})
        
        # Удаляем старый предмет
        if old_id in shop_items:
            del shop_items[old_id]
        
        # Проверяем, существует ли предмет с новым ID (если он изменился)
        if old_id != new_id and new_id in shop_items:
            messagebox.showwarning(
                "Предупреждение", 
                f"Предмет с ID '{new_id}' уже существует и будет перезаписан"
            )
        
        # Сохраняем предмет с новым ID
        shop_items[new_id] = item_data
        memory_config["ShopItems"] = shop_items
        
        # Обновляем список предметов
        self.load_shop_items()
    
    def load_ark_data(self):
        """Загружает данные о предметах и динозаврах из файла ArkData.json"""
        try:
            ark_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ArkData.json")
            with open(ark_data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Ошибка при загрузке данных ARK: {e}")
            return {"items": {}, "creatures": {}}
