import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *
from ui.sections_ui.base_section import BaseSection

class TimedPointsSection(BaseSection):
    """Класс для отображения настроек TimedPoints"""
    
    def setup_ui(self):
        """Настройка интерфейса для TimedPointsSection"""
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Заголовок
        header = tk.Label(main_frame, text="Настройки Timed Points", 
                       font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Создаем верхнюю панель с основными настройками
        settings_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        settings_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Включить/выключить Timed Points
        enable_var = tk.BooleanVar(value=self.config_data.get("Enable_Timed_Points", False))
        enable_checkbox = ttk.Checkbutton(
            settings_frame, 
            text="Включить начисление очков за время", 
            variable=enable_var
        )
        enable_checkbox.grid(row=0, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.fields["Enable_Timed_Points"] = enable_var
        enable_var.trace_add("write", lambda *args: self.on_field_change("Enable_Timed_Points", enable_var.get()))
        
        # Интервал в минутах
        interval_label = tk.Label(settings_frame, text="Интервал (мин):", fg=LIGHT_TEXT, bg=DARK_SECONDARY)
        interval_label.grid(row=1, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        interval_var = tk.StringVar(value=str(self.config_data.get("Interval_Minutes", 15)))
        interval_entry = ttk.Entry(settings_frame, textvariable=interval_var, width=10)
        interval_entry.grid(row=1, column=1, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.fields["Interval_Minutes"] = interval_var
        interval_var.trace_add("write", lambda *args: self.update_interval())
        
        # Накопление групп
        groups_stack_var = tk.BooleanVar(value=self.config_data.get("Groups_Stack", False))
        groups_stack_checkbox = ttk.Checkbutton(
            settings_frame, 
            text="Накапливать бонусы группы", 
            variable=groups_stack_var
        )
        groups_stack_checkbox.grid(row=2, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.fields["Groups_Stack"] = groups_stack_var
        groups_stack_var.trace_add("write", lambda *args: self.on_field_change("Groups_Stack", groups_stack_var.get()))
        
        # Разделитель
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Создаем фрейм для групп очков
        groups_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        groups_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING_SMALL)
        
        # Заголовок для групп
        groups_header = tk.Label(groups_frame, text="Группы и начисляемые очки", 
                               font=FONT_SUBHEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        groups_header.pack(pady=(0, PADDING_MEDIUM), anchor="w")
        
        # Создаем таблицу для групп
        table_frame = tk.Frame(groups_frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем скроллбар для таблицы
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаем таблицу с колонками
        self.groups_tree = ttk.Treeview(
            table_frame,
            columns=("group", "points"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Настраиваем заголовки колонок
        self.groups_tree.heading("group", text="Группа")
        self.groups_tree.heading("points", text="Очки")
        
        # Настраиваем ширину колонок
        self.groups_tree.column("group", width=200)
        self.groups_tree.column("points", width=100)
        
        # Размещаем таблицу
        self.groups_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.groups_tree.yview)
        
        # Загружаем существующие группы в таблицу
        self.load_groups()
        
        # Создаем фрейм с кнопками для управления группами
        buttons_frame = tk.Frame(groups_frame, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Кнопка добавления группы
        add_button = tk.Button(
            buttons_frame, 
            text="Добавить группу", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.add_group
        )
        add_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Кнопка удаления группы
        remove_button = tk.Button(
            buttons_frame, 
            text="Удалить группу", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=self.remove_group
        )
        remove_button.pack(side=tk.LEFT)
        
        # Связываем двойной клик по группе с функцией редактирования
        self.groups_tree.bind("<Double-1>", lambda e: self.edit_group())
    
    def load_groups(self):
        """Загружает группы из конфигурации в таблицу"""
        # Очищаем таблицу
        for item in self.groups_tree.get_children():
            self.groups_tree.delete(item)
        
        # Получаем группы из конфигурации
        groups = self.config_data.get("Groups", {})
        
        # Добавляем группы в таблицу
        for group_name, points in groups.items():
            self.groups_tree.insert("", "end", values=(group_name, points))
    
    def add_group(self):
        """Открывает диалог для добавления новой группы"""
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.parent)
        dialog.title("Добавить группу")
        dialog.geometry("300x150")
        dialog.configure(bg=DARK_SECONDARY)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Название группы
        group_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        group_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        group_label = tk.Label(group_frame, text="Название группы:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        group_label.pack(side=tk.LEFT)
        
        group_var = tk.StringVar()
        group_entry = ttk.Entry(group_frame, textvariable=group_var, width=20)
        group_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0), fill=tk.X, expand=True)
        
        # Очки
        points_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        points_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        points_label = tk.Label(points_frame, text="Очки:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        points_label.pack(side=tk.LEFT)
        
        points_var = tk.StringVar(value="10")
        points_entry = ttk.Entry(points_frame, textvariable=points_var, width=10)
        points_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        cancel_button = tk.Button(
            buttons_frame, 
            text="Отмена", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(PADDING_SMALL, 0))
        
        save_button = tk.Button(
            buttons_frame, 
            text="Сохранить", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=lambda: self.save_group(group_var.get(), points_var.get(), dialog)
        )
        save_button.pack(side=tk.RIGHT)
    
    def save_group(self, group_name, points_str, dialog):
        """Сохраняет новую группу в конфигурацию"""
        if not group_name:
            messagebox.showerror("Ошибка", "Название группы не может быть пустым")
            return
        
        try:
            points = int(points_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Очки должны быть целым числом")
            return
        
        # Получаем текущие группы или создаем пустой словарь
        groups = self.config_data.get("Groups", {})
        
        # Добавляем или обновляем группу
        groups[group_name] = points
        
        # Обновляем конфигурацию
        self.on_field_change("Groups", groups)
        
        # Обновляем таблицу
        self.load_groups()
        
        # Закрываем диалог
        dialog.destroy()
    
    def edit_group(self):
        """Редактирует выбранную группу"""
        # Получаем выбранный элемент
        selection = self.groups_tree.selection()
        if not selection:
            messagebox.showinfo("Информация", "Выберите группу для редактирования")
            return
        
        # Получаем данные выбранной группы
        item = self.groups_tree.item(selection[0])
        group_name, points = item["values"]
        
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.parent)
        dialog.title("Редактировать группу")
        dialog.geometry("300x150")
        dialog.configure(bg=DARK_SECONDARY)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Название группы (только для отображения)
        group_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        group_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        group_label = tk.Label(group_frame, text="Группа:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        group_label.pack(side=tk.LEFT)
        
        group_display = tk.Label(group_frame, text=group_name, bg=DARK_SECONDARY, fg=ORANGE_PRIMARY)
        group_display.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Очки
        points_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        points_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        points_label = tk.Label(points_frame, text="Очки:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        points_label.pack(side=tk.LEFT)
        
        points_var = tk.StringVar(value=str(points))
        points_entry = ttk.Entry(points_frame, textvariable=points_var, width=10)
        points_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Кнопки
        buttons_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        cancel_button = tk.Button(
            buttons_frame, 
            text="Отмена", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=(PADDING_SMALL, 0))
        
        save_button = tk.Button(
            buttons_frame, 
            text="Сохранить", 
            bg=DARK_BG, 
            fg=LIGHT_TEXT,
            command=lambda: self.update_group(group_name, points_var.get(), dialog)
        )
        save_button.pack(side=tk.RIGHT)
    
    def update_group(self, group_name, points_str, dialog):
        """Обновляет данные группы"""
        try:
            points = int(points_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Очки должны быть целым числом")
            return
        
        # Получаем текущие группы
        groups = self.config_data.get("Groups", {})
        
        # Обновляем группу
        groups[group_name] = points
        
        # Обновляем конфигурацию
        self.on_field_change("Groups", groups)
        
        # Обновляем таблицу
        self.load_groups()
        
        # Закрываем диалог
        dialog.destroy()
    
    def remove_group(self):
        """Удаляет выбранную группу"""
        # Получаем выбранный элемент
        selection = self.groups_tree.selection()
        if not selection:
            messagebox.showinfo("Информация", "Выберите группу для удаления")
            return
        
        # Получаем данные выбранной группы
        item = self.groups_tree.item(selection[0])
        group_name = item["values"][0]
        
        # Запрашиваем подтверждение
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить группу '{group_name}'?"):
            # Получаем текущие группы
            groups = self.config_data.get("Groups", {})
            
            # Удаляем группу
            if group_name in groups:
                del groups[group_name]
            
            # Обновляем конфигурацию
            self.on_field_change("Groups", groups)
            
            # Обновляем таблицу
            self.load_groups()
    
    def update_interval(self):
        """Обновляет значение интервала в конфигурации"""
        try:
            interval = int(self.fields["Interval_Minutes"].get())
            self.on_field_change("Interval_Minutes", interval)
        except ValueError:
            pass
