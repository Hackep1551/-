import json
import os
from tkinter import filedialog
from utils.memory_storage import memory_config

# Директория для хранения конфигураций
CONFIG_DIR = "configs"
SECTIONS_DIR = "sections"

# Путь к основному файлу шаблона
TEMPLATE_CONFIG = "config.json"

def ensure_dirs():
    """Проверяет и создаёт необходимые директории, если они не существуют"""
    for directory in [CONFIG_DIR, SECTIONS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def load_template():
    """Загружает шаблон конфигурации из файла"""
    if (os.path.exists(TEMPLATE_CONFIG)):
        try:
            with open(TEMPLATE_CONFIG, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла шаблона {TEMPLATE_CONFIG}")
            return {}
    else:
        print(f"Файл шаблона {TEMPLATE_CONFIG} не найден")
        return {}

def initialize_config():
    """Инициализирует конфигурацию из шаблона"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    
    # Проверяем наличие файла конфигурации
    if not os.path.exists(config_path):
        create_default_config(config_path)
    else:
        # Если файл существует, загружаем его в memory_config
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                for section, data in config_data.items():
                    memory_config[section] = data
        except Exception as e:
            print(f"Ошибка при загрузке config.json: {e}")
            create_default_config(config_path)

def create_default_config(config_path):
    """Создаёт файл конфигурации с настройками по умолчанию"""
    default_config = {
        "MySQL": {
            "HostAdress": "",
            "Username": "",
            "Password": "",
            "DataBaseName": "",
            "Port": 3306
        },
        "Timed_Points": {
            "Enable_Timed_Points": False,
            "Interval_Minutes": 15,
            "Groups_Stack": False,
            "Groups": {}
        },
        "Points_Stealing_On_Player_Kills": {
            "Enable": False,
            "Points_Stolen_On_Kill": 0.03,
            "Final_Reward_Multiplier": 1
        },
        "Lottery": {
            "Enable_Lottery": True,
            "Buy_Ticket_Command": "/lottery",
            "Announce_Interval_Seconds": 20,
            "Timespan_In_Minutes": 3,
            "Minimum_Participants": 2,
            "Win_Percentage": 1,
            "Entry_Price": 2500,
            "Interval_Minimum_Minutes": 15,
            "Interval_Maximum_Minutes": 60,
            "Lottery_Ingame_Name": "Lottery",
            "Messages": {}
        },
        "Logging_Options": {
            "Enable_Log_File": False,
            "Enable_Discord_Log": False,
            "Discord_Log_Webhook": "",
            "Log_Buy": True,
            "Log_Buy_Kits": True,
            "Log_Use_Kits": True,
            "Log_Points_Trading": True
        },
        "Shop_UI": {
            "Use_Custom_Categories": False,
            "Custom_Buff_HUD_Icon": "",
            "Custom_Top_Logo_Path": "",
            "Custom_Bottom_Left_WaterMark": "",
            "Custom_Bottom_Left_WaterMark_Alpha": 1,
            "Categories": {},
            "Translatable_UI_Text": {
                "Use_Translation": False
            }
        },
        "ShopSettings": {
            "Buy_Command": "/buy",
            "Sell_Command": "/sell",
            "Kit_Command": "/kit",
            "Kit_Buy_Command": "/buykit",
            "Shop_Command": "/shop",
            "Points_Command": "/points",
            "Points_Trading": {
                "Enable_Points_Trading": False,
                "Allow_Only_Same_Team": False,
                "Trade_Command": "/trade"
            },
            "Shop_Command_Opens_UI": True,
            "Use_Hexagons_As_Currency": False,
            "Shop_Name": "WShop",
            "Use_F2_To_Open_UI": False,
            "Enable_Hud_Icon": False,
            "Send_UI_Data_In_Multiple_Chunks": False,
            "Custom_Cryopod_Blueprint_Path": ""
        },
        "Group_Discounts": {},
        "Kits": {},
        "ShopItems": {},
        "SellItems": {},
        "Messages": {},
        "Notifications": {}
    }
    
    # Записываем конфигурацию в файл
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=4, ensure_ascii=False)
        
    # Также заполняем memory_config
    for section, data in default_config.items():
        memory_config[section] = data
        
    print(f"Created default configuration file at {config_path}")

def get_section_path(section_name):
    """Возвращает путь к файлу секции"""
    ensure_dirs()
    filename = f"{section_name.lower().replace(' ', '_')}.json"
    return os.path.join(SECTIONS_DIR, filename)

def load_config(section_name):
    """Загружает конфигурацию из памяти"""
    # Проверяем, есть ли раздел в памяти
    if section_name in memory_config:
        return memory_config[section_name]
    
    # Если раздела нет в памяти, пытаемся загрузить из шаблона
    template = load_template()
    if section_name in template:
        memory_config[section_name] = template[section_name].copy()
        return memory_config[section_name]
    
    # Если и в шаблоне нет, возвращаем пустой словарь
    memory_config[section_name] = {}
    return {}

def update_memory_config(section_name, config_data):
    """Обновляет конфигурацию в оперативной памяти"""
    memory_config[section_name] = config_data
    print(f"Секция {section_name} обновлена в памяти")
    return True

def get_full_config():
    """Возвращает полную конфигурацию из памяти"""
    # Загружаем все секции из шаблона, которые могут быть не в памяти
    template = load_template()
    for section_name, section_data in template.items():
        if section_name not in memory_config:
            memory_config[section_name] = section_data.copy()
            
    return memory_config

def save_config_to_file():
    """Экспортирует все конфигурации из памяти в единый JSON файл через диалог выбора файла"""
    # Открываем диалог для выбора файла сохранения
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Экспортировать конфигурацию"
    )
    
    if not file_path:  # Если пользователь отменил выбор файла
        return False
    
    try:
        # Получаем полную конфигурацию
        full_config = get_full_config()
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(full_config, file, indent=4, ensure_ascii=False)
        print(f"Конфигурация экспортирована в: {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка при экспорте конфигурации: {e}")
        return False

def load_config_from_file():
    """Импортирует конфигурацию из файла в память"""
    global memory_config
    
    # Открываем диалог для выбора файла загрузки
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Импортировать конфигурацию"
    )
    
    if not file_path:  # Если пользователь отменил выбор файла
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_config = json.load(file)
            
        # Обновляем нашу конфигурацию в памяти
        memory_config.update(loaded_config)
        print(f"Конфигурация импортирована из: {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка при импорте конфигурации: {e}")
        return False

# Инициализация системы при импорте модуля
ensure_dirs()
initialize_config()
