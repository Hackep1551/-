import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class ShopUISection(BaseSection):
    """Класс для отображения настроек интерфейса магазина"""
    
    def setup_ui(self):
        """Настройка интерфейса для секции ShopUI"""
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
        
        # Настройка основных опций магазина
        self.setup_main_options(scrollable_frame)
        
        # Настройка категорий
        categories_frame = tk.LabelFrame(scrollable_frame, text="Категории", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=(PADDING_MEDIUM, 0))
        
        self.setup_categories(categories_frame)
        
        # Настройка переводимых текстов интерфейса
        translation_frame = tk.LabelFrame(scrollable_frame, text="Перевод интерфейса", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        translation_frame.pack(fill=tk.BOTH, expand=True, pady=(PADDING_MEDIUM, 0))
        
        self.setup_translations(translation_frame)
    
    def setup_main_options(self, parent):
        """Настройка основных опций интерфейса магазина"""
        options_frame = tk.LabelFrame(parent, text="Основные настройки", bg=DARK_SECONDARY, fg=LIGHT_TEXT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        options_frame.pack(fill=tk.BOTH, pady=(0, PADDING_MEDIUM))
        
        # Опция использования пользовательских категорий
        use_custom_categories_var = tk.BooleanVar(value=self.config_data.get("Use_Custom_Categories", False))
        use_custom_categories_cb = ttk.Checkbutton(
            options_frame, 
            text="Использовать пользовательские категории",
            variable=use_custom_categories_var
        )
        use_custom_categories_cb.grid(row=0, column=0, sticky="w", pady=PADDING_SMALL)
        use_custom_categories_var.trace_add("write", lambda *args: self.on_field_change("Use_Custom_Categories", use_custom_categories_var.get()))
        
        # Поле для настройки иконки бафа HUD
        custom_buff_label = tk.Label(options_frame, text="Путь к иконке Buff HUD:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        custom_buff_label.grid(row=1, column=0, sticky="w", pady=PADDING_SMALL)
        
        custom_buff_var = tk.StringVar(value=self.config_data.get("Custom_Buff_HUD_Icon", ""))
        custom_buff_entry = ttk.Entry(options_frame, textvariable=custom_buff_var, width=50)
        custom_buff_entry.grid(row=1, column=1, sticky="w", pady=PADDING_SMALL)
        custom_buff_var.trace_add("write", lambda *args: self.on_field_change("Custom_Buff_HUD_Icon", custom_buff_var.get()))
        
        # Поле для настройки логотипа
        custom_logo_label = tk.Label(options_frame, text="Путь к логотипу:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        custom_logo_label.grid(row=2, column=0, sticky="w", pady=PADDING_SMALL)
        
        custom_logo_var = tk.StringVar(value=self.config_data.get("Custom_Top_Logo_Path", ""))
        custom_logo_entry = ttk.Entry(options_frame, textvariable=custom_logo_var, width=50)
        custom_logo_entry.grid(row=2, column=1, sticky="w", pady=PADDING_SMALL)
        custom_logo_var.trace_add("write", lambda *args: self.on_field_change("Custom_Top_Logo_Path", custom_logo_var.get()))
        
        # Поле для настройки водяного знака
        watermark_label = tk.Label(options_frame, text="Путь к водяному знаку:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        watermark_label.grid(row=3, column=0, sticky="w", pady=PADDING_SMALL)
        
        watermark_var = tk.StringVar(value=self.config_data.get("Custom_Bottom_Left_WaterMark", ""))
        watermark_entry = ttk.Entry(options_frame, textvariable=watermark_var, width=50)
        watermark_entry.grid(row=3, column=1, sticky="w", pady=PADDING_SMALL)
        watermark_var.trace_add("write", lambda *args: self.on_field_change("Custom_Bottom_Left_WaterMark", watermark_var.get()))
        
        # Поле для настройки прозрачности водяного знака
        watermark_alpha_label = tk.Label(options_frame, text="Прозрачность водяного знака:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        watermark_alpha_label.grid(row=4, column=0, sticky="w", pady=PADDING_SMALL)
        
        watermark_alpha_var = tk.StringVar(value=str(self.config_data.get("Custom_Bottom_Left_WaterMark_Alpha", 1)))
        watermark_alpha_entry = ttk.Entry(options_frame, textvariable=watermark_alpha_var, width=10)
        watermark_alpha_entry.grid(row=4, column=1, sticky="w", pady=PADDING_SMALL)
        watermark_alpha_var.trace_add("write", lambda *args: self.update_watermark_alpha(watermark_alpha_var))
        
    def update_watermark_alpha(self, var):
        """Обновляет значение прозрачности водяного знака"""
        try:
            value = float(var.get())
            if 0.0 <= value <= 1.0:
                self.on_field_change("Custom_Bottom_Left_WaterMark_Alpha", value)
        except ValueError:
            pass
            
    def setup_categories(self, parent):
        """Настройка категорий магазина"""
        # Рамка с кнопками для управления категориями
        control_frame = tk.Frame(parent, bg=DARK_SECONDARY)
        control_frame.pack(fill=tk.X, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Кнопка добавления категории
        add_button = tk.Button(
            control_frame,
            text="Добавить категорию",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.add_category
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Кнопка удаления категории
        delete_button = tk.Button(
            control_frame,
            text="Удалить категорию",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.delete_category
        )
        delete_button.pack(side=tk.LEFT)
        
        # Создаем фрейм для списка категорий
        list_frame = tk.Frame(parent, bg=DARK_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Создаем скроллбар
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаем список категорий
        self.categories_listbox = tk.Listbox(
            list_frame, 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            selectbackground=ORANGE_PRIMARY,
            selectforeground=LIGHT_TEXT,
            height=10,
            yscrollcommand=scrollbar.set
        )
        self.categories_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Привязываем скроллбар к списку
        scrollbar.config(command=self.categories_listbox.yview)
        
        # Заполняем список категорий
        self.update_categories_list()
        
        # Привязываем двойной клик для редактирования
        self.categories_listbox.bind("<Double-1>", lambda e: self.edit_category())

    def update_categories_list(self):
        """Обновляет список категорий"""
        # Очищаем список
        self.categories_listbox.delete(0, tk.END)
        
        # Если в конфигурации нет категорий, создаем пустой словарь
        if "Categories" not in self.config_data or not self.config_data["Categories"]:
            self.config_data["Categories"] = {}
            
        # Заполняем список категорий
        for category_name, category_data in self.config_data["Categories"].items():
            # Убедимся, что category_data - словарь
            if isinstance(category_data, dict):
                category_id = category_data.get("ID", 0)
                self.categories_listbox.insert(tk.END, f"{category_name} (ID: {category_id})")
            else:
                # Если мы получили целое число вместо словаря, преобразуем его в словарь
                self.config_data["Categories"][category_name] = {"ID": category_data}
                self.categories_listbox.insert(tk.END, f"{category_name} (ID: {category_data})")
        
    def add_category(self):
        """Добавляет новую категорию"""
        # Создаем диалоговое окно для ввода имени категории
        category_name = simpledialog.askstring("Новая категория", "Введите название категории:")
        
        if not category_name:  # Если пользователь нажал Отмена или не ввел имя
            return
            
        # Проверяем, существует ли уже такая категория
        if category_name in self.config_data["Categories"]:
            messagebox.showerror("Ошибка", f"Категория '{category_name}' уже существует.")
            return
            
        # Определяем ID для новой категории
        max_id = 0
        for _, category_data in self.config_data["Categories"].items():
            if isinstance(category_data, dict) and "ID" in category_data:
                max_id = max(max_id, category_data["ID"])
            elif isinstance(category_data, int):
                max_id = max(max_id, category_data)
                
        new_id = max_id + 1
        
        # Создаем новую категорию
        self.config_data["Categories"][category_name] = {"ID": new_id}
        
        # Обновляем конфигурацию
        self.on_field_change("Categories", self.config_data["Categories"])
        
        # Обновляем список категорий
        self.update_categories_list()
        
    def edit_category(self):
        """Редактирует выбранную категорию"""
        # Получаем выбранную категорию
        selection = self.categories_listbox.curselection()
        if not selection:  # Если ничего не выбрано
            messagebox.showinfo("Информация", "Выберите категорию для редактирования.")
            return
            
        # Получаем информацию о выбранной категории
        item_text = self.categories_listbox.get(selection[0])
        category_name = item_text.split(" (ID: ")[0]  # Извлекаем имя категории
        
        # Создаем диалоговое окно для редактирования
        new_name = simpledialog.askstring("Редактирование категории", "Введите новое название категории:", initialvalue=category_name)
        
        if not new_name:  # Если пользователь нажал Отмена или не ввел имя
            return
            
        # Проверяем, существует ли уже такая категория
        if new_name != category_name and new_name in self.config_data["Categories"]:
            messagebox.showerror("Ошибка", f"Категория '{new_name}' уже существует.")
            return
            
        # Получаем ID категории
        category_data = self.config_data["Categories"][category_name]
        if isinstance(category_data, dict):
            category_id = category_data.get("ID", 0)
        else:
            category_id = category_data
            
        # Удаляем старую категорию и создаем новую
        del self.config_data["Categories"][category_name]
        self.config_data["Categories"][new_name] = {"ID": category_id}
        
        # Обновляем конфигурацию
        self.on_field_change("Categories", self.config_data["Categories"])
        
        # Обновляем список категорий
        self.update_categories_list()
        
    def delete_category(self):
        """Удаляет выбранную категорию"""
        # Получаем выбранную категорию
        selection = self.categories_listbox.curselection()
        if not selection:  # Если ничего не выбрано
            messagebox.showinfo("Информация", "Выберите категорию для удаления.")
            return
            
        # Получаем информацию о выбранной категории
        item_text = self.categories_listbox.get(selection[0])
        category_name = item_text.split(" (ID: ")[0]  # Извлекаем имя категории
        
        # Запрашиваем подтверждение удаления
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить категорию '{category_name}'?"):
            return
            
        # Удаляем категорию
        del self.config_data["Categories"][category_name]
        
        # Обновляем конфигурацию
        self.on_field_change("Categories", self.config_data["Categories"])
        
        # Обновляем список категорий
        self.update_categories_list()
            
    def setup_translations(self, parent):
        """Настройка переводов интерфейса"""
        translations_data = self.config_data.get("Translatable_UI_Text", {})
        
        # Опция использования перевода
        use_translation_var = tk.BooleanVar(value=translations_data.get("Use_Translation", False))
        use_translation_cb = ttk.Checkbutton(
            parent, 
            text="Использовать перевод интерфейса",
            variable=use_translation_var
        )
        use_translation_cb.grid(row=0, column=0, sticky="w", pady=PADDING_SMALL, columnspan=2)
        use_translation_var.trace_add("write", lambda *args: self.update_translation_option("Use_Translation", use_translation_var.get()))
        
        # Заголовки столбцов
        tk.Label(parent, text="Элемент интерфейса", bg=DARK_SECONDARY, fg=LIGHT_TEXT, font=FONT_SUBHEADER).grid(row=1, column=0, sticky="w", pady=PADDING_SMALL)
        tk.Label(parent, text="Перевод", bg=DARK_SECONDARY, fg=LIGHT_TEXT, font=FONT_SUBHEADER).grid(row=1, column=1, sticky="w", pady=PADDING_SMALL)
        
        # Список элементов интерфейса для перевода
        ui_elements = {
            "Shop_Items": "Товары",
            "Kits": "Наборы",
            "Shop_Sell": "Продажа",
            "Join_Discord": "Discord",
            "Server_Rules": "Правила",
            "Donate": "Донат",
            "Close": "Закрыть",
            "Buy_multiple": "Купить несколько",
            "Points": "Очки:",
            "Buy_More_Kits": "Купить наборы"
        }
        
        # Создаем поля для перевода каждого элемента
        row = 2
        self.translation_vars = {}
        
        for key, default_text in ui_elements.items():
            # Метка с названием элемента
            tk.Label(parent, text=key, bg=DARK_SECONDARY, fg=LIGHT_TEXT).grid(row=row, column=0, sticky="w", pady=PADDING_SMALL)
            
            # Поле для ввода перевода
            var = tk.StringVar(value=translations_data.get(key, default_text))
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=row, column=1, sticky="w", pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.translation_vars[key] = var
            
            # Привязываем обработчик изменений
            var.trace_add("write", lambda *args, k=key, v=var: self.update_translation(k, v))
            
            row += 1
            
    def update_translation_option(self, key, value):
        """Обновляет опцию перевода"""
        if "Translatable_UI_Text" not in self.config_data:
            self.config_data["Translatable_UI_Text"] = {}
            
        self.config_data["Translatable_UI_Text"][key] = value
        self.on_field_change("Translatable_UI_Text", self.config_data["Translatable_UI_Text"])
        
    def update_translation(self, key, var):
        """Обновляет перевод элемента интерфейса"""
        if "Translatable_UI_Text" not in self.config_data:
            self.config_data["Translatable_UI_Text"] = {}
            
        self.config_data["Translatable_UI_Text"][key] = var.get()
        self.on_field_change("Translatable_UI_Text", self.config_data["Translatable_UI_Text"])
    
    def collect_field_data(self):
        """Собирает данные из полей ввода"""
        updated_data = {}
        
        # Копируем базовую структуру
        for key in self.config_data:
            if key not in ["Categories", "Translatable_UI_Text"]:
                if key in self.fields:
                    var = self.fields[key]
                    if isinstance(var, tk.BooleanVar):
                        updated_data[key] = var.get()
                    elif isinstance(var, tk.StringVar):
                        if key == "Custom_Bottom_Left_WaterMark_Alpha":
                            try:
                                updated_data[key] = float(var.get())
                            except ValueError:
                                updated_data[key] = 1.0
                        else:
                            updated_data[key] = var.get()
                    else:
                        updated_data[key] = self.config_data[key]
                else:
                    updated_data[key] = self.config_data[key]
        
        # Добавляем категории (они обновляются напрямую в self.config_data)
        updated_data["Categories"] = self.config_data.get("Categories", {})
        
        # Добавляем переводы (они обновляются напрямую в self.config_data)
        updated_data["Translatable_UI_Text"] = self.config_data.get("Translatable_UI_Text", {})
        
        return updated_data
