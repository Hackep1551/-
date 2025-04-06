import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from ui.dialogs.add_kit_dialog import AddKitDialog
from utils.memory_storage import memory_config

class KitsSection(BaseSection):
    """Класс для отображения настроек раздела Kits"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела Kits"""
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
            text="Наборы (Kits)", 
            font=FONT_HEADER, 
            bg=DARK_SECONDARY, 
            fg=LIGHT_TEXT
        )
        header.pack(anchor="w", pady=(0, PADDING_MEDIUM))
        
        # Кнопки для управления наборами
        buttons_frame = tk.Frame(scrollable_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        add_button = tk.Button(
            buttons_frame, 
            text="Добавить набор", 
            bg=ORANGE_PRIMARY, 
            fg=DARK_BG,
            command=self.add_kit
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        edit_button = tk.Button(
            buttons_frame, 
            text="Изменить набор", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.edit_kit
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            buttons_frame, 
            text="Удалить набор", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_kit
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем таблицу наборов
        table_frame = tk.Frame(scrollable_frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        # Определяем колонки таблицы
        columns = ("id", "title", "price", "items", "commands")
        self.kits_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настраиваем заголовки и ширину колонок
        self.kits_tree.heading("id", text="ID набора")
        self.kits_tree.heading("title", text="Название")
        self.kits_tree.heading("price", text="Цена")
        self.kits_tree.heading("items", text="Кол-во предметов")
        self.kits_tree.heading("commands", text="Консольные команды")
        
        self.kits_tree.column("id", width=150)
        self.kits_tree.column("title", width=200)
        self.kits_tree.column("price", width=80)
        self.kits_tree.column("items", width=120)
        self.kits_tree.column("commands", width=150)
        
        # Добавляем скроллбары
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.kits_tree.yview)
        self.kits_tree.configure(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.kits_tree.xview)
        self.kits_tree.configure(xscrollcommand=x_scrollbar.set)
        
        # Размещаем элементы на фрейме
        self.kits_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Обновляем таблицу
        self.update_kits_list()
        
        # Двойной клик для редактирования
        self.kits_tree.bind("<Double-1>", lambda e: self.edit_kit())

    def update_kits_list(self):
        """Обновляет список наборов в таблице"""
        # Очищаем таблицу
        for item in self.kits_tree.get_children():
            self.kits_tree.delete(item)
        
        # Получаем данные о наборах из памяти
        kits_data = memory_config.get("Kits", {})
        
        # Заполняем таблицу
        for kit_id, kit_data in kits_data.items():
            title = kit_data.get("Title", "")
            price = kit_data.get("Price", 0)
            items_count = len(kit_data.get("Items", []))
            commands_count = len(kit_data.get("ConsoleCommands", []))
            
            self.kits_tree.insert("", "end", values=(kit_id, title, price, items_count, commands_count))

    def add_kit(self):
        """Открывает диалог для добавления нового набора"""
        # Загрузка данных о предметах и динозаврах для автозаполнения
        ark_data = self.load_ark_data()
        
        dialog = AddKitDialog(
            self.parent,
            items_data=ark_data.get("items", {}),
            dinos_data=ark_data.get("creatures", {}),
            on_save=self.save_new_kit
        )

    def edit_kit(self):
        """Открывает диалог для редактирования выбранного набора"""
        # Получаем выбранный набор
        selected_items = self.kits_tree.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите набор для редактирования")
            return
        
        # Получаем ID выбранного набора
        kit_id = self.kits_tree.item(selected_items[0], "values")[0]
        
        # Получаем данные о наборе
        kits_data = memory_config.get("Kits", {})
        kit_data = kits_data.get(kit_id, {})
        
        # Загрузка данных о предметах и динозаврах для автозаполнения
        ark_data = self.load_ark_data()
        
        # Открываем диалог редактирования
        dialog = AddKitDialog(
            self.parent,
            items_data=ark_data.get("items", {}),
            dinos_data=ark_data.get("creatures", {}),
            on_save=lambda id, data: self.save_edited_kit(kit_id, data),
            kit_data=kit_data,
            kit_id=kit_id
        )
    
    def delete_kit(self):
        """Удаляет выбранный набор"""
        # Получаем выбранный набор
        selected_items = self.kits_tree.selection()
        if not selected_items:
            messagebox.showinfo("Информация", "Выберите набор для удаления")
            return
        
        # Получаем ID выбранного набора
        kit_id = self.kits_tree.item(selected_items[0], "values")[0]
        
        # Запрашиваем подтверждение
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить набор '{kit_id}'?"):
            return
        
        # Удаляем набор из памяти
        kits_data = memory_config.get("Kits", {})
        if kit_id in kits_data:
            del kits_data[kit_id]
            memory_config["Kits"] = kits_data
            self.update_kits_list()
    
    def save_new_kit(self, kit_id, kit_data):
        """Сохраняет новый набор"""
        # Проверяем, существует ли раздел Kits
        if "Kits" not in memory_config:
            memory_config["Kits"] = {}
            
        # Проверяем, существует ли уже такой набор
        if kit_id in memory_config["Kits"]:
            if not messagebox.askyesno("Подтверждение", f"Набор с ID '{kit_id}' уже существует. Перезаписать?"):
                return
        
        # Сохраняем набор
        memory_config["Kits"][kit_id] = kit_data
        
        # Обновляем список наборов
        self.update_kits_list()
    
    def save_edited_kit(self, kit_id, kit_data):
        """Сохраняет отредактированный набор"""
        # Проверяем, существует ли раздел Kits
        if "Kits" not in memory_config:
            memory_config["Kits"] = {}
        
        # Сохраняем набор
        memory_config["Kits"][kit_id] = kit_data
        
        # Обновляем список наборов
        self.update_kits_list()
    
    def load_ark_data(self):
        """Загружает данные о предметах и динозаврах из файла ArkData.json"""
        import json
        import os
        
        try:
            ark_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ArkData.json")
            with open(ark_data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Ошибка при загрузке данных ARK: {e}")
            return {"items": {}, "creatures": {}}
