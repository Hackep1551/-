# Цветовая схема приложения
DARK_BG = "#1E1E1E"
DARK_SECONDARY = "#252526"
BUTTON_BG = "#333333"
ORANGE_PRIMARY = "#FF8C00"
LIGHT_TEXT = "#E0E0E0"
GRAY_TEXT = "#A0A0A0"
RED_BTN = "#FF0000"

# Шрифты
FONT_HEADER = ("Segoe UI", 16, "bold")
FONT_SUBHEADER = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 8)

# Отступы
PADDING_TINY = 2
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 20

# Разделы конфигурации, точно как в config.json
SECTIONS = [
    "MySQL",
    "Timed_Points",
    "Points_Stealing_On_Player_Kills",
    "Lottery",
    "Logging_Options",
    "Shop_UI",
    "ShopSettings",
    "Group_Discounts",
    "Kits",
    "ShopItems",
    "SellItems",
    "Messages",
    "Notifications"
]

# Импорт функции обновления конфигурации в памяти
from utils.config_manager import update_memory_config
