import json
import os
from utils.memory_storage import memory_config

def load_config():
    """Загружает конфигурацию из файла"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            
            # Загружаем данные в оперативную память
            for section, data in config_data.items():
                memory_config[section] = data
            
            return config_data
    except Exception as e:
        print(f"Ошибка при загрузке конфигурации: {e}")
        return {}

def save_config():
    """Сохраняет конфигурацию из памяти в файл"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(memory_config, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении конфигурации: {e}")
        return False

def update_memory_config(section, data, delete=False):
    """Обновляет раздел конфигурации в памяти"""
    if delete:
        if section in memory_config:
            del memory_config[section]
    else:
        memory_config[section] = data

def import_config_from_file(file_path):
    """Импортирует конфигурацию из указанного файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
        return config_data
    except Exception as e:
        print(f"Ошибка при импорте конфигурации: {e}")
        raise

def export_config_to_file(config_data, file_path):
    """Экспортирует конфигурацию в указанный файл"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Ошибка при экспорте конфигурации: {e}")
        return False

def get_config_from_memory():
    """Возвращает текущую конфигурацию из памяти"""
    return memory_config
