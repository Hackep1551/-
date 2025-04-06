from ui.sections_ui.mysql_section import MySQLSection
from ui.sections_ui.timed_points_section import TimedPointsSection
from ui.sections_ui.points_stealing_section import PointsStealingSection
from ui.sections_ui.lottery_section import LotterySection
from ui.sections_ui.logging_options_section import LoggingOptionsSection
from ui.sections_ui.shop_ui_section import ShopUISection
from ui.sections_ui.shop_settings_section import ShopSettingsSection
from ui.sections_ui.group_discounts_section import GroupDiscountsSection
from ui.sections_ui.messages_section import MessagesSection
from ui.sections_ui.notifications_section import NotificationsSection
from ui.sections_ui.shop_items_section import ShopItemsSection
from ui.sections_ui.kits_section import KitsSection
from ui.sections_ui.generic_section import GenericSection
from utils.memory_storage import memory_config

class SectionFactory:
    """Фабрика для создания объектов разделов на основе имени раздела"""
    
    @staticmethod
    def create_section(section_name, parent_frame, config_data):
        """
        Создает и возвращает соответствующий объект раздела на основе имени раздела
        
        Args:
            section_name: Имя раздела
            parent_frame: Родительский фрейм для размещения элементов
            config_data: Данные конфигурации для раздела
        
        Returns:
            Объект раздела, наследующий от BaseSection
        """
        # Проверяем наличие данных конфигурации
        if config_data is None:
            if section_name == "ShopItems":
                config_data = {}  
            elif section_name == "Kits":
                config_data = {}
            
            # Обновляем memory_config
            memory_config[section_name] = config_data
            
        if section_name == "MySQL":
            section = MySQLSection(parent_frame, section_name, config_data)
        elif section_name == "Timed_Points":
            section = TimedPointsSection(parent_frame, section_name, config_data)
        elif section_name == "Points_Stealing_On_Player_Kills":
            section = PointsStealingSection(parent_frame, section_name, config_data)
        elif section_name == "Lottery":
            section = LotterySection(parent_frame, section_name, config_data)
        elif section_name == "Logging_Options":
            section = LoggingOptionsSection(parent_frame, section_name, config_data)
        elif section_name == "Shop_UI":
            section = ShopUISection(parent_frame, section_name, config_data)
        elif section_name == "ShopSettings":
            section = ShopSettingsSection(parent_frame, section_name, config_data)
        elif section_name == "Group_Discounts":
            section = GroupDiscountsSection(parent_frame, section_name, config_data)
        elif section_name == "Messages":
            section = MessagesSection(parent_frame, section_name, config_data)
        elif section_name == "Notifications":
            section = NotificationsSection(parent_frame, section_name, config_data)
        elif section_name == "ShopItems":
            section = ShopItemsSection(parent_frame, section_name, config_data)
        elif section_name == "Kits":
            section = KitsSection(parent_frame, section_name, config_data)
        else:
            section = GenericSection(parent_frame, section_name, config_data)
            
        section.setup_ui()
        return section
