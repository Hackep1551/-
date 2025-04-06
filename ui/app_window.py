import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from ui.constants import *
from ui.sections_ui.section_factory import SectionFactory
from utils.config_manager import load_config, save_config
from utils.memory_storage import memory_config

class AppWindow:
    """Класс основного окна приложения"""
    
    def __init__(self, root):
        """
        Инициализирует основное окно приложения
        
        Args:
            root: Корневой объект tkinter
        """
        self.root = root
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        # Настройка основного окна
        self.root.title("ARK Shop Config Creator")
        self.root.geometry("1200x800")
        self.root.configure(bg=DARK_BG)
        
        # Создание основного фрейма
        main_frame = tk.Frame(self.root, bg=DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создание левой панели с секциями конфигурации
        left_panel = tk.Frame(main_frame, bg=DARK_SECONDARY, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        left_panel.pack_propagate(False)  # Запрет изменения размера
        
        # Заголовок для левой панели
        header_label = tk.Label(left_panel, text="Разделы конфигурации", 
                            font=FONT_HEADER, fg=ORANGE_PRIMARY, bg=DARK_SECONDARY)
        header_label.pack(padx=PADDING_MEDIUM, pady=PADDING_MEDIUM, anchor="w")
        
        # Создание scrollable контейнера для списка секций
        section_container = tk.Frame(left_panel, bg=DARK_SECONDARY)
        section_container.pack(fill=tk.BOTH, expand=True, padx=PADDING_SMALL, pady=PADDING_SMALL)
        
        # Канва и скроллбар для прокрутки секций
        self.canvas = tk.Canvas(section_container, bg=DARK_SECONDARY, 
                            highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(section_container, orient="vertical", 
                                    command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=DARK_SECONDARY)
        
        # Конфигурация скроллинга
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Размещение элементов
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Правая панель с содержимым секции
        self.right_panel = tk.Frame(main_frame, bg=DARK_BG)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Создание нижней панели с кнопками управления
        bottom_panel = tk.Frame(self.root, bg=DARK_SECONDARY, height=50)
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        # Кнопка предпросмотра JSON
        preview_button = tk.Button(bottom_panel, text="Предпросмотр JSON", 
                              command=self.preview_json,
                              bg=BUTTON_BG, fg=LIGHT_TEXT,
                              padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        preview_button.pack(side=tk.LEFT, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        # Кнопки импорта и экспорта
        import_button = tk.Button(bottom_panel, text="Импорт", 
                               command=self.import_config,
                               bg=BUTTON_BG, fg=LIGHT_TEXT,
                               padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        import_button.pack(side=tk.RIGHT, padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        
        export_button = tk.Button(bottom_panel, text="Экспорт", 
                               command=self.export_config,
                               bg=BUTTON_BG, fg=LIGHT_TEXT,
                               padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        export_button.pack(side=tk.RIGHT, padx=(0, PADDING_SMALL), pady=PADDING_SMALL)
        
        # Сохраняем ссылки на текущий отображаемый раздел
        self.current_section = None
        self.current_section_frame = None
    
    def load_config(self):
        """Загружает конфигурацию и создает кнопки для разделов"""
        # Загрузка конфигурации
        self.config = load_config()
        
        # Создание кнопок для разделов конфигурации
        for section_name in self.config:
            btn = tk.Button(self.scrollable_frame, 
                         text=section_name.replace("_", " "), 
                         bg=BUTTON_BG, fg=LIGHT_TEXT,
                         padx=PADDING_MEDIUM, pady=PADDING_SMALL,
                         anchor="w", width=25,
                         command=lambda s=section_name: self.show_section(s))
            btn.pack(fill=tk.X, padx=PADDING_SMALL, pady=PADDING_TINY)
    
    def show_section(self, section_name):
        """Отображает содержимое выбранной секции конфигурации"""
        # Если есть текущая секция, уничтожаем её
        if self.current_section_frame:
            self.current_section_frame.destroy()
        
        # Создаем новый фрейм для содержимого секции
        self.current_section_frame = tk.Frame(self.right_panel, bg=DARK_SECONDARY)
        self.current_section_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Получаем данные для выбранной секции из памяти
        section_data = memory_config.get(section_name, {})
        
        # Создаем интерфейс для секции с помощью фабрики
        self.current_section = SectionFactory.create_section(
            section_name, 
            self.current_section_frame, 
            section_data
        )
    
    def save_config_to_file(self):
        """Сохраняет конфигурацию в файл"""
        if save_config():
            messagebox.showinfo("Успех", "Конфигурация успешно сохранена")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить конфигурацию")
    
    def import_config(self):
        """Импортирует конфигурацию из выбранного файла JSON"""
        file_path = filedialog.askopenfilename(
            title="Импорт конфигурации",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return  # Пользователь отменил выбор файла
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                imported_config = json.load(file)
            
            # Обновляем memory_config
            memory_config.clear()
            for section, data in imported_config.items():
                memory_config[section] = data
            
            # Пересоздаем UI
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
                
            if self.current_section_frame:
                self.current_section_frame.destroy()
                self.current_section = None
                
            # Создание кнопок для разделов конфигурации
            for section_name in memory_config:
                btn = tk.Button(self.scrollable_frame, 
                             text=section_name.replace("_", " "), 
                             bg=BUTTON_BG, fg=LIGHT_TEXT,
                             padx=PADDING_MEDIUM, pady=PADDING_SMALL,
                             anchor="w", width=25,
                             command=lambda s=section_name: self.show_section(s))
                btn.pack(fill=tk.X, padx=PADDING_SMALL, pady=PADDING_TINY)
            
            messagebox.showinfo("Успех", f"Конфигурация успешно импортирована из {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать конфигурацию: {str(e)}")
    
    def export_config(self):
        """Экспортирует конфигурацию в выбранный файл JSON"""
        file_path = filedialog.asksaveasfilename(
            title="Экспорт конфигурации",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return  # Пользователь отменил выбор файла
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(memory_config, file, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Успех", f"Конфигурация успешно экспортирована в {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать конфигурацию: {str(e)}")
    
    def preview_json(self):
        """Открывает окно предпросмотра конфигурации в формате JSON"""
        # Создаем новое окно для предпросмотра
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Предпросмотр JSON")
        preview_window.geometry("800x600")
        preview_window.configure(bg=DARK_SECONDARY)
        
        # Создаем текстовый виджет с прокруткой
        text_frame = tk.Frame(preview_window, bg=DARK_SECONDARY)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Используем моноширинную гарнитуру для лучшего отображения JSON
        preview_text = tk.Text(text_frame, bg=DARK_BG, fg=LIGHT_TEXT, wrap=tk.NONE, 
                            font=("Courier New", 10), yscrollcommand=text_scroll.set)
        preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Добавляем также горизонтальную прокрутку
        h_scroll = ttk.Scrollbar(preview_window, orient='horizontal', command=preview_text.xview)
        h_scroll.pack(fill=tk.X)
        preview_text.configure(xscrollcommand=h_scroll.set)
        
        text_scroll.config(command=preview_text.yview)
        
        # Форматируем JSON для лучшей читаемости
        formatted_json = json.dumps(memory_config, indent=4, ensure_ascii=False)
        preview_text.insert(tk.END, formatted_json)
        preview_text.configure(state='disabled')  # Делаем поле только для чтения
        
        # Кнопка копирования в буфер обмена
        copy_button = tk.Button(preview_window, text="Копировать в буфер обмена", 
                               bg=BUTTON_BG, fg=LIGHT_TEXT,
                               command=lambda: self.copy_to_clipboard(formatted_json))
        copy_button.pack(pady=PADDING_MEDIUM)
    
    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Успех", "JSON-конфигурация скопирована в буфер обмена")
