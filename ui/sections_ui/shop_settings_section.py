import tkinter as tk
from tkinter import ttk
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class ShopSettingsSection(BaseSection):
    """Класс для отображения настроек раздела ShopSettings"""
    
    def setup_ui(self):
        """Настройка интерфейса для раздела ShopSettings"""
        # Создаем фрейм с вкладками для организации большого количества опций
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Вкладка основных настроек
        basic_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(basic_frame, text="Основные настройки")
        
        # Вкладка для торговли очками
        trading_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(trading_frame, text="Торговля очками")
        
        # Вкладка для UI ссылок
        links_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(links_frame, text="UI ссылки")
        
        # Вкладка для MAGA интеграции
        maga_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(maga_frame, text="MAGA интеграция")
        
        # Вкладка для настроек отображения текста
        listing_frame = tk.Frame(notebook, bg=DARK_SECONDARY)
        notebook.add(listing_frame, text="Отображение текста")
        
        # Заполняем вкладку основных настроек
        self.setup_basic_settings(basic_frame)
        
        # Заполняем вкладку торговли очками
        self.setup_points_trading(trading_frame)
        
        # Заполняем вкладку UI ссылок
        self.setup_ui_links(links_frame)
        
        # Заполняем вкладку MAGA интеграции
        self.setup_maga_integration(maga_frame)
        
        # Заполняем вкладку настроек отображения текста
        self.setup_shop_listing_text(listing_frame)
    
    def setup_basic_settings(self, parent_frame):
        """Настройка основных параметров магазина"""
        row = 0
        
        # Словарь с описаниями для команд
        command_descriptions = {
            "Buy_Command": "Команда для покупки предметов",
            "Sell_Command": "Команда для продажи предметов",
            "Kit_Command": "Команда для использования набора",
            "Kit_Buy_Command": "Команда для покупки набора",
            "Shop_Command": "Команда для открытия магазина",
            "Points_Command": "Команда для просмотра баланса"
        }
        
        # Настройка команд
        commands_label = tk.Label(parent_frame, text="Команды", fg=ORANGE_PRIMARY, 
                                bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        commands_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                          padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        for key, description in command_descriptions.items():
            # Метка для поля
            label = tk.Label(parent_frame, text=key.replace("_", " ") + ":", 
                           fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Поле для ввода команды
            var = tk.StringVar(value=self.config_data.get(key, ""))
            entry = ttk.Entry(parent_frame, textvariable=var, width=20)
            entry.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную и добавляем отслеживание изменений
            self.fields[key] = var
            var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
            
            # Добавляем описание
            desc_label = tk.Label(parent_frame, text=description, 
                                fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
            desc_label.grid(row=row+1, column=0, columnspan=2, sticky="w", 
                          padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_SMALL))
            row += 2
        
        # Добавляем разделитель
        separator = ttk.Separator(parent_frame, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=2, sticky="ew", 
                     padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Другие базовые настройки
        other_settings_label = tk.Label(parent_frame, text="Другие настройки", fg=ORANGE_PRIMARY, 
                                      bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        other_settings_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                                padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Чекбоксы для различных опций
        checkbox_options = [
            ("Shop_Command_Opens_UI", "Команда магазина открывает UI", 
             "При вызове команды магазина открывается графический интерфейс"),
            ("Use_Hexagons_As_Currency", "Использовать гексагоны как валюту", 
             "Использовать гексагоны вместо очков"),
            ("Use_F2_To_Open_UI", "Использовать F2 для открытия UI", 
             "Открывать интерфейс магазина клавишей F2"),
            ("Enable_Hud_Icon", "Включить иконку на экране", 
             "Отображать иконку магазина на HUD"),
            ("Send_UI_Data_In_Multiple_Chunks", "Отправлять данные UI частями", 
             "Разделять отправку данных интерфейса на несколько пакетов")
        ]
        
        for key, label_text, tooltip in checkbox_options:
            var = tk.BooleanVar(value=self.config_data.get(key, False))
            checkbox = ttk.Checkbutton(parent_frame, text=label_text, variable=var)
            checkbox.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную и добавляем отслеживание изменений
            self.fields[key] = var
            var.trace_add("write", lambda *args, k=key, v=var: self.on_field_change(k, v))
            
            # Добавляем описание
            desc_label = tk.Label(parent_frame, text=tooltip, 
                                fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
            desc_label.grid(row=row+1, column=0, columnspan=2, sticky="w", 
                          padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_SMALL))
            row += 2
        
        # Название магазина
        shop_name_label = tk.Label(parent_frame, text="Название магазина:", 
                                 fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        shop_name_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        shop_name_var = tk.StringVar(value=self.config_data.get("Shop_Name", ""))
        shop_name_entry = ttk.Entry(parent_frame, textvariable=shop_name_var, width=25)
        shop_name_entry.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Сохраняем переменную и добавляем отслеживание изменений
        self.fields["Shop_Name"] = shop_name_var
        shop_name_var.trace_add("write", lambda *args: self.on_field_change("Shop_Name", shop_name_var))
        row += 1
        
        # Путь к крио-поду
        cryopod_label = tk.Label(parent_frame, text="Путь к крио-поду:", 
                               fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        cryopod_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        cryopod_var = tk.StringVar(value=self.config_data.get("Custom_Cryopod_Blueprint_Path", ""))
        cryopod_entry = ttk.Entry(parent_frame, textvariable=cryopod_var, width=40)
        cryopod_entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Сохраняем переменную и добавляем отслеживание изменений
        self.fields["Custom_Cryopod_Blueprint_Path"] = cryopod_var
        cryopod_var.trace_add("write", lambda *args: 
                            self.on_field_change("Custom_Cryopod_Blueprint_Path", cryopod_var))
        row += 1
        
        # Описание для пути крио-пода
        cryopod_desc = tk.Label(parent_frame, text="Пользовательский путь к чертежу крио-пода", 
                              fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
        cryopod_desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_SMALL))
        
        # Настройка весов для правильного растяжения
        parent_frame.grid_columnconfigure(1, weight=1)
    
    def setup_points_trading(self, parent_frame):
        """Настройка торговли очками"""
        row = 0
        
        # Заголовок
        header_label = tk.Label(parent_frame, text="Настройки торговли очками", 
                              fg=ORANGE_PRIMARY, bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        header_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Получаем данные торговли
        trading_data = self.config_data.get("Points_Trading", {})
        
        # Чекбокс включения торговли
        enable_trading_var = tk.BooleanVar(value=trading_data.get("Enable_Points_Trading", False))
        enable_trading_check = ttk.Checkbutton(
            parent_frame, 
            text="Включить торговлю очками", 
            variable=enable_trading_var
        )
        enable_trading_check.grid(row=row, column=0, columnspan=2, sticky="w", 
                                padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Сохраняем состояние в переменную trading_enable_var
        self.trading_enable_var = enable_trading_var
        enable_trading_var.trace_add("write", lambda *args: self.update_trading_settings())
        row += 1
        
        # Описание
        enable_desc = tk.Label(parent_frame, text="Позволяет игрокам обмениваться очками между собой", 
                             fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
        enable_desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                       padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
        row += 1
        
        # Чекбокс только для своей команды
        same_team_var = tk.BooleanVar(value=trading_data.get("Allow_Only_Same_Team", False))
        same_team_check = ttk.Checkbutton(
            parent_frame, 
            text="Разрешить торговлю только внутри команды", 
            variable=same_team_var
        )
        same_team_check.grid(row=row, column=0, columnspan=2, sticky="w", 
                           padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Сохраняем переменную
        self.trading_same_team_var = same_team_var
        same_team_var.trace_add("write", lambda *args: self.update_trading_settings())
        row += 1
        
        # Описание
        same_team_desc = tk.Label(parent_frame, 
                                text="Игроки смогут торговать только с членами своей команды", 
                                fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
        same_team_desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                          padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
        row += 1
        
        # Команда торговли
        trade_cmd_label = tk.Label(parent_frame, text="Команда торговли:", 
                                 fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        trade_cmd_label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        trade_cmd_var = tk.StringVar(value=trading_data.get("Trade_Command", "/trade"))
        trade_cmd_entry = ttk.Entry(parent_frame, textvariable=trade_cmd_var, width=20)
        trade_cmd_entry.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Сохраняем переменную
        self.trading_command_var = trade_cmd_var
        trade_cmd_var.trace_add("write", lambda *args: self.update_trading_settings())
        row += 1
        
        # Описание команды
        trade_cmd_desc = tk.Label(parent_frame, 
                                text="Команда для обмена очками между игроками", 
                                fg=GRAY_TEXT, bg=DARK_SECONDARY, font=FONT_SMALL)
        trade_cmd_desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                          padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
        
        # Настройка весов для правильного растяжения
        parent_frame.grid_columnconfigure(1, weight=1)
    
    def update_trading_settings(self):
        """Обновляет настройки торговли в конфигурации"""
        if "Points_Trading" not in self.config_data:
            self.config_data["Points_Trading"] = {}
        
        # Обновляем настройки из переменных
        self.config_data["Points_Trading"]["Enable_Points_Trading"] = self.trading_enable_var.get()
        self.config_data["Points_Trading"]["Allow_Only_Same_Team"] = self.trading_same_team_var.get()
        self.config_data["Points_Trading"]["Trade_Command"] = self.trading_command_var.get()
        
        # Уведомляем об изменении
        self.on_field_change("Points_Trading", self.config_data["Points_Trading"])
    
    def setup_ui_links(self, parent_frame):
        """Настройка UI ссылок"""
        row = 0
        
        # Заголовок
        header_label = tk.Label(parent_frame, text="Настройка ссылок в интерфейсе", 
                              fg=ORANGE_PRIMARY, bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        header_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Описание
        desc_label = tk.Label(parent_frame, 
                            text="Укажите ссылки, которые будут доступны через интерфейс магазина", 
                            fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        desc_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                      padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
        row += 1
        
        # Получаем данные ссылок
        links_data = self.config_data.get("UI_Links", {})
        
        # Список ссылок с описаниями
        links = [
            ("Discord_Join_Link", "Ссылка на Discord:", 
             "URL для присоединения к серверу Discord"),
            ("Server_Rules_Link", "Ссылка на правила сервера:", 
             "URL с правилами сервера"),
            ("Donation_Shop_Link", "Ссылка на магазин донатов:", 
             "URL для покупки донатов")
        ]
        
        # Создаем поля для каждой ссылки
        self.ui_links_vars = {}
        for key, label_text, tooltip in links:
            # Метка для поля
            label = tk.Label(parent_frame, text=label_text, fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Поле для ввода ссылки
            var = tk.StringVar(value=links_data.get(key, ""))
            entry = ttk.Entry(parent_frame, textvariable=var, width=50)
            entry.grid(row=row, column=1, sticky="ew", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.ui_links_vars[key] = var
            var.trace_add("write", lambda *args: self.update_ui_links())
            row += 1
            
            # Добавляем описание
            desc = tk.Label(parent_frame, text=tooltip, fg=GRAY_TEXT, 
                          bg=DARK_SECONDARY, font=FONT_SMALL)
            desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                    padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
            row += 1
        
        # Настройка весов для правильного растяжения
        parent_frame.grid_columnconfigure(1, weight=1)
    
    def update_ui_links(self):
        """Обновляет ссылки UI в конфигурации"""
        if "UI_Links" not in self.config_data:
            self.config_data["UI_Links"] = {}
        
        # Обновляем ссылки из переменных
        for key, var in self.ui_links_vars.items():
            self.config_data["UI_Links"][key] = var.get()
        
        # Уведомляем об изменении
        self.on_field_change("UI_Links", self.config_data["UI_Links"])
    
    def setup_maga_integration(self, parent_frame):
        """Настройка интеграции с MAGA плагином"""
        row = 0
        
        # Заголовок
        header_label = tk.Label(parent_frame, text="Интеграция с MAGA плагином", 
                              fg=ORANGE_PRIMARY, bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        header_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Описание
        desc_label = tk.Label(parent_frame, 
                            text="Настройки для интеграции с плагином MAGA (Make ARK Great Again)", 
                            fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        desc_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                      padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
        row += 1
        
        # Получаем данные MAGA интеграции
        maga_data = self.config_data.get("MAGA_Integration", {})
        
        # Чекбоксы для MAGA интеграции
        maga_options = [
            ("Use_Maga_Plugin", "Использовать MAGA плагин", 
             "Включить интеграцию с плагином Make ARK Great Again"),
            ("Block_Buy_On_Pvp_Cooldown", "Блокировать покупки при PVP откате", 
             "Запрещает покупки, когда игрок находится на откате PVP"),
            ("Block_Kits_On_Pvp_Cooldown", "Блокировать киты при PVP откате", 
             "Запрещает использование китов, когда игрок находится на откате PVP")
        ]
        
        # Создаем чекбоксы для каждой опции
        self.maga_vars = {}
        for key, label_text, tooltip in maga_options:
            var = tk.BooleanVar(value=maga_data.get(key, False))
            check = ttk.Checkbutton(parent_frame, text=label_text, variable=var)
            check.grid(row=row, column=0, columnspan=2, sticky="w", 
                     padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.maga_vars[key] = var
            var.trace_add("write", lambda *args: self.update_maga_settings())
            row += 1
            
            # Добавляем описание
            desc = tk.Label(parent_frame, text=tooltip, fg=GRAY_TEXT, 
                          bg=DARK_SECONDARY, font=FONT_SMALL)
            desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                    padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
            row += 1
    
    def update_maga_settings(self):
        """Обновляет настройки MAGA интеграции в конфигурации"""
        if "MAGA_Integration" not in self.config_data:
            self.config_data["MAGA_Integration"] = {}
        
        # Обновляем настройки из переменных
        for key, var in self.maga_vars.items():
            self.config_data["MAGA_Integration"][key] = var.get()
        
        # Уведомляем об изменении
        self.on_field_change("MAGA_Integration", self.config_data["MAGA_Integration"])
    
    def setup_shop_listing_text(self, parent_frame):
        """Настройка отображения текста в магазине"""
        row = 0
        
        # Заголовок
        header_label = tk.Label(parent_frame, text="Настройки отображения текста", 
                              fg=ORANGE_PRIMARY, bg=DARK_SECONDARY, font=FONT_SUBHEADER)
        header_label.grid(row=row, column=0, columnspan=2, sticky="w", 
                        padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Получаем данные форматов текста
        text_data = self.config_data.get("Shop_Listing_Text", {})
        
        # Числовые настройки
        numeric_settings = [
            ("Items_Per_Page", "Предметов на страницу:", 
             "Количество предметов, отображаемых на одной странице"),
            ("Display_Time", "Время отображения (сек):", 
             "Как долго отображать список в секундах"),
            ("Text_Size", "Размер текста:", 
             "Размер текста в списке")
        ]
        
        # Создаем поля для числовых настроек
        self.listing_numeric_vars = {}
        for key, label_text, tooltip in numeric_settings:
            # Метка для поля
            label = tk.Label(parent_frame, text=label_text, fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Поле для ввода значения
            var = tk.StringVar(value=str(text_data.get(key, "")))
            entry = ttk.Entry(parent_frame, textvariable=var, width=10)
            entry.grid(row=row, column=1, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.listing_numeric_vars[key] = var
            var.trace_add("write", lambda *args: self.update_listing_settings())
            row += 1
            
            # Добавляем описание
            desc = tk.Label(parent_frame, text=tooltip, fg=GRAY_TEXT, 
                          bg=DARK_SECONDARY, font=FONT_SMALL)
            desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                    padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
            row += 1
        
        # Разделитель
        separator = ttk.Separator(parent_frame, orient="horizontal")
        separator.grid(row=row, column=0, columnspan=2, sticky="ew", 
                     padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        row += 1
        
        # Форматы текста
        text_formats = [
            ("Each_Shop_Line_Format", "Формат строки предмета:", 
             "{0} - номер, {1} - название, {2} - ID, {3} - цена"),
            ("Usage_Explanation", "Пояснение по использованию:", 
             "Текст с пояснением, как использовать команду покупки"),
            ("Kits_Heading", "Заголовок раздела китов:", 
             "Текст заголовка для раздела с наборами"),
            ("Each_Kit_Line_Format", "Формат строки кита:", 
             "{0} - имя кита, {1} - описание, {2} - оставшееся количество, {3} - цена"),
            ("Kits_Usage_Explanation", "Пояснение по использованию китов:", 
             "Текст с пояснением, как использовать команду китов")
        ]
        
        # Создаем поля для форматов текста
        self.listing_text_vars = {}
        for key, label_text, tooltip in text_formats:
            # Метка для поля
            label = tk.Label(parent_frame, text=label_text, fg=LIGHT_TEXT, bg=DARK_SECONDARY)
            label.grid(row=row, column=0, sticky="w", padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            row += 1
            
            # Поле для ввода текста (на новой строке, чтобы было больше места)
            var = tk.StringVar(value=str(text_data.get(key, "")))
            entry = ttk.Entry(parent_frame, textvariable=var, width=60)
            entry.grid(row=row, column=0, columnspan=2, sticky="ew", 
                     padx=PADDING_MEDIUM, pady=PADDING_SMALL)
            
            # Сохраняем переменную
            self.listing_text_vars[key] = var
            var.trace_add("write", lambda *args: self.update_listing_settings())
            row += 1
            
            # Добавляем описание
            desc = tk.Label(parent_frame, text=tooltip, fg=GRAY_TEXT, 
                          bg=DARK_SECONDARY, font=FONT_SMALL)
            desc.grid(row=row, column=0, columnspan=2, sticky="w", 
                    padx=(PADDING_LARGE, PADDING_MEDIUM), pady=(0, PADDING_MEDIUM))
            row += 1
        
        # Настройка весов для правильного растяжения
        parent_frame.grid_columnconfigure(1, weight=1)
    
    def update_listing_settings(self):
        """Обновляет настройки отображения текста в конфигурации"""
        if "Shop_Listing_Text" not in self.config_data:
            self.config_data["Shop_Listing_Text"] = {}
        
        # Обновляем числовые настройки
        for key, var in self.listing_numeric_vars.items():
            try:
                # Преобразуем строку в нужный тип данных
                if key == "Text_Size":
                    self.config_data["Shop_Listing_Text"][key] = float(var.get())
                else:
                    self.config_data["Shop_Listing_Text"][key] = int(var.get())
            except ValueError:
                # В случае ошибки преобразования сохраняем значение как строку
                self.config_data["Shop_Listing_Text"][key] = var.get()
        
        # Обновляем форматы текста
        for key, var in self.listing_text_vars.items():
            self.config_data["Shop_Listing_Text"][key] = var.get()
        
        # Уведомляем об изменении
        self.on_field_change("Shop_Listing_Text", self.config_data["Shop_Listing_Text"])
    
    def collect_field_data(self):
        """Собирает данные из полей ввода"""
        # Базовые поля уже обработаны в методах update_*
        # Создаем копию текущих данных, чтобы не потерять структуру
        return self.config_data.copy()
