"""Модуль для хранения конфигурации в оперативной памяти"""

# Глобальный словарь для хранения конфигурации
memory_config = {}

def get_section(section_name):
    """Возвращает данные раздела из памяти"""
    return memory_config.get(section_name, {})

def update_section(section_name, data):
    """Обновляет данные раздела в памяти"""
    memory_config[section_name] = data

def delete_section(section_name):
    """Удаляет раздел из памяти"""
    if section_name in memory_config:
        del memory_config[section_name]
