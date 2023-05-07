from src.ui.base import AbstractMenu
from src.ui.user import UserMenu
from src.ui.weather_station import WeatherStationMenu


class MainMenu(AbstractMenu):
    @classmethod
    def _get_menu_options(cls) -> list[tuple[str, callable]]:
        return [
            ("User menu", UserMenu.run),
            ("Weather station menu", WeatherStationMenu.run),
        ]
