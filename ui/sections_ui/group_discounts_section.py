import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *
from ui.sections_ui.base_section import BaseSection
from utils.config_manager import update_memory_config

class GroupDiscountsSection(BaseSection):
    
    def setup_ui(self):
        """Настраивает интерфейс для GroupDiscountsSection"""
        # Создаем основной контейнер
        main_frame = tk.Frame(self.parent, bg=DARK_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Верхняя панель с информацией и кнопками
        top_panel = tk.Frame(main_frame, bg=DARK_SECONDARY)
        top_panel.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        # Информационный текст
        info_label = tk.Label(
            top_panel, 
            text="Настройка скидок для групп пользователей",
            font=FONT_SUBHEADER, 
            fg=ORANGE_PRIMARY, 
            bg=DARK_SECONDARY
        )
        info_label.pack(side=tk.LEFT)
        
        # Кнопка добавления группы
        add_button = tk.Button(
            top_panel,
            text="Добавить группу",
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            command=self.add_group
        )
        add_button.pack(side=tk.RIGHT)
        
        # Таблица групп
        table_frame = tk.Frame(main_frame, bg=DARK_SECONDARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем таблицу
        columns = ("group", "discount")
        self.groups_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настройка заголовков
        self.groups_tree.heading("group", text="Группа")
        self.groups_tree.heading("discount", text="Скидка (%)")
        
        # Настройка ширины столбцов
        self.groups_tree.column("group", width=200)
        self.groups_tree.column("discount", width=100)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.groups_tree.yview)
        self.groups_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем таблицу и скроллбар
        self.groups_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Обработчик двойного клика для редактирования
        self.groups_tree.bind("<Double-1>", self.edit_group_discount)
        
        # Обработчик удаления по клавише Delete
        self.groups_tree.bind("<Delete>", lambda event: self.delete_selected_group())
        
        # Заполняем таблицу данными
        self.display_groups()
    
    def display_groups(self):
        """Отображает группы и их скидки в таблице"""
        # Очищаем таблицу
        for i in self.groups_tree.get_children():
            self.groups_tree.delete(i)
        
        # Заполняем таблицу данными
        for group_name, discount in self.config_data.items():
            self.groups_tree.insert("", "end", values=(group_name, discount))
    
    def add_group(self):
        """Добавляет новую группу скидки"""
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.parent)
        dialog.title("Добавить группу")
        dialog.geometry("300x150")
        dialog.configure(bg=DARK_SECONDARY)
        dialog.resizable(False, False)
        dialog.transient(self.parent)  # Делаем окно модальным
        dialog.grab_set()
        
        # Центрируем окно относительно родителя
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - 300) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - 150) // 2
        dialog.geometry(f"300x150+{x}+{y}")
        
        # Поле для имени группы
        group_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        group_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        group_label = tk.Label(group_frame, text="Имя группы:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        group_label.pack(side=tk.LEFT)
        
        group_var = tk.StringVar()
        group_entry = ttk.Entry(group_frame, textvariable=group_var, width=20)
        group_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0), fill=tk.X, expand=True)
        
        # Поле для ввода процента скидки
        discount_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        discount_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        discount_label = tk.Label(discount_frame, text="Скидка %:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        discount_label.pack(side=tk.LEFT)
        
        discount_var = tk.IntVar(value=10)  # По умолчанию 10%
        discount_entry = ttk.Entry(discount_frame, textvariable=discount_var, width=5)
        discount_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
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
            command=lambda: self.save_new_group(group_var.get(), discount_var.get(), dialog)
        )
        save_button.pack(side=tk.RIGHT)
        
        # Фокус на первое поле
        group_entry.focus_set()
    
    def save_new_group(self, group_name, discount, dialog):
        """Сохраняет новую группу скидки"""
        if not group_name:
            messagebox.showerror("Ошибка", "Имя группы не может быть пустым")
            return
        
        if group_name in self.config_data:
            messagebox.showerror("Ошибка", f"Группа '{group_name}' уже существует")
            return
        
        # Сохраняем группу
        self.config_data[group_name] = discount
        
        # Обновляем таблицу
        self.display_groups()
        
        # Закрываем диалог
        dialog.destroy()
        
        # Обновляем данные в памяти
        self.on_field_change(group_name, discount)
    
    def edit_group_discount(self, event):
        """Редактирует скидку группы по двойному клику"""
        # Получаем ID выбранной строки
        selected_item = self.groups_tree.selection()
        if not selected_item:
            return
        
        # Получаем данные выбранной группы
        item = self.groups_tree.item(selected_item[0])
        group_name, discount = item["values"]
        
        # Создаем диалоговое окно
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Редактировать скидку для {group_name}")
        dialog.geometry("300x100")
        dialog.configure(bg=DARK_SECONDARY)
        dialog.resizable(False, False)
        dialog.transient(self.parent)  # Делаем окно модальным
        dialog.grab_set()
        
        # Центрируем окно относительно родителя
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - 300) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - 100) // 2
        dialog.geometry(f"300x100+{x}+{y}")
        
        # Поле для ввода процента скидки
        discount_frame = tk.Frame(dialog, bg=DARK_SECONDARY)
        discount_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        discount_label = tk.Label(discount_frame, text="Скидка %:", bg=DARK_SECONDARY, fg=LIGHT_TEXT)
        discount_label.pack(side=tk.LEFT)
        
        discount_var = tk.IntVar(value=discount)
        discount_entry = ttk.Entry(discount_frame, textvariable=discount_var, width=5)
        discount_entry.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
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
            command=lambda: self.save_group_discount(group_name, discount_var.get(), dialog)
        )
        save_button.pack(side=tk.RIGHT)
        
        # Фокус на поле ввода
        discount_entry.focus_set()
        discount_entry.select_range(0, tk.END)
    
    def save_group_discount(self, group_name, discount, dialog):
        """Сохраняет изменение скидки группы"""
        # Обновляем скидку
        self.config_data[group_name] = discount
        
        # Обновляем таблицу
        self.display_groups()
        
        # Закрываем диалог
        dialog.destroy()
        
        # Обновляем данные в памяти
        self.on_field_change(group_name, discount)
    
    def delete_selected_group(self):
        """Удаляет выбранную группу"""
        # Получаем ID выбранной строки
        selected_item = self.groups_tree.selection()
        if not selected_item:
            messagebox.showinfo("Информация", "Выберите группу для удаления")
            return
        
        # Получаем данные выбранной группы
        item = self.groups_tree.item(selected_item[0])
        group_name = item["values"][0]
        
        self.delete_group_discount(group_name)
    
    def delete_group_discount(self, group_name):
        """Удаляет группу скидки"""
        if messagebox.askyesno("Подтверждение", f"Удалить скидку для группы '{group_name}'?"):
            if group_name in self.config_data:
                del self.config_data[group_name]
                self.on_field_change(group_name, None, delete=True)
                self.display_groups()
    
    def update_discount(self, group_name, var):
        """Обновляет процент скидки для группы"""
        try:
            discount = int(var.get())
            self.config_data[group_name] = discount
            self.on_field_change(group_name, discount)
        except ValueError:
            # Игнорируем некорректные значения
            pass
    
    def on_field_change(self, key, value, delete=False):
        """Обновляет данные в конфигурации"""
        if delete:
            if key in self.config_data:
                del self.config_data[key]
        else:
            self.config_data[key] = value
        
        # Обновляем данные в памяти
        update_memory_config(self.section_name, self.config_data)