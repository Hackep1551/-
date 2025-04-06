import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from ui.constants import *
from ui.dialogs.add_kit_item_dialog import AddKitItemDialog
from ui.dialogs.add_kit_dino_dialog import AddKitDinoDialog
from ui.dialogs.add_kit_command_dialog import AddKitCommandDialog

class AddKitDialog:
    """Класс диалогового окна для добавления набора"""
    
    def __init__(self, parent, items_data=None, dinos_data=None, on_save=None, kit_data=None, kit_id=None):
        """
        Инициализация диалогового окна
        
        Args:
            parent: родительское окно
            items_data: словарь с данными о предметах
            dinos_data: словарь с данными о динозаврах
            on_save: функция обратного вызова при сохранении
            kit_data: данные о редактируемом наборе (если редактирование)
            kit_id: ID набора (если редактирование)
        """
        self.parent = parent
        self.items_data = items_data or {}
        self.dinos_data = dinos_data or {}
        self.on_save = on_save
        self.kit_data = kit_data or {}
        self.kit_id = kit_id
        self.result = None
        
        # Данные набора
        if self.kit_data:
            self.kit_items = self.kit_data.get("Items", [])
            self.kit_dinos = self.kit_data.get("Dinos", [])
            self.kit_commands = self.kit_data.get("ConsoleCommands", [])
            self.permission_groups = self.kit_data.get("PermissionGroupRequired", [])
        else:
            self.kit_items = []
            self.kit_dinos = []
            self.kit_commands = []
            self.permission_groups = []
        
        # Создаем диалоговое окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить набор" if not kit_id else f"Редактировать набор: {kit_id}")
        # Увеличиваем размер окна для лучшего размещения контента
        self.dialog.geometry("1000x800")
        self.dialog.configure(bg=DARK_SECONDARY)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрируем окно относительно экрана, а не родителя
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # Если есть данные для редактирования, заполняем поля
        if self.kit_data:
            self.title_var.set(self.kit_data.get("Title", ""))
            self.description_var.set(self.kit_data.get("Description", ""))
            self.price_var.set(str(self.kit_data.get("Price", 0)))
            self.default_amount_var.set(str(self.kit_data.get("DefaultAmount", 1)))
            self.only_from_spawn_var.set(self.kit_data.get("OnlyFromSpawn", False))
            self.auto_give_on_spawn_var.set(self.kit_data.get("AutoGiveOnSpawn", False))
            self.exclude_from_discount_var.set(self.kit_data.get("Exclude_From_Discount", False))
            self.icon_var.set(self.kit_data.get("Icon", ""))
            
            # Заполняем значения лимитов, если они есть
            limits = self.kit_data.get("Limits", {})
            self.max_purchase_same_time_var.set(str(limits.get("Max_Purchase_Same_Time_Amount", 1)))
            self.max_purchases_uses_var.set(str(limits.get("Max_Purchases/Uses", 100)))
            self.prevent_usage_after_wipe_var.set(str(limits.get("Prevent_Usage_After_Wipe_For_Minutes", 0)))
            self.cooldown_days_var.set(str(limits.get("Cooldown_Days", 0)))
            self.cooldown_hours_var.set(str(limits.get("Cooldown_Hours", 0)))
            self.cooldown_minutes_var.set(str(limits.get("Cooldown_Minutes", 0)))
            self.cooldown_seconds_var.set(str(limits.get("Cooldown_Seconds", 0)))
            
            # Заполняем списки
            self.update_items_list()
            self.update_dinos_list()
            self.update_commands_list()
            self.update_permissions_list()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер с прокруткой
        main_frame = tk.Frame(self.dialog, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Верхняя часть - основные настройки набора
        settings_frame = tk.LabelFrame(main_frame, text="Настройки набора", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        settings_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        # ID набора
        if not self.kit_id:
            id_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
            id_frame.pack(fill=tk.X, pady=PADDING_SMALL)
            
            id_label = tk.Label(id_frame, text="ID набора:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
            id_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
            
            self.id_var = tk.StringVar()
            id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=30)
            id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            id_hint = tk.Label(id_frame, text="(например, 00001_starter)", bg=DARK_SECONDARY, fg=GRAY_TEXT)
            id_hint.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Название набора
        title_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        title_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        title_label = tk.Label(title_frame, text="Название:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        title_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(title_frame, textvariable=self.title_var, width=40)
        title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Описание набора
        desc_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        desc_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        desc_label = tk.Label(desc_frame, text="Описание:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        desc_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.description_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.description_var, width=60)
        desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Цена набора
        price_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        price_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        price_label = tk.Label(price_frame, text="Цена:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        price_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.price_var = tk.StringVar(value="0")
        price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=10)
        price_entry.pack(side=tk.LEFT)
        
        # Количество по умолчанию
        amount_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        amount_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        amount_label = tk.Label(amount_frame, text="Количество по умолчанию:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        amount_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.default_amount_var = tk.StringVar(value="1")
        amount_entry = ttk.Entry(amount_frame, textvariable=self.default_amount_var, width=5)
        amount_entry.pack(side=tk.LEFT)
        
        # Иконка набора
        icon_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        icon_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        icon_label = tk.Label(icon_frame, text="Иконка:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        icon_label.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.icon_var = tk.StringVar()
        icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_var, width=60)
        icon_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Дополнительные флажки
        checkboxes_frame = tk.Frame(settings_frame, bg=DARK_SECONDARY)
        checkboxes_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.only_from_spawn_var = tk.BooleanVar(value=False)
        only_from_spawn_cb = ttk.Checkbutton(
            checkboxes_frame, 
            text="Выдавать только из точки спауна", 
            variable=self.only_from_spawn_var
        )
        only_from_spawn_cb.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        self.auto_give_on_spawn_var = tk.BooleanVar(value=False)
        auto_give_cb = ttk.Checkbutton(
            checkboxes_frame, 
            text="Автоматическая выдача при спауне", 
            variable=self.auto_give_on_spawn_var
        )
        auto_give_cb.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
        
        self.exclude_from_discount_var = tk.BooleanVar(value=False)
        exclude_discount_cb = ttk.Checkbutton(
            checkboxes_frame, 
            text="Исключить из системы скидок", 
            variable=self.exclude_from_discount_var
        )
        exclude_discount_cb.pack(side=tk.LEFT)
        
        # Добавляем фрейм для лимитов использования
        limits_frame = tk.LabelFrame(main_frame, text="Лимиты использования", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        limits_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        # Создаем сетку для более компактного размещения
        limits_grid = tk.Frame(limits_frame, bg=DARK_SECONDARY)
        limits_grid.pack(fill=tk.X)
        
        # Максимальное количество покупок за раз
        max_purchase_same_time_label = tk.Label(limits_grid, text="Макс. кол-во покупок за раз:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        max_purchase_same_time_label.grid(row=0, column=0, sticky="w", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.max_purchase_same_time_var = tk.StringVar(value="1")
        max_purchase_same_time_entry = ttk.Entry(limits_grid, textvariable=self.max_purchase_same_time_var, width=8)
        max_purchase_same_time_entry.grid(row=0, column=1, sticky="w", pady=PADDING_SMALL)
        
        # Максимальное количество покупок/использований
        max_purchases_uses_label = tk.Label(limits_grid, text="Макс. кол-во покупок/использований:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        max_purchases_uses_label.grid(row=0, column=2, sticky="w", padx=(PADDING_MEDIUM, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.max_purchases_uses_var = tk.StringVar(value="100")
        max_purchases_uses_entry = ttk.Entry(limits_grid, textvariable=self.max_purchases_uses_var, width=8)
        max_purchases_uses_entry.grid(row=0, column=3, sticky="w", pady=PADDING_SMALL)
        
        # Время блокировки после вайпа (в минутах)
        prevent_usage_after_wipe_label = tk.Label(limits_grid, text="Блокировка после вайпа (мин.):", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        prevent_usage_after_wipe_label.grid(row=1, column=0, sticky="w", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.prevent_usage_after_wipe_var = tk.StringVar(value="0")
        prevent_usage_after_wipe_entry = ttk.Entry(limits_grid, textvariable=self.prevent_usage_after_wipe_var, width=8)
        prevent_usage_after_wipe_entry.grid(row=1, column=1, sticky="w", pady=PADDING_SMALL)
        
        # Время перезарядки - заголовок
        cooldown_label = tk.Label(limits_grid, text="Время перезарядки:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        cooldown_label.grid(row=2, column=0, sticky="w", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        # Дни перезарядки
        cooldown_days_label = tk.Label(limits_grid, text="Дни:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        cooldown_days_label.grid(row=3, column=0, sticky="e", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.cooldown_days_var = tk.StringVar(value="0")
        cooldown_days_entry = ttk.Entry(limits_grid, textvariable=self.cooldown_days_var, width=8)
        cooldown_days_entry.grid(row=3, column=1, sticky="w", pady=PADDING_SMALL)
        
        # Часы перезарядки
        cooldown_hours_label = tk.Label(limits_grid, text="Часы:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        cooldown_hours_label.grid(row=3, column=2, sticky="e", padx=(PADDING_MEDIUM, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.cooldown_hours_var = tk.StringVar(value="0")
        cooldown_hours_entry = ttk.Entry(limits_grid, textvariable=self.cooldown_hours_var, width=8)
        cooldown_hours_entry.grid(row=3, column=3, sticky="w", pady=PADDING_SMALL)
        
        # Минуты перезарядки
        cooldown_minutes_label = tk.Label(limits_grid, text="Минуты:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        cooldown_minutes_label.grid(row=4, column=0, sticky="e", padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.cooldown_minutes_var = tk.StringVar(value="0")
        cooldown_minutes_entry = ttk.Entry(limits_grid, textvariable=self.cooldown_minutes_var, width=8)
        cooldown_minutes_entry.grid(row=4, column=1, sticky="w", pady=PADDING_SMALL)
        
        # Секунды перезарядки
        cooldown_seconds_label = tk.Label(limits_grid, text="Секунды:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        cooldown_seconds_label.grid(row=4, column=2, sticky="e", padx=(PADDING_MEDIUM, PADDING_SMALL), pady=PADDING_SMALL)
        
        self.cooldown_seconds_var = tk.StringVar(value="0")
        cooldown_seconds_entry = ttk.Entry(limits_grid, textvariable=self.cooldown_seconds_var, width=8)
        cooldown_seconds_entry.grid(row=4, column=3, sticky="w", pady=PADDING_SMALL)
        
        # Создаем Notebook для вкладок с предметами, динозаврами и командами
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка предметов
        items_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(items_tab, text="Предметы")
        self.setup_items_tab(items_tab)
        
        # Вкладка динозавров
        dinos_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(dinos_tab, text="Динозавры")
        self.setup_dinos_tab(dinos_tab)
        
        # Вкладка консольных команд
        commands_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(commands_tab, text="Консольные команды")
        self.setup_commands_tab(commands_tab)
        
        # Вкладка разрешений
        permissions_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(permissions_tab, text="Разрешения")
        self.setup_permissions_tab(permissions_tab)
        
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
            command=self.save_kit
        )
        save_button.pack(side=tk.RIGHT)
    
    def setup_items_tab(self, parent):
        """Настройка вкладки предметов"""
        # Создаем фрейм для списка предметов и кнопок управления
        frame = tk.Frame(parent, bg=DARK_SECONDARY)
        frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Кнопки управления предметами
        buttons_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(0, PADDING_SMALL))
        
        add_button = tk.Button(
            buttons_frame, 
            text="Добавить предмет", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.add_item
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        edit_button = tk.Button(
            buttons_frame, 
            text="Изменить предмет", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.edit_item
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            buttons_frame, 
            text="Удалить предмет", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_item
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем таблицу предметов
        table_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Определяем колонки таблицы
        columns = ("blueprint", "amount", "quality", "force_bp")
        self.items_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настраиваем заголовки
        self.items_tree.heading("blueprint", text="Blueprint")
        self.items_tree.heading("amount", text="Количество")
        self.items_tree.heading("quality", text="Качество")
        self.items_tree.heading("force_bp", text="Чертеж")
        
        # Настраиваем ширину колонок
        self.items_tree.column("blueprint", width=400)
        self.items_tree.column("amount", width=80)
        self.items_tree.column("quality", width=80)
        self.items_tree.column("force_bp", width=80)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем таблицу и скроллбар
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_dinos_tab(self, parent):
        """Настройка вкладки динозавров"""
        # Создаем фрейм для списка динозавров и кнопок управления
        frame = tk.Frame(parent, bg=DARK_SECONDARY)
        frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Кнопки управления динозаврами
        buttons_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(0, PADDING_SMALL))
        
        add_button = tk.Button(
            buttons_frame, 
            text="Добавить динозавра", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.add_dino
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        edit_button = tk.Button(
            buttons_frame, 
            text="Изменить динозавра", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.edit_dino
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            buttons_frame, 
            text="Удалить динозавра", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_dino
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем таблицу динозавров
        table_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Определяем колонки таблицы
        columns = ("blueprint", "level", "name", "neutered")
        self.dinos_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настраиваем заголовки
        self.dinos_tree.heading("blueprint", text="Blueprint")
        self.dinos_tree.heading("level", text="Уровень")
        self.dinos_tree.heading("name", text="Имя")
        self.dinos_tree.heading("neutered", text="Стерилизован")
        
        # Настраиваем ширину колонок
        self.dinos_tree.column("blueprint", width=400)
        self.dinos_tree.column("level", width=80)
        self.dinos_tree.column("name", width=150)
        self.dinos_tree.column("neutered", width=100)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.dinos_tree.yview)
        self.dinos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем таблицу и скроллбар
        self.dinos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_commands_tab(self, parent):
        """Настройка вкладки консольных команд"""
        # Создаем фрейм для списка команд и кнопок управления
        frame = tk.Frame(parent, bg=DARK_SECONDARY)
        frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Кнопки управления командами
        buttons_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(0, PADDING_SMALL))
        
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
            text="Изменить команду", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.edit_command
        )
        edit_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            buttons_frame, 
            text="Удалить команду", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_command
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем список команд
        list_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем список и скроллбар
        self.commands_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=10, width=80)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.commands_listbox.yview)
        self.commands_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем список и скроллбар
        self.commands_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_permissions_tab(self, parent):
        """Настройка вкладки разрешений"""
        # Создаем фрейм для списка разрешений и кнопок управления
        frame = tk.Frame(parent, bg=DARK_SECONDARY)
        frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Информационный текст
        info_label = tk.Label(
            frame, 
            text="Добавьте группы разрешений, которые будут иметь доступ к этому набору.",
            bg=DARK_SECONDARY, 
            fg=LIGHT_TEXT,
            justify=tk.LEFT,
            wraplength=700
        )
        info_label.pack(anchor="w", pady=PADDING_SMALL)
        
        # Кнопки управления разрешениями
        buttons_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=(0, PADDING_SMALL))
        
        add_button = tk.Button(
            buttons_frame, 
            text="Добавить группу", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.add_permission
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        delete_button = tk.Button(
            buttons_frame, 
            text="Удалить группу", 
            bg=BUTTON_BG, 
            fg=LIGHT_TEXT,
            command=self.delete_permission
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем список разрешений
        list_frame = tk.Frame(frame, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем список и скроллбар
        self.permissions_listbox = tk.Listbox(list_frame, bg=DARK_BG, fg=LIGHT_TEXT, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.permissions_listbox.yview)
        self.permissions_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем список и скроллбар
        self.permissions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def update_items_list(self):
        """Обновляет список предметов в таблице"""
        # Очищаем текущий список
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Заполняем таблицу предметами
        for item in self.kit_items:
            self.items_tree.insert("", "end", values=(
                item.get("Blueprint", ""),
                item.get("Amount", 1),
                item.get("Quality", 0),
                "Да" if item.get("ForceBlueprint", False) else "Нет"
            ))
    
    def update_dinos_list(self):
        """Обновляет список динозавров в таблице"""
        # Очищаем текущий список
        for item in self.dinos_tree.get_children():
            self.dinos_tree.delete(item)
        
        # Заполняем таблицу динозаврами
        for dino in self.kit_dinos:
            self.dinos_tree.insert("", "end", values=(
                dino.get("Blueprint", ""),
                dino.get("Level", 150),
                dino.get("Name", ""),
                "Да" if dino.get("Neutered", False) else "Нет"
            ))
    
    def update_commands_list(self):
        """Обновляет список консольных команд"""
        # Очищаем текущий список
        self.commands_listbox.delete(0, tk.END)
        
        # Заполняем список командами
        for command in self.kit_commands:
            self.commands_listbox.insert(tk.END, command)
    
    def update_permissions_list(self):
        """Обновляет список групп разрешений"""
        # Очищаем текущий список
        self.permissions_listbox.delete(0, tk.END)
        
        # Заполняем список группами
        for group in self.permission_groups:
            self.permissions_listbox.insert(tk.END, group)
    
    def add_item(self):
        """Открывает диалог для добавления предмета"""
        dialog = AddKitItemDialog(self.dialog, self.items_data, self.on_item_added)
    
    def on_item_added(self, item_data):
        """Обработчик добавления предмета"""
        self.kit_items.append(item_data)
        self.update_items_list()
    
    def edit_item(self):
        """Открывает диалог для редактирования предмета"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите предмет для редактирования")
            return
        
        # Получаем индекс выбранного предмета
        index = self.items_tree.index(selected[0])
        
        # Открываем диалог редактирования
        dialog = AddKitItemDialog(
            self.dialog, 
            self.items_data, 
            lambda data: self.on_item_edited(index, data), 
            self.kit_items[index]
        )
    
    def on_item_edited(self, index, item_data):
        """Обработчик редактирования предмета"""
        self.kit_items[index] = item_data
        self.update_items_list()
    
    def delete_item(self):
        """Удаляет выбранный предмет"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите предмет для удаления")
            return
        
        # Получаем индекс выбранного предмета
        index = self.items_tree.index(selected[0])
        
        # Удаляем предмет
        del self.kit_items[index]
        self.update_items_list()
    
    def add_dino(self):
        """Открывает диалог для добавления динозавра"""
        dialog = AddKitDinoDialog(self.dialog, self.dinos_data, self.on_dino_added)
    
    def on_dino_added(self, dino_data):
        """Обработчик добавления динозавра"""
        self.kit_dinos.append(dino_data)
        self.update_dinos_list()
    
    def edit_dino(self):
        """Открывает диалог для редактирования динозавра"""
        selected = self.dinos_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите динозавра для редактирования")
            return
        
        # Получаем индекс выбранного динозавра
        index = self.dinos_tree.index(selected[0])
        
        # Открываем диалог редактирования
        dialog = AddKitDinoDialog(
            self.dialog, 
            self.dinos_data, 
            lambda data: self.on_dino_edited(index, data), 
            self.kit_dinos[index]
        )
    
    def on_dino_edited(self, index, dino_data):
        """Обработчик редактирования динозавра"""
        self.kit_dinos[index] = dino_data
        self.update_dinos_list()
    
    def delete_dino(self):
        """Удаляет выбранного динозавра"""
        selected = self.dinos_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите динозавра для удаления")
            return
        
        # Получаем индекс выбранного динозавра
        index = self.dinos_tree.index(selected[0])
        
        # Удаляем динозавра
        del self.kit_dinos[index]
        self.update_dinos_list()
    
    def add_command(self):
        """Открывает диалог для добавления консольной команды"""
        dialog = AddKitCommandDialog(self.dialog, self.on_command_added)
    
    def on_command_added(self, command):
        """Обработчик добавления консольной команды"""
        self.kit_commands.append(command)
        self.update_commands_list()
    
    def edit_command(self):
        """Открывает диалог для редактирования консольной команды"""
        selected = self.commands_listbox.curselection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите команду для редактирования")
            return
        
        # Получаем индекс выбранной команды
        index = selected[0]
        
        # Открываем диалог редактирования
        dialog = AddKitCommandDialog(
            self.dialog, 
            lambda data: self.on_command_edited(index, data), 
            self.kit_commands[index]
        )
    
    def on_command_edited(self, index, command):
        """Обработчик редактирования консольной команды"""
        self.kit_commands[index] = command
        self.update_commands_list()
    
    def delete_command(self):
        """Удаляет выбранную консольную команду"""
        selected = self.commands_listbox.curselection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите команду для удаления")
            return
        
        # Получаем индекс выбранной команды
        index = selected[0]
        
        # Удаляем команду
        del self.kit_commands[index]
        self.update_commands_list()
    
    def add_permission(self):
        """Добавляет группу разрешений"""
        group_name = simpledialog.askstring("Добавить группу", "Введите название группы разрешений:")
        if not group_name:
            return
        
        if group_name in self.permission_groups:
            messagebox.showerror("Ошибка", f"Группа '{group_name}' уже добавлена")
            return
        
        self.permission_groups.append(group_name)
        self.update_permissions_list()
    
    def delete_permission(self):
        """Удаляет выбранную группу разрешений"""
        selected = self.permissions_listbox.curselection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите группу для удаления")
            return
        
        # Получаем индекс выбранной группы
        index = selected[0]
        
        # Удаляем группу
        del self.permission_groups[index]
        self.update_permissions_list()
    
    def save_kit(self):
        """Сохраняет набор"""
        # Проверяем ID набора
        if not self.kit_id:
            kit_id = self.id_var.get()
            if not kit_id:
                messagebox.showerror("Ошибка", "ID набора не может быть пустым")
                return
        else:
            kit_id = self.kit_id
        
        # Проверяем название набора
        title = self.title_var.get()
        if not title:
            messagebox.showerror("Ошибка", "Название набора не может быть пустым")
            return
        
        # Проверяем цену набора
        try:
            price = int(self.price_var.get())
            if price < 0:
                messagebox.showerror("Ошибка", "Цена не может быть отрицательной")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть целым числом")
            return
        
        # Проверяем количество по умолчанию
        try:
            default_amount = int(self.default_amount_var.get())
            if default_amount < 1:
                messagebox.showerror("Ошибка", "Количество по умолчанию должно быть не меньше 1")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество по умолчанию должно быть целым числом")
            return
        
        # Проверяем значения лимитов
        try:
            max_purchase_same_time = int(self.max_purchase_same_time_var.get())
            max_purchases_uses = int(self.max_purchases_uses_var.get())
            prevent_usage_after_wipe = int(self.prevent_usage_after_wipe_var.get())
            cooldown_days = int(self.cooldown_days_var.get())
            cooldown_hours = int(self.cooldown_hours_var.get())
            cooldown_minutes = int(self.cooldown_minutes_var.get())
            cooldown_seconds = int(self.cooldown_seconds_var.get())
            
            if max_purchase_same_time < 1:
                messagebox.showerror("Ошибка", "Максимальное количество покупок за раз должно быть не меньше 1")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Все значения лимитов должны быть целыми числами")
            return
        
        # Формируем данные набора
        kit_data = {
            "Title": title,
            "Description": self.description_var.get(),
            "DefaultAmount": default_amount,
            "OnlyFromSpawn": self.only_from_spawn_var.get(),
            "AutoGiveOnSpawn": self.auto_give_on_spawn_var.get(),
            "Price": price,
            "Icon": self.icon_var.get(),
            "Exclude_From_Discount": self.exclude_from_discount_var.get(),
            "Limits": {
                "Max_Purchase_Same_Time_Amount": max_purchase_same_time,
                "Max_Purchases/Uses": max_purchases_uses,
                "Prevent_Usage_After_Wipe_For_Minutes": prevent_usage_after_wipe,
                "Cooldown_Days": cooldown_days,
                "Cooldown_Hours": cooldown_hours,
                "Cooldown_Minutes": cooldown_minutes,
                "Cooldown_Seconds": cooldown_seconds
            },
            "Items": self.kit_items,
            "Dinos": self.kit_dinos,
            "ConsoleCommands": self.kit_commands,
            "PermissionGroupRequired": self.permission_groups
        }
        
        # Возвращаем результат через callback
        self.dialog.destroy()
        if self.on_save:
            self.on_save(kit_id, kit_data)
